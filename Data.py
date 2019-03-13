from Constants import USER_KEYS, GROUP_KEYS, GROUP_LIST_KEY


class User:
    def __init__(self, data):
        self.user_data = {}
        for i in range(len(USER_KEYS)):
            if USER_KEYS[i]:
                self.user_data[USER_KEYS[i]] = data[i]

    def getUserData(self):
        return self.user_data


class Group:
    def __init__(self, data):
        self.group_data = {}
        for i in range(len(GROUP_KEYS)):
            if GROUP_KEYS[i]:
                self.group_data[GROUP_KEYS[i]] = data[i]
        self.group_data[GROUP_LIST_KEY] = self.group_data[GROUP_LIST_KEY].split(",")

    def getGroupData(self):
        return self.group_data

    # def isUserPresent(self, user_name):
    #     if user_name in self.group_data[GROUP_LIST_KEY]:
    #         return True
    #     return False

