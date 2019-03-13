from sanic import Sanic
from sanic.response import json
from sanic.log import logger
from Processing import *
import argparse

app = Sanic()
inner_log = logger.debug


@app.route("/")
async def home(req):
    return json({"Message": "Welcome to PAAS (Passwd As A Service). Refer the documentation at "
                            "\'https://github.com/glkc/PAS\' for directions."})


@app.route("/users")
async def getUsersList(req):
    logger.info("Requesting users list")
    return returnData(getUsers(inner_log))
    # returning the response as json instead of html beautification


@app.route("/users/query")
async def getUsersMatchList(req):
    conditions = req.args
    logger.info("Requesting user list with requirements - {}".format(conditions))
    for key in conditions.keys():
        if key not in USER_KEYS:
            return json({MESSAGE_KEY: "Invalid key {} for user condition".format(key)}, status=CONFLICT_ERROR_CODE)
    return returnData(getUsersMatch(conditions, inner_log))


@app.route("/users/<uid>")
async def getUserById(req, uid):
    logger.info("Requesting details of user id - {}".format(uid))
    return returnData(getUserByUserId(uid, inner_log))


@app.route("users/<uid>/groups")
async def getGroupsListByUserId(req, uid):
    logger.info("Requesting List of groups with user {} as a member".format(uid))
    return returnData(getGroupsByUserId(uid, inner_log))


@app.route("/groups")
async def getGroupsList(req):
    logger.info("Requesting list of groups")
    return returnData(getGroups(inner_log))


@app.route("/groups/query")
async def getGroupsMatchList(req):
    conditions = req.args
    logger.info("Requesting group list with requirements - {}".format(conditions))
    for key in conditions.keys():
        if key not in GROUP_KEYS:
            return json({MESSAGE_KEY: "Invalid key {} for group condition".format(key)}, status=CONFLICT_ERROR_CODE)
    return returnData(getGroupsMatch(conditions, inner_log))


@app.route("/groups/<gid>")
async def getGroupById(req, gid):
    logger.info("Requesting details of the group id - {}".format(gid))
    return returnData(getGroupsByGroupId(gid, inner_log))


def returnData(ret):
    if STATUS_KEY in ret:
        logger.warn("Error obtaining data")
        return json({MESSAGE_KEY: ret[MESSAGE_KEY]}, status=ret[STATUS_KEY])
    return json(ret)


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host address to which the service is exposed (Default-{})'.format(HOST_ADDRESS),
                        default=HOST_ADDRESS)
    parser.add_argument('--port',
                        help='Port address on which the service is exposed on the host (Default-{})'.format(HOST_PORT),
                        default=HOST_PORT)
    parser.add_argument('--user_path',
                        help='Path to file location containing users list (Default-{})'.format(USER_LIST_FILE_PATH),
                        default=USER_LIST_FILE_PATH)
    parser.add_argument('--group_path',
                        help='Path to file location containing groups data (Default-{})'.format(GROUP_LIST_FILE_PATH),
                        default=GROUP_LIST_FILE_PATH)
    p_args = parser.parse_args()
    if p_args.host != HOST_ADDRESS:  # ASSUME: user provides the input correctly in format
        logger.debug("Overriding default host address {} with user input {}".format(HOST_ADDRESS, p_args.host))
    if p_args.port != HOST_PORT:  # ASSUME: user provides the input correctly in format
        logger.debug("Overriding default port {} with user input {}".format(HOST_PORT, p_args.port))
    if p_args.user_path != USER_LIST_FILE_PATH:  # ASSUME: user provides the input correctly in format
        logger.debug("Overriding default path to user list {} with user input {}".format(USER_LIST_FILE_PATH,
                                                                                         p_args.user_path))
    if p_args.group_path != GROUP_LIST_FILE_PATH:  # ASSUME: user provides the input correctly in format
        logger.debug("Overriding default path to group list {} with user input {}".format(GROUP_LIST_FILE_PATH,
                                                                                          p_args.group_path))
    return p_args


if __name__ == "__main__":
    args = getArgs()
    initiatePaths(args.user_path, args.group_path, logger.error)
    app.run(host=args.host, port=args.port, debug=ENABLE_DEBUG)
