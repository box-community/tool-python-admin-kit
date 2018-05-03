from __future__ import print_function
import csv
import json

import os

from auth import box, config

# This script takes *the_folder* and generates shared links with the privileges of *access_type*
# To do this it downloads the file to a temp directory, gets the information it needs, and removes it

the_folder = config.base_folder_id

access_type = "company"


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


if __name__ == "__main__":
    client = box.box_user()

    files = filter(lambda x: x.type == "file",
                   [item for sublist in get_subfiles(client.folder(the_folder).get()) for item in sublist])

    with open("output/shared_links.csv", 'wb') as shared_links:
        myFields = ["user", "shared_link", "num_files"]
        writer = csv.DictWriter(shared_links, fieldnames=myFields)
        writer.writeheader()
        for item in files:
            f = open("temp/" + item.name, "wb")
            item.download_to(f)
            f.close()
            try:
                with open("temp/" + item.name, 'rb') as csvfile:
                    items = csv.reader(csvfile, delimiter=' ', quotechar='|')
                    n = sum(1 for line in items)
                    print(item.name, str(n - 1))
                writer.writerow(
                    {
                        myFields[0]: str(item.name),
                        myFields[1]: "=HYPERLINK(\"" + client.file(item.id).get_shared_link(access=access_type) + "\")",
                        myFields[2]: str(n - 1)
                    }
                )
            except:
                print(item.name + " may not be csv format")
            os.remove("temp/" + item.name)
