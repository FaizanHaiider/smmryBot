#!/usr/bin/python

import praw, re, subprocess, os
from langdetect import detect

# get reference ID from reference.txt  
if os.path.isfile("reference.txt"):
	with open("reference.txt", "r") as f:
		temp_id = f.read().split("\n")
		reference_id = temp_id[0]

# create instance of Reddit and login
user_agent = ("")
r = praw.Reddit(client_id='',
				client_secret='',
				password='',
				username='',
				user_agent=user_agent)

# open subreddit
subr = r.subreddit("pythonforengineers")

# filter self posts out from all new posts
all_new = subr.new(limit=50)
url_posts = []
for submission in all_new:
	if reference_id == submission.id:
		break
	elif not submission.is_self:
		url_posts.append(submission)

# create summary for each url post and reply to submission
for url in url_posts:
	cmd = "php curlSmmry.php " + url.url
	php_script = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
	smmry_response = php_script.stdout.read()

	# parse response
	smmry_array = re.split("\+", smmry_response)
	title = smmry_array[0].decode("utf8")
	summary = smmry_array[1].decode("utf8")

	# check language. if not english, exit
	if detect(summary) != "en":
		exit(1)

	# create final comment
	comment = "[" + title + "](" + url.url + ") summarized in 5 lines using [smmry.com](http://www.smmry.com).\n\n \"" + summary + "\"\n\n **I am a bot**"

	# reply to post with summart
	url.reply(comment)