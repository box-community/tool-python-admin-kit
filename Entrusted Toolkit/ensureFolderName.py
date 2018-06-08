import sys
from boxsdk import JWTAuth, Client
from argparse import ArgumentParser
from common import authenticate_as_user, walk_folder_tree, folder_str

## Parse command line arguments.
parser = ArgumentParser(description="Given a Box folder ID and some prefix, ensure that the prefix is prepended to the name of the folder and every subfolder.")
parser.add_argument("-f", "--folder", dest="folder", required=True, help="ID of top-level Box folder", metavar="FOLDER_ID")
parser.add_argument("-u", "--user",   dest="user",   required=True, help="ID of the user that owns or has write permissions on the folder", metavar="USER_ID")
parser.add_argument("-p", "--prefix", dest="prefix", required=True, help="the string prefix ", metavar="PREFIX")
parser.add_argument("-c", "--config", dest="config", required=True, help="path to the JSON file containing your JWT authorization configuration. For formatting information, see: https://developer.box.com/docs/setting-up-a-jwt-app#section-use-an-application-config-file", metavar="PATH")
args = parser.parse_args()

def ensure_name_starts_with(client, prefix, verbose=False):
    """
    Given a client and prefix, returns a function that takes a folder and updates its name to match the prefix.
    """
    def action(folder):
        if (folder.name.startswith(prefix)): return
        new_name = f"{prefix} {folder.name}"
        if (verbose): 
            print(f"Rename  {folder_str(folder)} => {new_name}")
        client.folder(folder_id=folder.id).rename(new_name)
    return action

# Authenticate and get client instance
client = authenticate_as_user(args.config, args.user)

# Get the folder for the given folder ID. This is where we will start our walk.
root = client.folder(folder_id=args.folder).get()
print(f"Walking {folder_str(root)}")

# Walk the folder tree, renaming each folder as necessary.
folder_action = ensure_name_starts_with(client, args.prefix, True)
walk_folder_tree(client, root, folder_action)