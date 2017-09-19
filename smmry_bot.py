#!/usr/bin/python

import praw, re, subprocess, os
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

ERR_STR = "Sorry, an error occured."
ENDING_STR = "\n\n Notice something wrong or want to give feedback? Send me a msg. \n\n*I am a bot*"

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
    old_timestamp = 0
    old_id = 0

    with open(file_name) as f:
        content = f.readline()

    if len(content) == 0:
        return old_timestamp, old_id

    content = content.strip("\n")
    content_split = content.split(":")

    old_timestamp = content_split[0]
    old_timestamp = old_timestamp.replace(".0", "")
    old_id = content_split[1]

    return old_timestamp, old_id

def write_to_file(old_timestamp, old_id):
    file_name = "db.txt"
    with open(file_name, "w+") as f:
        f.write("%s:%s\n" % (old_timestamp, old_id))

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

    # default title and summary values
    title = "error"
    summary = "error"

    try:
        title, summary = format_smmry(smmry_response)
    except:
        pass

    return title, summary

def create_smmrys(r, old_timestamp, old_id):
    subr = r.subreddit("testbotsdankt")
    post_id_list = []
    new_timestamp = old_timestamp
    new_subm_id = old_id
    first_iter = 1

    for subm in subr.submissions(old_timestamp):
        if subm.id == old_id:
            continue
        for top_level_comment in subm.comments:
            if re.search("^(!smmry_bot)$", top_level_comment.body, re.IGNORECASE):
                title, smmry = get_smmry_php(subm)

                # error check
                if title == "error" and summary == "error":
                    err_msg = ERR_STR + ENDING_STR
                    top_level_comment.reply(err_msg)
                else:
                    # create final comment
                    title = "**Title**: [" + title + "](" + subm.url + ") \n\n>"
                    final_msg = title + smmry + ENDING_STR
                    # reply to !smmry_bot comment
                    top_level_comment.reply(final_msg)

                # get new timestamp and id for next iteration
                if first_iter == 1:
                    new_timestamp = subm.created_utc
                    new_subm_id = subm.id
                    first_iter = 0
                    print "new: "
                    print new_timestamp
                    print new_subm_id

    return new_timestamp, new_subm_id


def main():
    r = login()
    old_timestamp, old_id = load_previous_subm()

    new_timestamp, new_id = create_smmrys(r, old_timestamp, old_id)

    write_to_file(new_timestamp, new_id)


if __name__ == "__main__":
    main()
