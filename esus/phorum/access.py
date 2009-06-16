from inspect import getargspec

from django.conf import settings

__all__ = ("InsufficientContextError", "AccessManager")

class InsufficientContextError(Exception):
    """
    When Esus has_<custom_permission> is called from template and do not has
    required context setted up, raise this exception to let programmer know to
    set it up properly in view
    """


def check_required_context(fn):
    """
    Check if all arguments required in the method are available in instance's
    context dictionary attribute and call method with values present there.
    
    If some kwargs where specified in call, they're preferred over context. Args
    are ignored.

    If not, raise InsufficientContextError
    """
    def _innerWrapper(self, *args, **kwargs):
        # get arguments, strip self out
        args = getargspec(fn)[0][1:]

        new_kwargs = {}
        for arg in args:
            if self.context.has_key(arg):
                new_kwargs[arg] = self.context[arg]
            elif kwargs.has_key(arg):
                # taking preference under cycle
                pass
            else:
                raise InsufficientContextError(''.join([u"Context %(key)s is required",
                    " for calling permision %(permission)s, but not found in",
                    " current context %(context)s"]) % {
                        "key" : arg,
                        "permission" : str(fn),
                        "context" : str(self.context)
                    })
        new_kwargs.update(kwargs)
        
        return fn(self, **new_kwargs)
    return _innerWrapper

class AccessManager(object):
    """
    Provide our logic for more complicated permissions
    """
    # Only attributes specified in this list are not delgated to underlying
    # AccessManager
    MY_ATTRIBUTES = [
        "__init__",
        "_backend", "backend", "get_backend",
        "context"
    ]

    def __init__(self, context=None):
        super(AccessManager, self).__init__()

        self._backend = None
        self.context = context or {}

    def __getattribute__(self, attr):
        """

        """
        if attr not in object.__getattribute__(self, "MY_ATTRIBUTES"):
            return getattr(self.backend, attr)
        else:
            return object.__getattribute__(self, attr)

    def get_backend(self):
        if not self._backend:
            backend_name = getattr(settings, "ESUS_ACCESS_SERVICE", "esus.phorum.access.EsusAccessManager")
            modules = backend_name.split(".")
            module = __import__(modules[0])
            for mod in modules[1:]:
                if not hasattr(module, mod):
                    raise ValueError("Access backend not configured")
                module = getattr(module, mod)

            self._backend = module(context=self.context)
        return self._backend

    backend = property(fget=get_backend)

class AccessInterface(object):
    """
    Service functions for every implementing backend
    """
    def __init__(self, context=None):
        super(AccessInterface, self).__init__()

        self.context = context or {}

    def update_context(self, context):
        self.context.update(context)

class EsusAccessManager(AccessInterface):
    """
    EsusAccessManager also defines interface any interface should implement.
    Don't forget to use decorators, too
    """
    
    @check_required_context
    def has_comment_create(self, user, table):
        """
        Can user post comment to given table?

        Yes, if he is authenticated and table is public. Otherwise, see how custom
        this implementation is.
        """
        if not user.is_authenticated():
            return False

        category = self.context.get("category", None) or table.category

        if not table.is_public:
            raise NotImplementedError()
        else:
            return True

    @check_required_context
    def has_comment_delete(self, user, comment):
        """
        Can user delete comment for given table?
        
        User can delete comment, if:
            * he is table owner
        """
        if not user.is_authenticated():
            return False

        table = self.context.get("table", None) or comment.table

        if user == table.owner:
            return True

        return False
        
    @check_required_context
    def has_table_access_modify(self, user, table):
        """
        Can user modify access rights to table?

        Yes, if:
            * he is table owner
        """

        if user == table.owner:
            return True
        else:
            return False

