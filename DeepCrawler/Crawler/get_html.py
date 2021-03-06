import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib.parse import quote
from .platforms import Platforms
import platform
from bs4 import BeautifulSoup as BS
import re

class GetHTML:
    def __init__(self):
        executable = ''
        if platform.system() == 'Windows':
            print('Detected OS : Windows')
            executable = './DeepCrawler/Crawler/chromedriver/chromedriver_win.exe'
        elif platform.system() == 'Linux':
            print('Detected OS : Linux')
            executable = './DeepCrawler/Crawler/chromedriver/chromedriver_linux'
        elif platform.system() == 'Darwin':
            print('Detected OS : Darwin')
            executable = './DeepCrawler/Crawler/chromedriver/chromedriver_mac'
        else:
            assert False, 'Unknown OS Type'

        print(executable)
        self.browser = webdriver.Chrome(executable)

    def get_post_links(self, platform, keyword, page_num):
        keyword_encode = quote(keyword)

        if platform == Platforms.GOOGLE:
            pass
        elif platform == Platforms.NAVER_BLOG:
            link = "https://section.blog.naver.com/Search/Post.nhn?pageNo={}&rangeType=ALL&orderBy=sim&keyword={}" \
                .format(page_num, keyword_encode)

            self.browser.get(link)

        time.sleep(1)

        elem = self.browser.find_element_by_tag_name("body")
        posts = self.browser.find_elements(By.XPATH, '//a[@class="desc_inner"]')

        links = []
        for post in posts:
            links.append(post.get_attribute("href"))

        return links

    def get_html(self, platform, post_link):
        self.browser.get(post_link)
        time.sleep(1)
        if platform == Platforms.GOOGLE:
            return "Google Not Implemented Yet"
        elif platform == Platforms.NAVER_BLOG:
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            html = self.html_scraper()
            cleanr = re.compile('<.*?>')
            html = re.sub(cleanr, '', html)
            return html

    def html_scraper(self):
        html = self.browser.find_elements_by_tag_name('html')
        html = html[-1].get_attribute('innerHTML')
        html = self.iframe_filter(html)
        return html

    def iframe_filter(self,input):
        result = None

        soup = BS(input,"lxml")
        list = soup.find_all('iframe')
        if len(list) == 0:
            # Return this frame's content
            result = input
        else:
            # Replace with filtered content
            # Return replaced html
            for idx, curr_element in enumerate(list):
                self.browser.switch_to.frame(idx)
                temp = self.html_scraper()
                curr_element.replaceWith(temp)
                self.browser.switch_to.parent_frame()
            result = str(soup)
        return result
