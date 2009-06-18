# -*- coding: utf-8 -*-
from djangosanetesting.cases import DatabaseTestCase, UnitTestCase

from esus.phorum.access import (
    AccessManager, InsufficientContextError,
    TableAccessManager, FULL_ACCESS_CODE
)

from unit_project.tests.fixtures import users_usual, user_super, table_simple, comment_simple


class TestAccessHandling(DatabaseTestCase):
    def setUp(self):
        self.manager = AccessManager()
        users_usual(self)
        user_super(self)
        table_simple(self)
        comment_simple(self)

        super(TestAccessHandling, self).setUp()

    def test_missing_context(self):
        self.assert_raises(InsufficientContextError, self.manager.has_comment_create)

    def test_superuser_always_privileged(self):
        self.manager.update_context({
            "table" : self.table,
            "category" : self.category,
            "user" : self.user_super,
        })
        self.assert_true(self.manager.has_comment_create())
        self.assert_true(self.manager.has_comment_delete(comment=self.comment_doe))
        self.assert_true(self.manager.has_table_read())


class TestTableAccessManager(UnitTestCase):
    def test_selected_defaults_can_read(self):
        manager = TableAccessManager(TableAccessManager.get_default_access())
        self.assert_true(manager.can_read())

    def test_selected_defaults_can_write(self):
        manager = TableAccessManager(TableAccessManager.get_default_access())
        self.assert_true(manager.can_write())

    def test_selected_defaults_cannot_delete(self):
        manager = TableAccessManager(TableAccessManager.get_default_access())
        self.assert_false(manager.can_delete())

    def test_selected_defaults_can_read_write_as_named(self):
        self.assert_equals(TableAccessManager.compute_named_access(["read", "write"]),
            TableAccessManager.get_default_access())
            
    def test_full_access(self):
        manager = TableAccessManager(FULL_ACCESS_CODE)
        self.assert_true(manager.can_read())
        self.assert_true(manager.can_write())
        self.assert_true(manager.can_delete())

    def test_no_access(self):
        manager = TableAccessManager(TableAccessManager.compute_named_access([]))
        self.assert_false(manager.can_read())
        self.assert_false(manager.can_write())
        self.assert_false(manager.can_delete())

    def test_read_only(self):
        manager = TableAccessManager(TableAccessManager.compute_named_access(["read"]))
        self.assert_true(manager.can_read())
        self.assert_false(manager.can_write())
        self.assert_false(manager.can_delete())
