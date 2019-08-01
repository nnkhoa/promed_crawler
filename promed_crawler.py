import json
import requests 
import re
import os

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

# for some reasons, the first page of the search starts with number 2
def crawl_search_result(date_start = "2019-07-27", date_end = "2019-07-29", num_page = 2):
    url = "http://www.promedmail.org/ajax/runSearch.php?date1=" +date_start + "&date2=" + date_end + "&pagenum=" + str(num_page)
    web_resp = requests.get(url, headers={"Referer": "http://www.promedmail.org/"})
    return web_resp.json().get('return')

def write_post(filename, post_html):
    f = open(filename, 'w+')
    f.write(post_html)

def create_dir():
    dir_name = "content"
    try:
        os.mkdir(dir_name)
        print("Directory " + dir_name + " created.")
    except FileExistsError:
        print("Directory " + dir_name + " existed.")

def crawl(post_ids):
    file_path = "./content/"
    for post_id in post_ids:
        post_html = crawl_id(post_id)
        filename = file_path + post_id + ".html"
        write_post(filename, post_html)

def process_search_results(content):
    num_post = get_num_post(content)
    list_ids = get_ids(content)
    num_page = int(int(num_post)/len(list_ids))
    
    print("Total Post: ", num_post)
    print("Total Page: ", num_page)

    for i in range(3, num_page+3):
        list_ids.extend(get_ids(crawl_search_result(num_page = i)))
    return list_ids

def main():
    create_dir()
    content = crawl_search_result() 
    list_ids = process_search_results(content)
    crawl(list_ids)

if __name__ == "__main__":
    main()
