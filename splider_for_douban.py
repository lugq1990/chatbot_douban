import re
from bs4 import BeautifulSoup
import requests
import time
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import json


class DoubanSplider:
    def __init__(self) -> None:
        self.base_top_url = "https://movie.douban.com/top250?start={}&filter="
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def get_response(self, url):
        response = requests.get(url, headers=self.headers)

        if response.status_code != 200:
            print("Get some error from request! As error code is {}".format(response.status_code))
        
        bs = BeautifulSoup(response.content, 'html.parser')
        time.sleep(.2)
        return bs
    
    def get_response_with_driver(self, url):
        self.driver.get(url)
        
        bs = BeautifulSoup(self.driver.page_source, 'html.parser')
        time.sleep(.1)
        return bs

    def get_top250_links(self):
        each_page = 25
        full_n = 250
        res_tuple = []

        for i in range(int(full_n/each_page)):
            print("Now if page: {}".format(i))
            bs = self.get_response_with_driver(self.base_top_url.format(i * each_page))

            # find each page items
            items = bs.find_all('div', class_='item')
            for item in items:
                each_item_info = self._get_top_content(item)
                res_tuple.append(each_item_info)

        return res_tuple
        
        
    @staticmethod
    def save_list_into_file(obj_list, file_name, file_path=None):
        if not file_path:
            file_path = 'tmp_data'
        
        if file_name.find('.') == -1:
            file_name += '.txt'
        
        with open(os.path.join(file_path, file_name), 'w', encoding='utf-8') as f:
            for obj in obj_list:
                if isinstance(obj, list) or isinstance(obj, tuple):
                    f.write(','.join(obj) + '\n')
                else:
                    f.write(obj + '\n')

    @staticmethod
    def _get_top_content(item):
        title = item.find(class_='hd').find(class_='title').get_text()
        url = item.find(class_='hd').find('a').get('href')
        score = item.find_all("span", class_='rating_num')[0].get_text()
        n_users = item.find_all("span")[-2].get_text()
        return (title, score, n_users, url)

    def get_movie_base_info(self):
        """
        get_movie_base_info Just to use a open source link to get sample data based on movie ID.
        """
        base_api_url = "https://movie.querydata.org/api?id={}"

        # get full ids with movie name
        with open(os.path.join('tmp_data', 'top250_link.txt'), 'r', encoding='utf-8') as f:
            data_line = f.readlines()

        movie_info_dict = {}
        for data in data_line:
            id = data.split(',')[-1].split("/")[-2]
            movie_name = data.split(',')[0]
            response = requests.get(base_api_url.format(id)).text
            movie_info_dict[movie_name] = response
        
        return movie_info_dict





if __name__ == '__main__':
    splider = DoubanSplider()

    res_link = splider.get_top250_links()
    splider.save_list_into_file(res_link, 'top250_link.txt')