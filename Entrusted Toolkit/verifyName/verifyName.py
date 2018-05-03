import json
from datetime import datetime

from boxsdk.exception import BoxAPIException

from auth import box, config

# Verifies a folder has a given prefix

prefix_list = ["(Box Entrusted)", "{Box Entrusted}", "[Box Entrusted]"]


def pretty_print(folder_path, nest_level):
    string = ''
    for i in range(0, nest_level):
        string += ' '
    return string + "/" + folder_path


def rename(folder, word, nestLevel):
    new_word = ""
    if folder.name:
        if folder.name[0:15] not in prefix_list:
            new_word = word + "/" + folder.name
            print (pretty_print(str(word + "/" + folder.name), nestLevel))
            f.write(pretty_print(str(word + "/" + folder.name), nestLevel) + "\n")
        else:
            new_word = word + "/" + folder.name
    return new_word


def get_subfiles(folder):
    request = client.make_request(
        "GET",
        client.get_url('folders', folder["id"], "items")
    )
    items = json.loads(request.content)
    offset = 0
    contents = []
    while offset < items["total_count"]:
        contents.append(folder.get_items(limit=items["limit"], offset=offset))  # get the items from inside
        offset += items["limit"]
    return contents


def recurse(folderId, path, nestLevel):
    folders = filter(lambda x: x.type == "folder",
                     [item for sublist in get_subfiles(client.folder(folder_id=folderId).get()) for item in sublist])
    for folder in folders:
        try:
            new_path = rename(folder, path, nestLevel)
            recurse(folder.id, new_path, nestLevel + 1)  # recursion
        except BoxAPIException as err:
            if err.status == 404:  # the item was not a folder
                pass
            else:
                raise


if __name__ == "__main__":
    client = box.box_user(userId=config.user_id)

    time = (datetime.now().strftime("_%m-%d-%Y"))
    filename = "VerifiedNames" + time + ".txt"
    f = open(filename, "a+")

    root = client.folder(folder_id=config.base_folder_id).get()
    print (root.name)
    recurse(root.id, root.name, 0)
    f.close()
