from example_project.tests.helpers import EsusTestCase
from example_project.tests.fixtures import create_zena_categories

from esus.phorum.models import Category

class TestCategories(EsusTestCase):

    def setUp(self):
        create_zena_categories(self)

        super(TestCategories, self).setUp()

    def test_categories_shown(self):
        s = self.selenium
        s.click(self.elements['navigation']['categories'])
        categories = Category.objects.all()
        page_categories = []
        for i in xrange(0, len(categories)):
            page_categories.append(s.get_text(self.elements['pages']['category']['categories_list']+"[%d]" % (i+1)))
        # check all categories are in place
        for category in categories:
            self.assert_equals(True, category.name in page_categories)

    def test_simple_discussion_creation(self):
        s = self.selenium
        s.click(self.elements['navigation']['categories'])

