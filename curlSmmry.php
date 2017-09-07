<?php
	# create curl cmd
	$curl_cmd = "http://api.smmry.com/&SM_API_KEY=&SM_WITH_BREAK&SM_LENGTH=6&SM_URL=$argv[1]";

	# init curl
	$ch = curl_init($curl_cmd);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	# make api call
	$output = json_decode(curl_exec($ch), true);
	# close connection
	curl_close($ch);
	# print smmry.com response
	echo $output["sm_api_title"];
	echo "+";
	echo $output["sm_api_content"];
?>
