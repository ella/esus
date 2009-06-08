# -*- coding: utf-8 -*-
from example_project.tests.helpers import EsusTestCase
from example_project.tests.fixtures import create_zena_categories, create_tables

from esus.phorum.models import Category

class TestCategories(EsusTestCase):

    def setUp(self):
        create_zena_categories(self)
        create_tables(self)
        
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


    def test_tables_in_category_shown(self):
        s = self.selenium

        # go inside category with table
        s.click(self.elements['navigation']['categories'])
        s.click(self.elements['pages']['category']['categories_list']+"/a[@href='/category/kong-fuzi-de-zhexue']")

        # check first table is as expected
        self.assert_equals(u"孔夫子得学徒", s.get_text(self.elements['pages']['category']['tables_list']+"[1]/a"))

