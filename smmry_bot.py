#!/usr/bin/python

import praw, re, subprocess, os

def printArr(arr):
    for x in arr:
        print x

def login():
    user_agent = ""
    r = praw.Reddit(client_id='',
                    client_secret='',
                    password='',
                    username='',
                    user_agent=user_agent
                    )
    return r
def load_previous_subm():
    file_name = "db.txt"
    with open(file_name) as f:
        content = f.readlines()
    content = [x.strip('\n') for x in content]
    # printArr(content)
    content_length = len(content)
    # print content_length
    return content, content_length

def write_to_file(arr):
    file_name = "db.txt"
    with open(file_name, "w+") as f:
        for subm in arr:
            f.write("%s\n" % subm)


def main():
    # r = login()
    subms_ids, subms_length = load_previous_subm()
    most_recent_subm = "0"
    if subms_length > 0:
        most_recent_subm = subms_ids[0]

    # print most_recent_subm






if __name__ == "__main__":
    main()
