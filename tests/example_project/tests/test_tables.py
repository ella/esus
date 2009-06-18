# -*- coding: utf-8 -*-
#from django.utils.translation import ugettext_lazy as _

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

        self.assert_equals("Important", s.get_text("//div[@id='comments']/div[@class='comment']//h1[position()=1]"))


    def test_article_deleting(self):
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
        s.click(u"//input[@name='Odeslat']")
        s.wait_for_page_to_load(30000)

        articles_count = int(s.get_xpath_count("//div[@id='comments']/div[@class='comment']"))

        # select last comment for deletion
        #self.assert_equals("Important", s.get_text("//div[@id='comments']/div[@class='comment'][1]//input[@type='checkbox']"))
        s.check('id_form-0-DELETE')
        s.click(u"//input[@name='control-action']")
        s.wait_for_page_to_load(30000)

        # comment should not be present
        self.assert_equals(articles_count-1, int(s.get_xpath_count("//div[@id='comments']/div[@class='comment']")))

class TestTableAccess(EsusTestCase):
    def setUp(self):
        create_zena_categories(self)
        create_tables(self)

        super(TestTableAccess, self).setUp()

    def go_to_admin_table_access(self):
        s = self.selenium

        # go to my table access settings
        s.click(self.elements['navigation']['categories'])
        s.wait_for_page_to_load(30000)
        s.click(self.elements['pages']['category']['categories_list']+"/a[@href='/category/sex']")
        s.wait_for_page_to_load(30000)
        s.click(self.elements['pages']['category']['tables_list']+"[1]/a")
        s.wait_for_page_to_load(30000)
        s.click(self.elements['pages']['table']['access'])
        s.wait_for_page_to_load(30000)

    def test_user_banning(self):
        # login as superuser and ban user Tester
        self.logout()
        self.login_superuser()

        s = self.selenium
        self.go_to_admin_table_access()

        # add him to list
        s.type('id_username', u"Tester")
        s.click(self.elements['pages']['table_access']['submit_new_user'])
        s.wait_for_page_to_load(30000)

        # revoke rw privileges
        s.click(self.elements['pages']['table_access']['users_list']['access_read'] % {'position' : 0})
        s.click(self.elements['pages']['table_access']['users_list']['access_write'] % {'position' : 0})
        s.click(self.elements['pages']['table_access']['submit_users'])
        s.wait_for_page_to_load(30000)

        # login as banned user
        self.logout()
        self.login_user()

        # try to go to table
        s.click(self.elements['navigation']['categories'])
        s.wait_for_page_to_load(30000)
        s.click(self.elements['pages']['category']['categories_list']+"/a[@href='/category/sex']")
        s.wait_for_page_to_load(30000)
        s.click(self.elements['pages']['category']['tables_list']+"[1]/a")
        s.wait_for_page_to_load(30000)

        # check banned message present
#        self.assert_true(s.is_text_present(unicode(_("You have not enough privileges to read this table."))))
        self.assert_true(s.is_text_present("You have not enough privileges to read this table."))
