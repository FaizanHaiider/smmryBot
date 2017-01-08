#!/usr/bin/python

import praw, re, subprocess, os
from langdetect import detect

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


# create instance of Reddit and login
user_agent = ("")
r = praw.Reddit(client_id='',
				client_secret='',
				password='',
				username='',
				user_agent=user_agent)

# open subreddit
subr = r.subreddit("pythonforengineers")
post_id_list = []

for comment in subr.stream.comments():
	if re.search("^(smmry_bot!)$", comment.body, re.IGNORECASE):
		
		# get reddit Submission object
		submission = comment.submission

		if submission.id in post_id_list:
			summary_exists = "A summary has already been created for this submission. Summary under parent comment = smmry_bot! (case insensitive). \n\n I am a **bot**. [PM](https://www.reddit.com/message/compose/?to=danktofen) my creator for questions/concerns"
			comment.reply(summary_exists)
			continue

		print submission.url

		# call php script
		cmd = "php curlSmmry.php " + submission.url
		php_script = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		smmry_response = php_script.stdout.read()

		# parse php response. catch any errors
		try:
			title, summary = format_smmry(smmry_response)
		except:
			comment.reply("An error occured. Sorry about that.\n\n I am a **bot** [PM](https://www.reddit.com/message/compose/?to=danktofen) my creator for questions/concerns")
		 	continue

		# check language. if not english, move on
		if detect(summary) != "en":
			comment.reply("smmry.com works best with English articles. Articles in other languages result in summaries that don't make sense.\n\n I am a **bot**. [PM](https://www.reddit.com/message/compose/?to=danktofen) my creator for questions/concerns")
			continue
		
		# create final comment
		final_msg = "[" + title + "](" + submission.url + ") summarized in 5 lines using [smmry.com](http://www.smmry.com).\n\n>" + summary + "\n\n I am a **bot**. [PM](https://www.reddit.com/message/compose/?to=danktofen) my creator for questions/concerns"

		print final_msg

		# reply to post with summart
		comment.reply(final_msg)

		# record submission id so script doesn't summarize the same article twice
		post_id_list.append(submission.id) 