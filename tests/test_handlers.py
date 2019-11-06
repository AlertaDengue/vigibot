__author__ = 'fccoelho'

import unittest
from vigibot.handlers import check_user_exists, add_user, add_location


class U:
    id = 1
    first_name = 'ze'
    last_name = 'teste'
    
class L:
    latitude = 23.0
    longitude = -46.2

class MyTestCase(unittest.TestCase):
    def test_check_for_new_user_returns_false(self):
        res = check_user_exists(90290)
        self.assertFalse(res)
    def test_add_a_user(self):
        add_user(U())
        res = check_user_exists(1)
        self.assertTrue(res)
        
    def test_add_location(self):
        user = U()
        location = L()
        add_location(user, location)
        


if __name__ == '__main__':
    unittest.main()
