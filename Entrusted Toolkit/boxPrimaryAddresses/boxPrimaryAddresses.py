# Configure the Authentication and the file to run this on. This currently assumes all users have a Box account
from __future__ import print_function
from auth import box

# boxPrimaryAddresses returns a login email address for a list of usernames

names_file = "names.txt"  # configure this line


def primary(client):
    with open(names_file, "r") as f:
        content = f.read().splitlines()

    for line in content:
        user = line.replace(" ", "")  # gets rid of any spaces if the user entered theirs with a space at the end
        box_users = client.users(filter_term=user + "@")
        try:
            first_user = box_users[0]
            print(first_user.login)
        except:
            print(line + " has no box account")


# -----runner------
if __name__ == "__main__":
    client = box.box_access_token()
    primary(client)
