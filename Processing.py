from Constants import *
from Data import User, Group
import os

user_list_path = None
group_list_path = None
logger = None


def initiatePaths(up, gp, l):
    global user_list_path, group_list_path, logger
    user_list_path = up
    group_list_path = gp
    logger = l  # ASSUME: logger is valid
    if not user_list_path:
        logger.error("User list path is not defined")
        exit(1)
    if not group_list_path:
        logger.error("Group list path is not defined")
        exit(1)


def getUsers():
    if os.path.isfile(user_list_path):
        ret = []
        with open(user_list_path) as f:
            for user in f:
                ret.append(User(user.split(":")).getUserData())
        logger.debug("List of users is extracted")
        return ret
    else:
        return {MESSAGE_KEY: "User File is not available at {}".format(user_list_path), STATUS_KEY: 409}


def getUserByUserId(uid):  # uid is unique
    user = getUsersMatch({USER_ID_KEY: uid})
    if STATUS_KEY in user or not user:
        return {MESSAGE_KEY: "User Id {} Not found".format(uid), STATUS_KEY: 404}
    return user[0]


def getUsersMatch(args):
    users = getUsers()
    if STATUS_KEY in users:
        return {MESSAGE_KEY: "Error getting users list-{}".format(users[MESSAGE_KEY]), STATUS_KEY: users[STATUS_KEY]}
    ret = []
    for user in users:
        add = True
        for k in args.keys():
            if args[k] != user[k]:
                add = False
                break
        if add:
            ret.append(user)
    return ret


def getGroups():
    if os.path.isfile(group_list_path):
        ret = []
        with open(group_list_path) as f:
            for group in f:
                ret.append(Group(group.split(":")).getGroupData())
        logger.debug("List of Groups is extracted")
        return ret
    else:
        return {MESSAGE_KEY: "Group list file is not available at {}".format(group_list_path), STATUS_KEY: 409}


def gerGroupsByUserId(uid):
    user = getUserByUserId(uid)
    if USER_NAME_KEY not in user:
        return {MESSAGE_KEY: "Error getting User-{}".format(user[MESSAGE_KEY]), STATUS_KEY: user[STATUS_KEY]}
    groups = getGroups()
    if STATUS_KEY in groups:
        return {MESSAGE_KEY: "Error getting groups list-{}".format(groups[MESSAGE_KEY]), STATUS_KEY: groups[STATUS_KEY]}
    ret = []
    user_name = user[USER_NAME_KEY]
    for g in groups:
        if user_name in g[GROUP_LIST_KEY]:
            ret.append(g)
    return ret


def getGroupsMatch(args):
    groups = getGroups()
    if STATUS_KEY in groups:
        return {MESSAGE_KEY: "Error getting groups list-{}".format(groups[MESSAGE_KEY]), STATUS_KEY: groups[STATUS_KEY]}
    ret = []
    for g in groups:
        add = True
        for k in args.keys():
            if args[k] != g[k]:
                add = False
                break
        if add:
            ret.append(g)
    return ret


def getGroupsByGroupId(gid):  # ASSUME: gid is unique
    group = getGroupsMatch({GROUP_ID_KEY: gid})
    if STATUS_KEY in group or not group:
        return {MESSAGE_KEY: "Group {} not found".format(gid), STATUS_KEY: 404}
    return group[0]
