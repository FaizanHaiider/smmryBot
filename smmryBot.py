#!/usr/bin/python

import praw, re, subprocess, os
from langdetect import detect

# create instance of Reddit and login
user_agent = ("")
r = praw.Reddit(client_id='',
				client_secret='',
				password='',
				username='',
				user_agent=user_agent)

# open subreddit
subr = r.subreddit("")

for comment in subr.stream.comments():
	if re.search("smmry_bot!", comment.body):
		
		# get reddit Submission object
		submission = comment.submission

		# call php script
		cmd = "php curlSmmry.php " + submission.url
		php_script = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		smmry_response = php_script.stdout.read()

		# parse php response
		smmry_array = re.split("\+", smmry_response)
		title = smmry_array[0].decode("utf-8")
		title = title[1:]
		summary = smmry_array[1].decode("utf-8")

		# check if smmry returned an error
		# if error in (0,1,2,3):
		# 	comment.reply("An error occured. Sorry about that.\n\n I am a **bot** [PM](https://www.reddit.com/message/compose/?to=danktofen) my creator for questions/concerns")
		# 	continue

		# check language. if not english, move on to next iteration
		if detect(summary) != "en":
			comment.reply("smmry.com works best with English articles. Articles in other languages result in summaries that don't make sense.\n\n I am a **bot**. [PM](https://www.reddit.com/message/compose/?to=danktofen) my creator for questions/concerns")
			continue
		
		# create final comment
		final_msg = "[" + title + "](" + submission.url + ") summarized in 7 lines using [smmry.com](http://www.smmry.com).\n\n \"" + summary + "\"\n\n I am a **bot**. [PM](https://www.reddit.com/message/compose/?to=danktofen) my creator for questions/concerns"

		# reply to post with summart
		comment.reply(final_msg)