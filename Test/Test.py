from Main import app
from Processing import initiatePaths
from sanic.log import logger
from Constants import *
import unittest, json


class PosRestTests(unittest.TestCase):
    def setUp(self):
        initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logger)

    def testHome(self):  # testing if the home page has 200 response
        req, resp = app.test_client.get('/')
        self.assertEqual(resp.status, 200)

    def testGetUsers(self):  # checking if all the users in the file are processed
        req, resp = app.test_client.get('/users')
        self.assertEqual(resp.status, 200,
                         "Error Obtaining users list from {}-{}".format(TEST_USER_LIST_FILE_PATH, resp.text))
        data = json.loads(resp.text)
        with open(TEST_USER_LIST_FILE_PATH) as f:
            tot = sum(1 for _ in f)
            self.assertEqual(len(data), tot,
                             "Error processing user list from {}.".format(TEST_USER_LIST_FILE_PATH) +
                             "{} users data is processed instead of {}".format(len(data), tot))

    def testGetUserById(self):  # checking if an available users data is obtained
        user_check_id = '104'
        req, resp = app.test_client.get('/users/{}'.format(user_check_id))
        self.assertEqual(resp.status, 200, "Error Obtaining user data-{}".format(resp.text))
        data = json.loads(resp.text)
        self.assertEqual(data[USER_ID_KEY], user_check_id, "wrong user data obtained")

    def testGetUserMatches(self):  # checking combinations of matches in user data
        user_check_id = '104'
        req, resp = app.test_client.get('/users/query?uid={}'.format(user_check_id))
        self.assertEqual(resp.status, 200, "Error Obtaining user data-{}".format(resp.text))
        data = json.loads(resp.text)
        self.assertEqual(len(data), 1, "Only user data should be obtained")
        self.assertEqual(data[0][USER_ID_KEY], user_check_id, "wrong user data obtained")

        user_name = 'meera'
        user_comment = 'Meera Yadav'
        req, resp = app.test_client.get('/users/query?comment={}'.format(user_comment))
        self.assertEqual(resp.status, 200, "Error Obtaining user data-{}".format(resp.text))
        data = json.loads(resp.text)
        self.assertEqual(len(data), 1, "Only user data should be obtained")
        self.assertEqual(data[0][USER_NAME_KEY], user_name, "Wrong user data obtained")

        home = '/var/lib/gnats'  # ASSUME: test data does not change
        req, resp = app.test_client.get('/users/query?home={}'.format(home))
        self.assertEqual(resp.status, 200, "Error Obtaining user data-{}".format(resp.text))
        data = json.loads(resp.text)
        self.assertEqual(len(data), 1, "Only user data should be obtained")
        self.assertEqual(data[0][USER_NAME_KEY], 'gnats', "Wrong user data obtained")

    def testGroupsByUser(self):  # checking if group list is returned for a valid userid
        user_check_id = '7'
        team_count = 4
        req, resp = app.test_client.get('/users/{}/groups'.format(user_check_id))
        self.assertEqual(resp.status, 200, "Error Obtaining user data-{}".format(resp.text))
        data = json.loads(resp.text)
        self.assertEqual(len(data), team_count, "{} should belong to only {} teams".format(user_check_id, team_count))

    def testGroups(self):  # checking if all the available groups in the file are processed
        req, resp = app.test_client.get('/groups')
        self.assertEqual(resp.status, 200,
                         "Error Obtaining groups list from {} - {}".format(TEST_GROUP_LIST_FILE_PATH, resp.text))
        data = json.loads(resp.text)
        with open(TEST_GROUP_LIST_FILE_PATH) as f:
            tot = sum(1 for _ in f)
            self.assertEqual(len(data), tot,
                             "Error processing Group list from {}.".format(TEST_USER_LIST_FILE_PATH) +
                             "{} Groups data is processed instead of {}".format(len(data), tot))

    def testGroupById(self):  # checking if an available group data can be obtained by id
        group_id = '104'
        req, resp = app.test_client.get('/groups/{}'.format(group_id))
        self.assertEqual(resp.status, 200, "Error Obtaining group data-{}".format(resp.text))
        data = json.loads(resp.text)
        self.assertEqual(data[GROUP_ID_KEY], group_id, "Wrong group details obtained")

    def testGroupMatch(self):  # checking combinations of group match from available data
        group_id = '104'
        req, resp = app.test_client.get('/groups/query?{}={}'.format(GROUP_ID_KEY, group_id))
        self.assertEqual(resp.status, 200, "Error Obtaining group data-{}".format(resp.text))
        data = json.loads(resp.text)
        self.assertEqual(len(data), 1, "only one group data should be obtained")
        self.assertEqual(data[0][GROUP_ID_KEY], group_id, "Wrong group details obtained")

        member1 = 'landscape'
        member2 = 'lp'
        req, resp = app.test_client.get('/groups/query?member={}&member={}'.format(member1, member2))
        self.assertEqual(resp.status, 200, "Error Obtaining group data-{}".format(resp.text))
        data = json.loads(resp.text)
        self.assertEqual(len(data), 2, "only two group data should be obtained")


