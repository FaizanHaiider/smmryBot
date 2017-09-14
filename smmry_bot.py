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
    content = [x.replace(".0", "") for x in content]
    # printArr(content)
    content_length = len(content)
    # print content_length
    return content, content_length

def write_to_file(most_recent_timestamp):
    file_name = "db.txt"
    with open(file_name, "w+") as f:
        f.write("%s\n" % most_recent_timestamp)

def format_smmry(smmry_response):
    smmry_array = re.split("\+", smmry_response)
    title = smmry_array[0].decode("utf-8")
    #title = title[1:]
    title = title.replace("\\'", "\'")

    smmry = smmry_array[1].decode("utf-8")
    smmry = smmry[1:]
    smmry = smmry.replace("[BREAK] ", "\n\n>")
    smmry = smmry.replace("[BREAK]", "")
    smmry = smmry.replace("\\'", "\'")

    return title, smmry

def get_smmry_php(subm):
    subm_url = subm.url
    cmd = "php curlSmmry.php " + subm.url
    php_script = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    smmry_response = php_script.stdout.read()

    try:
        title, summary = format_smmry(smmry_response)
    except:
        comment.reply("An error occured. Sorry about that.\n\n I am a **bot** [PM]() my creator for questions/concerns")
    return title, summary

def create_smmrys(r, most_recent_timestamp):
    subr = r.subreddit("testbotsdankt")
    post_id_list = []
    new_timestamp = most_recent_timestamp
    first_iter = 1

    for subm in subr.submissions(most_recent_timestamp):
        print subm.url
        for top_level_comment in subm.comments:
            if re.search("^(!smmry_bot)$", top_level_comment.body, re.IGNORECASE):
                title, smmry = get_smmry_php(subm)
            	# create final comment
                title = "**Title**: [" + title + "](" + subm.url + ") \n\n>"
            	ending_msg = "\n\n Notice something wrong or want to give feedback? Send me a msg. \n\n*I am a bot*"
                final_msg = title + smmry + ending_msg
                top_level_comment.reply(final_msg)
                if first_iter == 1:
                    new_timestamp = subm.created_utc
                    first_iter = 0
                    print new_timestamp
    return new_timestamp


def main():
    r = login()
    subms_ids, subms_length = load_previous_subm()
    most_recent_timestamp = "0"
    if subms_length > 0:
        most_recent_timestamp = subms_ids[0]
    most_recent_timestamp = create_smmrys(r, most_recent_timestamp)
    write_to_file(most_recent_timestamp)


if __name__ == "__main__":
    main()
