import Processing
from Constants import *
import logging
import unittest

logging.basicConfig(format='%(asctime)s %(process)d-%(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


# ASSUME: test cases are dependent on the test files of users and group and they are not changed
class PosRestTests(unittest.TestCase):
    def testEmptyFilePath(self):  # testing user file not provided case
        with self.assertRaises(SystemExit) as e:
            Processing.initiatePaths("", TEST_GROUP_LIST_FILE_PATH, logging)
            self.assertEqual(e.exception.code, 1)

    def testEmptyFilePath2(self):  # testing group file not provided case
        with self.assertRaises(SystemExit) as e:
            Processing.initiatePaths(TEST_USER_LIST_FILE_PATH, "", logging)
            self.assertEqual(e.exception.code, 1)

    def testUsersNeg(self):  # testing getUsers() when user file not available
        Processing.initiatePaths("/t/t", TEST_GROUP_LIST_FILE_PATH, logging)
        data = Processing.getUsers(logging.info)  # testing else case in getUsers()
        self.assertEqual(data[STATUS_KEY], CONFLICT_ERROR_CODE)
        self.assertEqual(type(data), dict, "Correct data type is not obtained")

    def testUserPos(self):  # testing getUsers()
        Processing.initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logging)  # testing if case
        data = Processing.getUsers(logging.info)
        self.assertEqual(type(data), list, "Correct data type are not obtained")
        with open(TEST_USER_LIST_FILE_PATH) as f:
            tot = sum(1 for _ in f)
            self.assertEqual(len(data), tot,
                             "Error processing user list from {}.".format(TEST_USER_LIST_FILE_PATH) +
                             "{} users data is processed instead of {}".format(len(data), tot))

    def testUserByUidPos(self):  # testing a pos user callup by uid
        Processing.initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logging)
        user_id = '104'
        data = Processing.getUserByUserId(user_id, logging.info)
        self.assertEqual(data[USER_ID_KEY], user_id, "Correct details are not obtained")
        self.assertEqual(type(data), dict, "Correct data type are not obtained")

    def testUserByUidNeg(self):  # testing unavailable user callup by uid
        Processing.initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logging)
        user_id = '500'
        data = Processing.getUserByUserId(user_id, logging.info)
        self.assertEqual(type(data), dict, "Correct data type are not obtained")
        self.assertEqual(data[STATUS_KEY], NOT_FOUND_CODE, "Details should not be available")

    def testUserQuery1(self):  # testing available user callup by query
        Processing.initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logging)
        user_id = '104'
        data = Processing.getUsersMatch({USER_ID_KEY: [user_id]}, logging.info)
        self.assertEqual(len(data), 1, "Only one detail should be obtained")
        self.assertEqual(data[0][USER_ID_KEY], user_id, "Correct details are not obtained")
        self.assertEqual(type(data), list, "Wrong type of data is obtained")

    def testUserQuery2(self):  # testing unavailable user callup by query
        Processing.initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logging)
        user_id = '500'
        data = Processing.getUsersMatch({USER_ID_KEY: [user_id]}, logging.info)
        self.assertEqual(len(data), 0, "User details should not be obtained")
        self.assertEqual(type(data), list, "Wrong type of data is obtained")

    def testUserQuery3(self):  # testing available user callup by query
        Processing.initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logging)
        home = '/var/lib/gnats'  # ASSUME: test data does not change
        data = Processing.getUsersMatch({HOME_PATH_KEY: [home]}, logging.info)
        self.assertEqual(len(data), 1, "Only user data should be obtained")
        self.assertEqual(data[0][USER_NAME_KEY], 'gnats', "Wrong user data obtained")
        self.assertEqual(type(data), list, "Wrong type of data is obtained")

    def testGroupsNeg(self):  # testing groups list callup if file not present
        Processing.initiatePaths(TEST_USER_LIST_FILE_PATH, "/t/t", logging)
        data = Processing.getGroups(logging.info)  # testing else case in getGroups()
        self.assertEqual(data[STATUS_KEY], CONFLICT_ERROR_CODE)
        self.assertEqual(type(data), dict, "Wrong type of data is obtained")

    def testGroupsPos(self):  # testing getGroups()
        Processing.initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logging)  # testing if case
        data = Processing.getGroups(logging.info)
        with open(TEST_GROUP_LIST_FILE_PATH) as f:
            tot = sum(1 for _ in f)
            self.assertEqual(len(data), tot,
                             "Error processing user list from {}.".format(TEST_GROUP_LIST_FILE_PATH) +
                             "{} users data is processed instead of {}".format(len(data), tot))
        self.assertEqual(type(data), list, "Wrong type of data is obtained")

    def testGroupsByUid(self):  # testing groups for an available user
        Processing.initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logging)
        user_id = '7'
        team_count = 4
        data = Processing.getGroupsByUserId(user_id, logging.info)
        self.assertEqual(len(data), team_count, "Correct details are not obtained")
        self.assertEqual(type(data), list, "Wrong type of data is obtained")

    def testGroupsByUidNeg(self):  # testing groups for an unavailable user
        Processing.initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logging)
        user_id = '500'
        data = Processing.getGroupsByUserId(user_id, logging.info)
        self.assertEqual(data[STATUS_KEY], NOT_FOUND_CODE, "user details should not be obtained")
        self.assertEqual(type(data), dict, "Wrong type of data is obtained")

    def testGroupByGid(self):  # testing group by available gid
        Processing.initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logging)
        group_id = '104'
        data = Processing.getGroupsByGroupId(group_id, logging.info)
        self.assertEqual(data[GROUP_ID_KEY], group_id, "Correct details are not obtained")
        self.assertEqual(type(data), dict, "Wrong type of data is obtained")

    def testGroupByGidNeg(self):  # testing group by unavailable gid
        Processing.initiatePaths(TEST_USER_LIST_FILE_PATH, TEST_GROUP_LIST_FILE_PATH, logging)
        group_id = '500'
        data = Processing.getGroupsByGroupId(group_id, logging.info)
        self.assertEqual(data[STATUS_KEY], NOT_FOUND_CODE, "group details should not be obtained")
        self.assertEqual(type(data), dict, "Wrong type of data is obtained")

    def testGroupQuery1(self):  # testing group callup by query
        member2 = 'lp'
        member3 = 'syslog'
        data = Processing.getGroupsMatch({GROUP_MEMBER_KEY: [member3, member2]}, logging.info)
        self.assertEqual(type(data), list, "Wrong type of data is obtained")
        self.assertEqual(len(data), 0, "No group data should be obtained")

    def testGroupQuery2(self):  # testing group callup by query
        member2 = 'lp'
        member3 = 'landscape'
        data = Processing.getGroupsMatch({GROUP_MEMBER_KEY: [member3, member2]}, logging.info)
        self.assertEqual(type(data), list, "Wrong type of data is obtained")
        self.assertEqual(len(data), 2, "2 groups data should be obtained")

    def testGroupQuery3(self):  # testing group callup by query
        group_id = '104'
        data = Processing.getGroupsMatch({GROUP_ID_KEY: [group_id]}, logging.info)
        self.assertEqual(len(data), 1, "1 group data should be obtained")
        self.assertEqual(type(data), list, "Wrong type of data is obtained")
        self.assertEqual(data[0][GROUP_ID_KEY], group_id, "Wrong group details obtained")


if __name__ == '__main__':
    unittest.main()
