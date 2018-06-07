import sys
from boxsdk import JWTAuth, Client
from argparse import ArgumentParser

## Parse command line arguments.
parser = ArgumentParser(description="Given a Box folder ID and some prefix, ensure that the prefix is prepended to the name of the folder and every subfolder.")
parser.add_argument("-f", "--folder", dest="folder", required=True, help="ID of top-level Box folder", metavar="FOLDER_ID")
parser.add_argument("-u", "--user",   dest="user",   required=True, help="ID of the user that owns or has write permissions on the folder", metavar="USER_ID")
parser.add_argument("-p", "--prefix", dest="prefix", required=True, help="the string prefix ", metavar="PREFIX")
parser.add_argument("-c", "--config", dest="config", required=True, help="path to the JSON file containing your JWT authorization configuration. For formatting information, see: https://developer.box.com/docs/setting-up-a-jwt-app#section-use-an-application-config-file", metavar="PATH")
args = parser.parse_args()

def authenticate_as_user(config, user):
    """
    Using the JWT auth configuration file, get an authenticated client that can act as the specified user. 
    """
    auth = JWTAuth.from_settings_file(args.config)
    print ("Authenticating...")
    auth.authenticate_user(args.user)
    client = Client(auth)
    me = client.user().get()
    print (f"Authenticated as {me.name} ({me.login}).")
    return client

def is_folder(item):
    """
    Check the item's 'type' to determine whether it's a folder.
    """
    return item['type'] == "folder"

def get_subfolders(client, folder):
    """
    Fetch all subfolders of a given folder
    """
    offset = 0
    lastFetchedCount = -1
    result = []
    while (lastFetchedCount != 0):
        # fetch folder items and add subfolders to list
        items = client.folder(folder_id=folder['id']).get_items(limit=1000, offset=offset)
        result.extend(filter(is_folder, items))
        # update offset and counts for terminating conditions.
        offset += len(items)
        lastFetchedCount = len(items)
    return result

def walk_folder_tree(client, folder, folder_action):
    """
    Ensure this folder is appropriately named, then recurse to every subfolder.  
    """
    folder_action(folder)
    for subfolder in get_subfolders(client, folder):
        walk_folder_tree(client, subfolder, folder_action)

def ensure_name_starts_with(client, prefix):
    """
    Given a client and prefix, returns a function that takes a folder and updates its name to match the prefix.
    """
    def action(folder):
        if (folder.name.startswith(prefix) == False):
            new_name = prefix + " " + folder.name
            print(f"Renaming '{folder.name}' ({folder.id}) as '{new_name}''")
            client.folder(folder_id=folder.id).rename(new_name)
    return action

## Authenticate and get client instance
client = authenticate_as_user(args.config, args.user)
# Get the folder for the ID provided by the user. This is where we will start our walk.
root = client.folder(folder_id=args.folder).get()
# Walk the folder tree, renaming each folder as necessary.
print(f"Starting folder walk in '{root.name}' ({root.id})...")
folder_action = ensure_name_starts_with(client, args.prefix)
walk_folder_tree(client, root, folder_action)
print("Done!")