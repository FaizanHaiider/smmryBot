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


def main():
    # r = login()
    submission_ids = load_previous_subm()



if __name__ == "__main__":
    main()
