import sys
from datetime import date, timedelta
from common import authenticate_as_service_account, is_file, do_for_folder_items
from argparse import ArgumentParser

## Parse command line arguments.
parser = ArgumentParser(description="Given a Box folder ID, create a shared link with the specified expiration (in days) for all files in the folder.")
parser.add_argument("-f", "--folder", dest="folder", required=True, help="ID of top-level Box folder", metavar="FOLDER_ID")
parser.add_argument("-e", "--expiration", dest="expiration", nargs='?', const=1, type=int, default=30, help="The shared link expiration in days (default: 30)", metavar="EXPIRATION")
parser.add_argument("-a", "--auth", dest="auth", required=True, help="path to the JSON file containing your JWT authorization configuration. For formatting information, see: https://developer.box.com/docs/setting-up-a-jwt-app#section-use-an-application-config-file", metavar="CONFIG")
args = parser.parse_args()

# Authenticate as service account and get client instance
# https://github.com/box/box-python-sdk/blob/master/docs/usage/authentication.md#server-auth-with-jwt
client = authenticate_as_service_account(args.auth)

# The expiration date for the shared link, in ISO format.
expiration = (date.today() + timedelta(days=args.expiration)).isoformat()

def create_shared_link(client, items):
    """
    Create a shared link for all 'file' items in the folder.
    """
    # Filter out any non-file items
    for item in filter(is_file, items):
        # Create a shared link with the specified expiration, 
        #   or update the existing shared link.
        url = client.file(item.id).get_shared_link(access="company", unshared_at=expiration)
        # Print CSV row
        print(f'{item.name},{url}')

# Print CSV header
print("file,link")
# Pass the client, folder id, and create_shared_link function
#   to do_for_folder_items, which will page through all the items
#   in the folder and pass each page of items to the function.
do_for_folder_items(client, args.folder, create_shared_link)
