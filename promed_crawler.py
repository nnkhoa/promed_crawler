import json
import requests 
import re

def crawl_id(id):
    url = "http://www.promedmail.org/ajax/getPost.php?alert_id=%s" % id
    web_resp = requests.get(url, headers={"Referer": "http://www.promedmail.org/"})
    post_html = web_resp.json().get('post')

    return post_html

def get_ids(content):
    id_strings = re.findall('id=\"id\d+', content)

    post_ids = []
    for id_string in id_strings:
        post_ids.append(re.sub('\D', "", id_string))
    
    return post_ids

def get_num_post(content):
    return re.findall('\d+',content)[0]

def crawl_search_result(date_start = "2019-07-01", date_end = "2019-07-29", num_page = 2):
    url = "http://www.promedmail.org/ajax/runSearch.php?date1=" +date_start + "&date2=" + date_end + "&pagenum=" + str(num_page)
    web_resp = requests.get(url, headers={"Referer": "http://www.promedmail.org/"})
    return web_resp.json().get('return')

def process_search_results(content):
    num_post = get_num_post(content)
    list_ids = get_ids(content)
    num_page = int(int(num_post)/len(list_ids))

    for i in range(3, num_page+2):
        list_ids.extend(crawl_search_result(num_page = i))
    
    return list_ids

def main():
    content = crawl_search_result() 
    list_ids = process_search_results(content)
    print(len(list_ids))

if __name__ == "__main__":
    main()
