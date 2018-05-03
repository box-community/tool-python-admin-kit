#!/usr/bin/python

import getopt
from boxsdk.exception import BoxAPIException
import sys
from auth import box


# prints folders of a user
# Sample: printUserFolders.py -u <account num> -f <folder num>

def prettyPrint(folderName, nestLevel):
    for i in range(0, nestLevel):
        sys.stdout.write(' ')
    print("/" + folderName)


def recurse(folderId, nestLevel):
    contents = client.folder(folder_id=folderId).get_items(limit=1000, offset=0)
    folders = filter(lambda x: x.type == "folder", contents)
    for folder in folders:
        try:
            prettyPrint(folder.name, nestLevel)
            recurse(folder.id, nestLevel + 1)  # recursion
        except BoxAPIException as err:
            if err.status == 404:  # the item was not a folder
                pass
            else:
                raise


def printUserFolders(argv):
    global client
    try:
        opts, args = getopt.getopt(argv, "u:f:ha", ["accountNum=", "folderNum=", "help"])
    except getopt.GetoptError as err:
        print(str(err))
        # print ("printUserFolders.py -u <accountNum> -f <folderNum>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print(
                """Usage: printUserFolders.py -u <accountNum> -f <folderNum>
            
Options:
    -h|--help\t\t\t\tShow Help information
    -u|--accountNum|-a\t\tSpecify the Box Account Number
    -f|--folderNum\t\t\tSpecify the box folder id\n\n""")
        elif opt in ('-u', '--accountNum', '-a'):
            userID = arg
            client = box.box_user(userID)
            # print (opts)
            # if '-f' not in opts:
            #     print("Usage:\tprintUserFolders.py -u <accountNum> -f <folderNum>")
            #     print("Please include folder number")
            #     sys.exit(2)
        elif opt in ('-f', '--folderNum'):
            if client != "":
                root = client.folder(folder_id=arg).get()
                print(root.name)
                recurse(arg, 0)

            else:
                print("Usage:\tprintUserFolders.py -u <accountNum> -f <folderNum>")
                print("Please include account number")
                sys.exit(2)
        else:
            print("Usage:\tprintUserFolders.py -u <accountNum> -f <folderNum>")
            sys.exit(2)


if __name__ == "__main__":
    printUserFolders(sys.argv[1:])
