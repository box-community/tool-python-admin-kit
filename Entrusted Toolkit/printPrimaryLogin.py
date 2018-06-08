import sys
import multiprocessing
from joblib import Parallel, delayed
from argparse import ArgumentParser
from common import authenticate_as_service_account, walk_folder_tree, path_str

## Parse command line arguments.
parser = ArgumentParser(description="Given a list of Box usernames, find the primary login / email address.")
parser.add_argument("-f", "--file", dest="file", required=True, help="path to the file containing the usernames to look up, one per line.", metavar="PATH")
parser.add_argument("-c", "--config", dest="config", required=True, help="path to the JSON file containing your JWT authorization configuration. For formatting information, see: https://developer.box.com/docs/setting-up-a-jwt-app#section-use-an-application-config-file", metavar="PATH")
args = parser.parse_args()

def print_primary_login(username):
    """
    Given a username, find the associated Box user and, if found, print the primary login.
    """
    users = client.users(filter_term=username.strip() + "@")
    primary_login = users[0]['login'] if len(users) > 0 else "(user not found)"
    print(f"{username}, {primary_login}")

# Get an authenticated Box client with enterprise privileges
client = authenticate_as_service_account(args.config)

# Fetch the usernames from the provided file
with open(args.file, "r") as f:
    content = f.read().splitlines()

# Iterate over the usernames and print the primary login
print ("Username, PrimaryLogin")
Parallel(n_jobs=-1)(delayed(print_primary_login)(username) for username in content)