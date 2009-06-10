class EsusAuthenticationBackend(object):
    """
    Provide our logic for more complicated permissions
    """

    def authenticate(self, *args, **kwargs):
        """
        This backend is not used for authentication, always returns None
        """
        return None

    def get_user(self, *args, **kwargs):
        """
        This backend is not used for authentication, always returns None
        """
        return None

    def has_perm(self, user_obj, perm, **kwargs):
        """
        Custom permission handlign: If we're providing perm_<perm_name> method,
        it's called for authentication and **kwargs are delegated.

        Otherwise, we're returning False as we're leaving work for Django
        permissions.
        """

        attr = getattr(self, "perm_%s" % perm, None)

        if not attr:
            return False
        else:
            return attr(user_obj=user_obj, **kwargs)


