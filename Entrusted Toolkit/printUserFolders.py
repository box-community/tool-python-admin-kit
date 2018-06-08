import sys
from argparse import ArgumentParser
from common import authenticate_as_user, walk_folder_tree, path_str

## Parse command line arguments.
parser = ArgumentParser(description="Given a Box folder ID, log the ID and path of that folder and every subfolder.")
parser.add_argument("-f", "--folder", dest="folder", required=True, help="ID of top-level Box folder", metavar="FOLDER_ID")
parser.add_argument("-u", "--user",   dest="user",   required=True, help="ID of the user that owns or has write permissions on the folder", metavar="USER_ID")
parser.add_argument("-c", "--config", dest="config", required=True, help="path to the JSON file containing your JWT authorization configuration. For formatting information, see: https://developer.box.com/docs/setting-up-a-jwt-app#section-use-an-application-config-file", metavar="PATH")
args = parser.parse_args()

def print_path(folder):
    """
    Given a folder, log the full path.
    """
    print(f"{folder.id}, {path_str(folder)}")

# Authenticate and get client instance
client = authenticate_as_user(args.config, args.user)

print("FolderId, FolderPath")
# Get the folder for the given folder ID. This is where we will start our walk.
root = client.folder(folder_id=args.folder).get()
# Walk the folder tree, print the path of each folder.
walk_folder_tree(client, root, print_path)