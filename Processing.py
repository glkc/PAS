from Constants import *
from Data import User, Group
import os

user_list_path = None
group_list_path = None


def initiatePaths(up, gp, msg):
    global user_list_path, group_list_path
    user_list_path = up
    group_list_path = gp
    if not user_list_path:  # exiting the system as the files are not defined and all the operations do not work
        msg("User list path is not defined")
        exit(1)
    if not group_list_path:
        msg("Group list path is not defined")
        exit(1)


def getUsers(msg):
    if os.path.isfile(user_list_path):
        ret = []
        with open(user_list_path) as f:
            for user in f:
                ret.append(User(user.strip("\n").split(":")).getUserData())  # split string line by ':'
        msg("List of users is extracted from - {}".format(user_list_path))
        return ret
    else:
        return {MESSAGE_KEY: "User File is not available at {}".format(user_list_path), STATUS_KEY: CONFLICT_ERROR_CODE}


def getUserByUserId(uid, msg):  # ASSUME: uid is unique
    user = getUsersMatch({USER_ID_KEY: [uid]}, msg)
    if STATUS_KEY in user or not user:
        return {MESSAGE_KEY: "User Id {} Not found".format(uid), STATUS_KEY: NOT_FOUND_CODE}
    return user[0]


def getUsersMatch(args, msg):  # args is a map with key-value requirements
    users = getUsers(msg)
    if STATUS_KEY in users:
        return {MESSAGE_KEY: "Error getting users list-{}".format(users[MESSAGE_KEY]), STATUS_KEY: users[STATUS_KEY]}
    ret = []
    for user in users:
        add = True
        for k in args.keys():
            if args[k][0] != user[k]:  # checking if all the requirements match
                msg("User {} does not match the requirements at {}".format(user[USER_ID_KEY], k))
                add = False  # requirement did not match
                break
        if add:
            ret.append(user)
    return ret


def getGroups(msg):
    if os.path.isfile(group_list_path):
        ret = []
        with open(group_list_path) as f:
            for group in f:
                ret.append(Group(group.strip("\n").split(":")).getGroupData())
        msg("List of Groups is extracted from {}".format(group_list_path))
        return ret
    else:
        return {MESSAGE_KEY: "Group list file is not available at {}".format(group_list_path),
                STATUS_KEY: CONFLICT_ERROR_CODE}


def getGroupsByUserId(uid, msg):
    user = getUserByUserId(uid, msg)
    if USER_NAME_KEY not in user:
        return {MESSAGE_KEY: "Error getting User-{}".format(user[MESSAGE_KEY]), STATUS_KEY: user[STATUS_KEY]}
    groups = getGroups(msg)
    if STATUS_KEY in groups:
        return {MESSAGE_KEY: "Error getting groups list-{}".format(groups[MESSAGE_KEY]), STATUS_KEY: groups[STATUS_KEY]}
    ret = []
    user_name = user[USER_NAME_KEY]  # ASSUME: user name is unique
    msg("Getting groups with user name {} corresponding to uid {} as a member".format(user_name, uid))
    for g in groups:
        if user_name in g[GROUP_LIST_KEY]:
            msg("User {} is present in Group Id {}".format(user_name, g[GROUP_ID_KEY]))
            ret.append(g)
    return ret


def getGroupsMatch(args, msg):  # args is a map with key-value requirements
    groups = getGroups(msg)
    if STATUS_KEY in groups:
        return {MESSAGE_KEY: "Error getting groups list-{}".format(groups[MESSAGE_KEY]), STATUS_KEY: groups[STATUS_KEY]}
    ret = []
    for g in groups:
        add = True
        for k in args.keys():
            if k == GROUP_LIST_KEY:
                for user in args[k]:
                    if user not in g[k]:
                        add = False
                        break
                if not add:
                    break
            elif args[k][0] != g[k]:  # checking if all the requirements match
                msg("Group {} does not match the requirements at {}".format(g[GROUP_ID_KEY], k))
                add = False  # requirement did not match
                break
        if add:
            ret.append(g)
    return ret


def getGroupsByGroupId(gid, msg):  # ASSUME: gid is unique
    group = getGroupsMatch({GROUP_ID_KEY: [gid]}, msg)
    if STATUS_KEY in group or not group:
        return {MESSAGE_KEY: "Group {} not found".format(gid), STATUS_KEY: NOT_FOUND_CODE}
    return group[0]
