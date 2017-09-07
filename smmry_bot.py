#!/usr/bin/python

import praw, re, subprocess, os
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

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


# None == remove timestamp
# 1 == add timestamp
# 2 == return most recent timestamp
# def time_stamp(value=None):
#     if value == None:
#         # todo
#     elif value == 1:
#         # todo

def format_smmry(smmry_response):
    smmry_array = re.split("\+", smmry_response)
    title = smmry_array[0].decode("utf-8")
    title = title[1:]
    title = title.replace("\\'", "\'")

    smmry = smmry_array[1].decode("utf-8")
    smmry = smmry[1:]
    smmry = smmry.replace("[BREAK] ", "\n\n>")
    smmry = smmry.replace("[BREAK]", "")
    smmry = smmry.replace("\\'", "\'")

    return title, smmry

def create_smmry(subm):
    subm_url = subm.url
    cmd = "php curlSmmry.php " + subm.url
    php_script = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    smmry_response = php_script.stdout.read()

    try:
        title, summary = format_smmry(smmry_response)
    except:
        comment.reply("An error occured. Sorry about that.\n\n I am a **bot** [PM](https://www.reddit.com/message/compose/?to=danktofen) my creator for questions/concerns")
    return summary

def create_smmrys(r):
    subr = r.subreddit("testbotsdankt")
    post_id_list = []
    temp_timestamp = ""

    for subm in subr.new():
        print subm.url
        for top_level_comment in subm.comments:
            if re.search("^(!smmry_bot)$", top_level_comment.body, re.IGNORECASE):
                print top_level_comment.body
                smmry = create_smmry(subm)
                top_level_comment.reply(smmry)


def main():
    r = login()
    subms_ids, subms_length = load_previous_subm()
    most_recent_subm = "0"
    if subms_length > 0:
        most_recent_subm = subms_ids[0]
    create_smmrys(r)


if __name__ == "__main__":
    main()
