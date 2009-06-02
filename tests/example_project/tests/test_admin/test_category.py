
from example_project.tests.test_admin.helpers import AdminTestCase

class TestHallAdministration(AdminTestCase):
    """
    Test CRUD of categories (for admin).
    """

    def test_creation(self):
        s = self.selenium

        s.click(self.elements['pages']['welcome']['category_add'])

        s.type('id_name', u"Example category")
        s.type('id_slug', u"example-hall")
#        s.type('id_description', u"Description")

        s.click(self.elements['listing']['save'])

        self.assert_equals(u"Example category", s.get_text(self.elements['listing']['list_first']))

