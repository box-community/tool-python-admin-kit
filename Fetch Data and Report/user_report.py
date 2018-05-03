from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from __future__ import print_function
from ConfigParser import ConfigParser
import csv
import optparse

import os

# This runs on the output xlsx file of fetch_user_data. Gives insight into user data


def human_file_size(size):  # http://stackoverflow.com/a/1094933/70554
    format2 = "%3.1f %s"
    tiers = ["bytes", "KB", "MB", "GB", "TB"]

    for t in tiers[:-1]:
        if size < 1024.0:
            return format2 % (size, t)
        size /= 1024.0
    return format2 % (size, tiers[-1])


def median(values):
    values.sort()
    count = len(values)
    if count % 2 == 1:
        return values[count / 2]
    else:
        return (values[(count / 2) - 1] + values[count / 2]) / 2.0


if __name__ == "__main__":
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args()

    config = ConfigParser()
    config.read('settings.cfg')

    infile = csv.reader(open(os.path.join("output", "user_report.csv"), "rb"))

    headers = infile.next()

    types = ("user", "group", "admin", "entrusted", "inactive")
    storage = ([], [], [], [], [])

    for attr_values in infile:
        attrs = dict(zip(headers, attr_values))
        box_space_used = int(attrs["box_space_used"])
        active_shared_acct = 0
        active_individual_acct = 0
        if attrs["box_status"] == "active":
            if attrs["box_account_type"] == "" and attrs["box_role"] != "user":
                # active admin quota
                storage[2].append(box_space_used)
            elif attrs["box_name"][0:14] == "[BoxEntrusted]":
                # active entrusted quota
                storage[3].append(box_space_used)
            elif attrs["box_account_type"] == "" and attrs["box_name"][0:14] != "[BoxEntrusted]":
                # active group quota
                storage[1].append(box_space_used)
            elif attrs["box_account_type"] != "":
                # active user quota
                storage[0].append(box_space_used)
            else:
                print("unaccounted for users")
        else:
            # total inactive quota
            storage[4].append(box_space_used)
    s = []
    for i in range(0, len(types)):
        print("Summary for " + ("active " if i < 4 else "") + "%s accounts" % types[i])

        s = storage[i]
        stats = {"total_count": len(s)}
        if len(s) > 0:
            stats["space_total"] = human_file_size(sum(s))
            stats["space_mean"] = human_file_size(sum(s) / float(len(s)))
            stats["space_median"] = human_file_size(median(s))

            non_zero_storage = [x for x in s if x != 0]
            stats["non_zero_space_total"] = human_file_size(sum(non_zero_storage))
            stats["non_zero_space_mean"] = human_file_size(sum(s) / float(len(non_zero_storage)))
            stats["non_zero_space_median"] = human_file_size(median(non_zero_storage))

            stats["user_count_zero"] = s.count(0)

            s.sort(reverse=True)

            print("""\tTotal accounts: {total_count} 
            Total storage used: {space_total}
            Mean storage used: {space_mean}
            Median storage used: {space_median}\n""".format(**stats))
        else:
            print("\tzero accounts of this type\n")

    all_storage = []
    for sublist in storage:
        for item in sublist:
            all_storage.append(item)
    all_storage.sort(reverse=True)
    top_1_percent = round((sum(all_storage[0:len(s) / 100]) / float(sum(all_storage))) * 100, 2)
    top_10_percent = round((sum(all_storage[0:len(s) / 10]) / float(sum(all_storage))) * 100, 2)
    top_25_percent = round((sum(all_storage[0:len(s) / 4]) / float(sum(all_storage))) * 100, 2)

    print("Summary for all accounts:")
    print("""\tTop 1% of users account for: {0}% of space used   
    Top 10% of users account for: {1}% of space used 
    Top 25% of users account for: {2}% of space used""".format(top_1_percent, top_10_percent, top_25_percent))

    # print roles
    # print affiliations
