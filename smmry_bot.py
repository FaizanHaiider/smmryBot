#!/usr/bin/python

import praw, re, subprocess, os
from langdetect import detect

def login():
    user_agent = ""
    r = praw.Reddit(client_id='',
                    client_secret='',
                    password='',
                    username='',
                    user_agent=user_agent
                    )
    return r

def main():
    r = login()


if __name__ == "__main__"
    main()
