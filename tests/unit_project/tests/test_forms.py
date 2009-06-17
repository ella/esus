# -*- coding: utf-8 -*-
from djangosanetesting.cases import DatabaseTestCase

from esus.phorum.forms import TableAccessForm

from unit_project.tests.fixtures import user_super


class TestUserForms(DatabaseTestCase):
    def setUp(self):
        user_super(self)
        super(TestUserForms, self).setUp()

    def test_nonexisting_users_not_valid(self):
        table_access_form = TableAccessForm({
            'can_read' : False,
            'can_write' : False,
            'can_delete' : False,
            'username' : "nonexisting user",
        })
        self.assert_false(table_access_form.is_valid())

    def test_existing_users_valid(self):
        table_access_form = TableAccessForm({
            'can_read' : False,
            'can_write' : False,
            'can_delete' : False,
            'username' : "superuser",
        })
        self.assert_true(table_access_form.is_valid())

    def test_access_detection_empty(self):
        table_access_form = TableAccessForm({
            'can_read' : False,
            'can_write' : False,
            'can_delete' : False,
            'username' : "superuser",
        })
        self.assert_true(table_access_form.is_valid())
        self.assert_equals([], table_access_form.get_access_names())

    def test_access_detection_full(self):
        table_access_form = TableAccessForm({
            'can_read' : True,
            'can_write' : True,
            'can_delete' : True,
            'username' : "superuser",
        })
        self.assert_true(table_access_form.is_valid())
        self.assert_equals(["read", "write", "delete"], table_access_form.get_access_names())

    def test_access_detection_partial(self):
        table_access_form = TableAccessForm({
            'can_read' : True,
            'can_write' : False,
            'can_delete' : True,
            'username' : "superuser",
        })
        self.assert_true(table_access_form.is_valid())
        self.assert_equals(["read", "delete"], table_access_form.get_access_names())
