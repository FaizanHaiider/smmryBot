#!/usr/bin/python

import praw # reddit API
import re # regex  
import subprocess # to run php script
import os # open, read, and close reference file


# get newest post submission.ID
if os.path.isfile("reference.txt"):
	with open("reference.txt", "r") as f:
		refer_id = f.read()

# create instance of Reddit and login
user_agent = ("")
r = praw.Reddit(client_id='',
				client_secret='',
				password='',
				username='',
				user_agent=user_agent)

# open subreddit
subr = r.subreddit("swissnews")

# newest post
temp_list = subr.new(limit=1)
newest_post = temp_list.next()

# check if new content
if newest_post.id == refer_id:
	exit(1) # no new content
else:
	id_for_file = newest_post.id # new content
	with open("reference.txt", "w") as f:
		f.write(id_for_file)


# find URL post(s)
submissions = subr.new()
for submission in submissions:
	if not submission.is_self:
		if submission.id == refer_id:
			exit(1)
		else:
			# run php script and read response
			cmd = "php curlSmmry.php " + submission.url
			php_script = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
			smmry_response = php_script.stdout.read()

			# # parse response
			smmry_array = re.split("\+", smmry_response)
			title = smmry_array[0].decode("utf8")
			summary = smmry_array[1].decode("utf8")

			# # create final comment
			comment = "[" + title + "](" + submission.url + ") summarized in 5 lines using [smmry.com](http://www.smmry.com).\n\n \"" + summary + "\"\n\n **I am a bot**"

			# # reply to post with summart
			submission.reply(comment)