class NegRestTests(unittest.TestCase):
    def setUp(self):
        initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logger)

    def testGetUsers(self):  # checking if correct error code is returned if file not present
        initiatePaths("/etc", TEST_GROUP_LIST_FILE_PATH, logger)
        req, resp = app.test_client.get('/users')
        self.assertEqual(resp.status, CONFLICT_ERROR_CODE)
        initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logger)

    def testGetUserById(self):  # checking if an unavailable users data is not obtained
        user_check_id = '500'
        req, resp = app.test_client.get('/users/{}'.format(user_check_id))
        self.assertEqual(resp.status, NOT_FOUND_CODE, "Error Obtaining user data-{}".format(resp.text))

    def testGetUserMatches(self):  # checking combinations of matches in user data
        user_check_id = '104'
        user_name = 'meera'
        req, resp = app.test_client.get('/users/query?uid={}&name={}'.format(user_check_id, user_name))
        self.assertEqual(resp.status, 200, "Error Obtaining user data-{}".format(resp.text))
        data = json.loads(resp.text)
        self.assertEqual(len(data), 0,
                         "No user data should be obtained for uid {} and name {}".format(user_check_id, user_name))

    def testGroupsByUser(self):  # checking if error code returned for a invalid userid
        user_check_id = '500'
        req, resp = app.test_client.get('/users/{}/groups'.format(user_check_id))
        self.assertEqual(resp.status, NOT_FOUND_CODE, "Error Obtaining user data-{}".format(resp.text))

    def testGroups(self):  # checking if correct error code is returned if file not present
        initiatePaths(TEST_USER_LIST_FILE_PATH, '/etc', logger)
        req, resp = app.test_client.get('/groups')
        self.assertEqual(resp.status, CONFLICT_ERROR_CODE)
        initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logger)

    def testGroupById(self):  # checking if an unavailable group data can not be obtained by id
        group_id = '500'
        req, resp = app.test_client.get('/groups/{}'.format(group_id))
        self.assertEqual(resp.status, NOT_FOUND_CODE, "Error Obtaining group data-{}".format(resp.text))

    def testGroupMatch(self):  # checking combinations of group match from available data
        member2 = 'lp'
        member3 = 'syslog'
        req, resp = app.test_client.get('/groups/query?member={}&member={}'.format(member2, member3))
        self.assertEqual(resp.status, 200, "Error Obtaining group data-{}".format(resp.text))
        data = json.loads(resp.text)
        self.assertEqual(len(data), 0, "No group data should be obtained")

    def testEmptyFilePath(self):
        with self.assertRaises(SystemExit) as e:
            initiatePaths("", TEST_GROUP_LIST_FILE_PATH, logger)
            self.assertEqual(e.exception.code, 1)
        with self.assertRaises(SystemExit) as e:
            initiatePaths(TEST_USER_LIST_FILE_PATH, "", logger)
            self.assertEqual(e.exception.code, 1)


# class MultiRestTests(unittest.TestCase):
#     def setUp(self):
#         initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logger.error)
#
#     def testGetUsers(self):  # checking if correct error code is returned if file not present
#         req, resp = app.test_client.get('/users')
#         self.assertEqual(resp.status, 200,
#                          "Error Obtaining users list from {}-{}".format(TEST_USER_LIST_FILE_PATH, resp.text))
#         data = json.loads(resp.text)
#         tot = None
#         with open(TEST_USER_LIST_FILE_PATH) as f:
#             tot = sum(1 for _ in f)
#         self.assertEqual(len(data), tot,
#                          "Error processing user list from {}.".format(TEST_USER_LIST_FILE_PATH) +
#                          "{} users data is processed instead of {}".format(len(data), tot))


if __name__ == '__main__':
    unittest.main()
