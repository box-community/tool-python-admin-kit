from boxsdk import JWTAuth, Client

## AUTHENTICATION 

def authenticate_as_user(config, user):
    """
    Using the JWT auth configuration file, get an authenticated client that can act as the specified user. 
    """
    auth = JWTAuth.from_settings_file(config)
    auth.authenticate_user(user)
    return Client(auth);

def authenticate_as_service_account(config):
    """
    Using the JWT auth configuration file, get an authenticated client that can act as the app service account. 
    """
    auth = JWTAuth.from_settings_file(config)
    auth.authenticate_instance()
    return Client(auth);


## STRING FUNCTIONS

def path_str(folder):
    """
    If 'path_collection' is present, returns the folder's full path.
    Otherwise, return the folder name.
    """
    path = ""
    if hasattr(folder, 'path_collection'):
        path = "/" + "/".join(map(lambda p: p['name'], folder.path_collection['entries'])) + "/"
    return path + folder.name

## TREE TRAVERSAL

def is_folder(item):
    """
    Check the item's 'type' to determine whether it's a folder.
    """
    return item['type'] == "folder"

def is_file(item):
    """
    Check the item's 'type' to determine whether it's a file.
    """
    return item['type'] == "file"

def do_for_folder_items(client, folder_id, fn):
    """
    Fetch all items in a given folder
    """
    offset = 0
    hasMoreItems = True
    while (hasMoreItems):
        # fetch folder items and add subfolders to list
        items = client.folder(folder_id=folder_id).get_items(limit=100, offset=offset)
        item_list = list(items)
        # pass the items to the provided function.
        fn(client, item_list)
        # update offset and counts for terminating conditions.
        offset += len(item_list)
        hasMoreItems = len(item_list) != 0

def get_subfolders(client, folder):
    """
    Fetch all subfolders of a given folder
    """
    offset = 0
    lastFetchedCount = -1
    result = []
    while (lastFetchedCount != 0):
        # fetch folder items and add subfolders to list
        items = client.folder(folder_id=folder['id']).get_items(limit=1000, offset=offset, fields=["id", "name","path_collection"])
        result.extend(filter(is_folder, items))
        # update offset and counts for terminating conditions.
        offset += len(items)
        lastFetchedCount = len(items)
    return result

def walk_folder_tree(client, folder, folder_action):
    """
    Perform some folder_action against a folder, then do the same for every subfolder.
    """
    folder_action(folder)
    for subfolder in get_subfolders(client, folder):
        walk_folder_tree(client, subfolder, folder_action)