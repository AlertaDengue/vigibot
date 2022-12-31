__author__ = 'fccoelho'

import unittest
from telegram import Update, User, Bot, InlineQuery, Location
from vigibot.handlers import check_user_exists, add_user, add_location, inlinequery


class U:
    id = 1
    first_name = 'ze'
    last_name = 'teste'


class L:
    latitude = 23.0
    longitude = -46.2


class HandlersTestCase(unittest.TestCase):
    def test_check_for_new_user_returns_false(self):
        res = check_user_exists(90290)
        self.assertFalse(res)

    def test_add_a_user(self):
        res = check_user_exists(1)
        if not res:
            add_user(U())
            res = check_user_exists(1)
        self.assertTrue(res)

    def test_add_location(self):
        user = U()
        location = L()
        add_location(user, location)

    # def test_inline_query(self):
    #     upd = Update(
    #         0,
    #         inlinequery=InlineQuery(
    #             'id',
    #             User(2, 'test user', False),
    #             'test query',
    #             offset='22',
    #             location=Location(latitude=-23.691288, longitude=-46.788279),
    #         ),
    #     )
    #     inlinequery(upd, {})
    #     pass


if __name__ == '__main__':
    unittest.main()
