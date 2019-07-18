import json
import requests 


def crawl_id(id):
	url = "http://www.promedmail.org/ajax/getPost.php?alert_id=%s" % id
	web_resp = requests.get(url, headers={"Referer": "http://www.promedmail.org/"})
	post_html = web_resp.json().get('post')

	return post_html
