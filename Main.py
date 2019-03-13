from sanic import Sanic
from sanic.response import json
from sanic.log import logger
from Processing import *
import argparse

app = Sanic()


@app.route("/")
async def test(request):
    return json({"hello": "world"})


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
    initiatePaths(args.user_path, args.group_path, logger)
    app.run(host=args.host, port=args.port, debug=ENABLE_DEBUG)
