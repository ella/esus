# -*- coding: utf-8 -*-
from djangosanetesting.cases import DatabaseTestCase

from esus.phorum.access import AccessManager

from unit_project.tests.fixtures import users_usual, table_simple, comment_simple


class TestCommentAccess(DatabaseTestCase):
    def setUp(self):
        self.manager = AccessManager()
        users_usual(self)
        table_simple(self)
        comment_simple(self)

        super(TestCommentAccess, self).setUp()

    def test_any_logged_user_can_comment(self):
        self.assert_true(self.manager.has_comment_create(
            user = self.user_tester,
            table = self.table,
        ))

    def test_table_owner_can_delete_comment(self):
        self.assert_true(self.manager.has_comment_delete(
            user = self.user_tester,
            comment = self.comment_doe,
        ))

    def test_common_user_cannot_delete_comment(self):
        self.assert_false(self.manager.has_comment_delete(
            user = self.user_john_doe,
            comment = self.comment_owner,
        ))

