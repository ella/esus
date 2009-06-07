# -*- coding: utf-8 -*-
from example_project.tests.helpers import EsusTestCase
from example_project.tests.fixtures import create_zena_categories, create_tables

class TestTables(EsusTestCase):

    def setUp(self):
        create_zena_categories(self)
        create_tables(self)

        super(TestTables, self).setUp()

    def test_table_creation(self):
        s = self.selenium

        # go inside first category
        s.click(self.elements['navigation']['categories'])
        s.click(self.elements['pages']['category']['categories_list']+"[1]/a")

        # go for "Create table link
        s.click(self.elements['pages']['category']['table_add'])

        s.type(u"id_name", u"论语: Lún Yǔ")
        s.type(u"id_description", u"Peacful discussion about those works of Kǒng Fūzǐ")

        s.click(self.elements['navigation']['submit_form'])
        s.wait_for_page_to_load(30000)

        self.assert_equals(u"论语: Lún Yǔ", s.get_text(self.elements['pages']['table']['name']))

    def test_article_adding(self):
        s = self.selenium

        # go inside category with table
        s.click(self.elements['navigation']['categories'])
        s.click(self.elements['pages']['category']['categories_list']+"/a[@href='/category/kong-fuzi-de-zhexue']")

        # go to first table
        s.click(self.elements['pages']['category']['tables_list']+"[1]/a")

        # add testing text
        s.type("id_text", u"""
= Important =

This is ""Czechtile"" text.
""")
        # submit
        s.click(u"//input[@type='submit']")
        s.wait_for_page_to_load(30000)

        self.assert_equals("Important", s.get_text("//div[@id='comments']/div[@class='comment']/h1"))
