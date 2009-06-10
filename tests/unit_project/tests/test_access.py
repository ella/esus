# -*- coding: utf-8 -*-
from djangosanetesting.cases import DatabaseTestCase

from esus.phorum.access import AccessManager, InsufficientContextError

from unit_project.tests.fixtures import users_usual, user_super, table_simple


class TestAccessHandling(DatabaseTestCase):
    def setUp(self):
        self.manager = AccessManager()
        users_usual(self)
        user_super(self)
        table_simple(self)

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

