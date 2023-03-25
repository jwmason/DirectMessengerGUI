# Mason Wong
# masonjw1@uci.edu
# 48567424

"""This module tests profile"""

import unittest
from Profile import Profile


class TestProfile(unittest.TestCase):
    """This tests profile"""
    def test_profile(self):
        """Tests attributes"""
        username = "test_user"
        password = "test_pass"
        profile = Profile(username, password)

        self.assertEqual(profile.username, username)
        self.assertEqual(profile.password, password)
        self.assertListEqual(profile._messages, [])
        self.assertListEqual(profile.sent_messages, [])
        self.assertListEqual(profile.friends, [])


if __name__ == '__main__':
    unittest.main()
