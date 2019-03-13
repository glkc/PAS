# PAAS

## Description
PAAS also known as Passwd As A Service, exposes the user and group information on a UNIX-like system.

## Requirements
* Python 3
* [sanic](https://sanic.readthedocs.io/en/latest/sanic/getting_started.html#install-sanic)
* aiohttp (for unit testing)
 
## Instructions
* Parameters Host and Port on which the service to be accessible can be set via runtime variable as mentioned below.
* Locations to files of passwd and groups can also be set during runtime
* Certain assumptions are taken while implementing this library. Some of them are
    * The format of data stored in the files is same as that of in UNIX systems
    * read permission is available to the program
 
```
usage: python Main.py [-h] [--host HOST] [--port PORT] [--user_path USER_PATH]
               [--group_path GROUP_PATH]

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           Host address to which the service is exposed
                        (Default-127.0.0.1)
  --port PORT           Port address on which the service is exposed on the
                        host (Default-4589)
  --user_path USER_PATH
                        Path to file location containing users list
                        (Default-/etc/passwd)
  --group_path GROUP_PATH
                        Path to file location containing groups data
                        (Default-/etc/groups)
```
## Routes
Data from the files can be accessed via the following routes on address http://HOST:PORT/
* GET /users 
    * Returns the list of all users on the system, as defined in the `passwd` OR `user` file.
* GET /users/query[?name=<>][&uid=<>][&gid=<>][&comment=<>][&home=<>][&shell=<>]
    * Returns the list of users matching all of the specified query fields. 
    * The bracket notation indicates that any of the following query parameters may be supplied:
        - name
        - uid
        - gid
        - comment
        - home
        - shell
    * Only exact matches are supported.
    * if no query provided, then all users data is returned
* GET /users/\<uid>
    * Returns a single user data with given \<uid>. 
    * Returns 404 if given \<uid> is not found.
* GET /users/\<uid>/groups
    * Returns all the groups for which the given user \<uid> is a member.
* GET /groups
    * Returns the list of all groups on the system, as defined by `groups` file.
* GET /groups/\<gid>
    * Returns a single group with \<gid>. 
    * Returns 404 if \<gid> is not found.
* GET /groups/query[?name=\<nq>][&gid=\<gq>][&member=\<mq1>[&member=\<mq2>][&...]]
    * Returns a list of groups matching all of the specified query fields. 
    * The bracket notation indicates that any of the following query parameters may be supplied:
        - name
        - gid
        - member (repeated)
    * Any group containing all the specified members is returned, i.e. when query members are a subset of group members.

## Unit Tests
Unit tests are written for certain scenarios and it can be running the file Test.py
```
> python Test.py 
```