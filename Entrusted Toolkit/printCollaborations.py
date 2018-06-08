import sys
import json
from pprint import pprint
from argparse import ArgumentParser
from common import authenticate_as_user, walk_folder_tree, path_str

## Parse command line arguments.
parser = ArgumentParser(description="Given a Box folder ID, print information about accepted collaborations originating in that folder and all subfolders.")
parser.add_argument("-f", "--folder", dest="folder", required=True, help="ID of top-level Box folder", metavar="FOLDER_ID")
parser.add_argument("-u", "--user",   dest="user",   required=True, help="ID of the user that owns or has write permissions on the folder", metavar="USER_ID")
parser.add_argument("-c", "--config", dest="config", required=True, help="path to the JSON file containing your JWT authorization configuration. For formatting information, see: https://developer.box.com/docs/setting-up-a-jwt-app#section-use-an-application-config-file", metavar="PATH")
args = parser.parse_args()

def get_collabs(client, folder):
    """
    Fetch this folder's collaborations from Box
    """
    url = client.get_url('folders', folder.id, "collaborations")
    request = client.make_request("GET", url)
    return json.loads(request.content)['entries']

def print_original_collabs(client):
    """
    Given a client, returns a function that takes a folder and prints out any accepted collaborations that originate in that folder.
    """
    def action(folder):
        # The collaboration originated in this folder (i.e. is not inherited from a parent folder)
        def is_original(collab): return collab['item']['id'] == folder.id
        # The collaboration has been accepted by the collaborator
        def is_accepted(collab): return collab['status'] != 'pending'
        # A tuple containing info on the folder, collaboration, collaborator, and creator    
        def collab_info(collab): 
            collaborator = collab['accessible_by']
            creator = collab['created_by'] 
            return (folder.id, f'"{path_str(folder)}"', 
                    collab['id'], collab['role'], collab['created_at'], 
                    collaborator['id'], f"\"{collaborator['name']}\"", collaborator['login'],
                    creator['id'], f"\"{creator['name']}\"", creator['login'])
        # Print out the info for accepted collaborations originating in this folder
        collaborations = get_collabs(client, folder)
        for c in map(collab_info, filter(is_original, filter(is_accepted, collaborations))):
            print(", ".join(c))

    return action

# Authenticate and get client instance
client = authenticate_as_user(args.config, args.user)

# Get the folder for the given folder ID. This is where we will start our walk.
root = client.folder(folder_id=args.folder).get()
# Walk the folder tree, print the path of each folder.
print("FolderId, FolderPath, CollaborationId, CollaborationRole, CollaborationCreated, CollaboratorId, CollaboratorName, CollaboratorLogin, CreatorId, CreatorName, CreatorLogin")
folder_action = print_original_collabs(client)
walk_folder_tree(client, root, folder_action)