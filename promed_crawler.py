import json
import requests 
import re
import os
import arghandler
import time
from joblib import Parallel, delayed
import multiprocessing

class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)

class SearchTool:

    __search = ""
    __date_start = ""
    __date_end = ""
    __num_page = 0
    __json_content = ""

    list_ids = []

    def __init__(self, options):
        self.__search = options.search
        self.__date_start = options.date_start
        self.__date_end = options.date_end

    def get_ids(self):
        id_strings = re.findall('id=\"id\d+', self.__json_content)

        post_ids = []
        for id_string in id_strings:
            post_ids.append(re.sub('\D', "", id_string))
    
        return post_ids
    
    def get_num_post(self):
        return re.findall('\d+', self.__json_content)[0]

    def process_search_results(self):
        num_post = self.get_num_post()
        list_ids = self.get_ids()
        
        print(len(list_ids))
        
        self.__num_page = int(int(num_post)/len(list_ids))
    
        print("Total Post: ", num_post)
        print("Total Page: ", self.__num_page)

        for i in range(3, self.__num_page+3):
            self.search_promed(num_page = i)
            list_ids.extend(self.get_ids())
        
        self.list_ids = list_ids
    
    # for some reasons, the first page of the search starts with number 2
    def search_promed(self, num_page = 2):
        url = ("http://www.promedmail.org/ajax/runSearch.php?search=" + self.__search
                                                        + "&date1=" + self.__date_start 
                                                        + "&date2=" + self.__date_end 
                                                        + "&pagenum=" + str(num_page))
        web_resp = requests.get(url, headers={"Referer": "http://www.promedmail.org/"})
        
        self.__json_content = web_resp.json().get('return')

    def get_search_ids(self):
        self.search_promed()
        self.process_search_results()

class Crawler:
    def __init__(self):
        print ("Initiate Crawler.")

    def crawl_id(self, post_id):
        url = "http://www.promedmail.org/ajax/getPost.php?alert_id=%s" % post_id
        web_resp = requests.get(url, headers={"Referer": "http://www.promedmail.org/"})
        post_html = web_resp.json().get('post')

        return post_html

    def write_post(self, filename, post_html):
        f = open(filename, 'w+')
        f.write(post_html)
    
    def put_in_file(self, file_path, post_id):
        post_html = self.crawl_id(post_id)
        filename = file_path + post_id + ".html"
        self.write_post(filename, post_html)
        return 0

    def crawl(self, post_ids, parallel = 0):
        file_path = "./content/"
        
        if parallel >= 2:
            Parallel(n_jobs = parallel, prefer="threads") (delayed(self.put_in_file)(file_path, post_ids[i]) for i in range(len(post_ids)))
        else:
            for post_id in post_ids:
                self.put_in_file(file_path, post_id)

def create_dir():
    dir_name = "content"
    try:
        os.mkdir(dir_name)
        print("Directory " + dir_name + " created.")
    except FileExistsError:
        print("Directory " + dir_name + " existed.")


def main():
    create_dir()
    args = arghandler.parse_argv()

    num_cores = multiprocessing.cpu_count()
    print("CPU cores: ", num_cores)

    options = Struct(**args)

    search_tool = SearchTool(options)
    crawler = Crawler()
    
    search_tool.get_search_ids()
    
    start = time.time()
    crawler.crawl(search_tool.list_ids, int(options.parallel))
    end = time.time()

    print("Elapsed Time: ", end - start)

if __name__ == "__main__":
    main()
