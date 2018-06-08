import sys
from argparse import ArgumentParser
from common import authenticate_as_user, walk_folder_tree, path_str

## Parse command line arguments.
parser = ArgumentParser(description="Given a Box folder ID and some list of prefix, print the path of any subfolder whose name does not start with one of the prefixes.")
parser.add_argument("-f", "--folder", dest="folder",     required=True, help="ID of top-level Box folder", metavar="FOLDER_ID")
parser.add_argument("-u", "--user",   dest="user",       required=True, help="ID of the user that owns or has write permissions on the folder", metavar="USER_ID")
parser.add_argument("-p", "--prefixes", dest="prefixes", required=True, nargs='+', help="The acceptable folder name prefixes", metavar="PREFIX")
parser.add_argument("-c", "--config", dest="config",     required=True, help="path to the JSON file containing your JWT authorization configuration. For formatting information, see: https://developer.box.com/docs/setting-up-a-jwt-app#section-use-an-application-config-file", metavar="PATH")
args = parser.parse_args()

def audit_name_starts_with(prefixes):
    """
    Given a list of prefixes, returns a function that takes a folder and prints the folder path if the folder name does not start with one of the prefixes.
    """
    def action(folder):
        if any(folder.name.startswith(prefix) for prefix in prefixes) == False:
            print(f"{folder.id}, {path_str(folder)}")
    return action

# Authenticate and get client instance
client = authenticate_as_user(args.config, args.user)

print("FolderId, FolderPath")
# Get the folder for the given folder ID. This is where we will start our walk.
root = client.folder(folder_id=args.folder).get()
# Walk the folder tree, print the path of each folder.
walk_folder_tree(client, root, audit_name_starts_with(args.prefixes))