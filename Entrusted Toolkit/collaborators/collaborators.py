from __future__ import print_function
from __future__ import print_function
import json

from boxsdk.exception import BoxAPIException

from auth import box, config
import Collab

# This script prints folder names and any new collaborators at that given level
# Set the folder to run this on in auth/config.py

client = box.box_user(userId=config.user_id)
base_folder = config.base_folder_id


def collaborators():
    root = client.folder(folder_id=base_folder).get()
    root_collab = Collab.Collab(root, None, [])
    print(root.name)
    recurse(root_collab, 0)


# finds new folders and looks at their collaborators
def recurse(current_collab, nest_level):
    contents = get_subfolders(current_collab)
    folders = filter(lambda x: x.type == "folder", [item for sublist in contents for item in sublist])
    for folder in folders:
        try:
            newFolder = Collab.Collab(folder, current_collab, find_collaborators(folder, current_collab, nest_level))
            recurse(newFolder, nest_level + 1)
        except BoxAPIException as err:
            if err.status == 404:  # the item was not a folder
                pass
            else:
                raise


# helper function to return a list of subfolders of a given Collab
def get_subfolders(current_collab):
    current_folder = current_collab.folder
    request = client.make_request(
        "GET",
        client.get_url('folders', current_folder.id, "items")
    )
    body = request.content
    items = json.loads(body)
    offset = 0
    total_count = items["total_count"]
    contents = []
    while offset < total_count:
        contents.append(current_folder.get_items(limit=items["limit"], offset=offset))  # get the items from inside
        offset += items["limit"]
    return contents


# Returns a list of collaborators
def find_collaborators(folder, parent, nest_level):
    request = client.make_request(
        "GET",
        client.get_url('folders', folder.id, "collaborations")
    )
    body = request.content
    items = json.loads(body)
    collaboratorsList = get_collaborators(folder, parent, nest_level, items)
    return collaboratorsList


# returns a list of collaborators
def get_collaborators(folder, parent, nest_level, items):
    collaboratorsList = []
    new_collaborators = []
    for item in items["entries"]:
        collaboratorsList.append(item["accessible_by"]["name"])
        new_collaborators.append(get_new_collaborators(parent, nest_level, item))
    if None not in new_collaborators:
        print_new_collaborators(new_collaborators, folder, nest_level)

    return collaboratorsList


# returns if collaborators are new compared to their parent
def get_new_collaborators(parent, nest_level, item):
    if item["accessible_by"]["name"] not in parent.collaborations:
        return pretty_print(
            str(item["accessible_by"]["name"] + " role: " + item["role"]),
            nest_level,
            False
        )


# prints collaborators when there are new ones to be printed
def print_new_collaborators(new_collaborators, folder, nest_level):
    if new_collaborators:
        print(pretty_print("#### NEW COLLABORATIONS ####", nest_level, False))
        print(pretty_print(str(folder.name + " [Folder ID: " + folder.id + "]"), nest_level, True))
        for new_collaborator in new_collaborators:
            print(new_collaborator)


def pretty_print(folder_name, nest_level, slash):
    string = ''
    for i in xrange(0, nest_level):
        string += ' '
    if slash:
        return string + "/" + folder_name
    else:
        return string + folder_name


if __name__ == "__main__":
    collaborators()
