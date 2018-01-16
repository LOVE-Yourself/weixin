from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
from lxml import etree
import urllib.request


class weixin_spider(object):
    def get_search_content(self,driver,search_input):
        # 获取搜索框
        input_search = driver.find_element_by_xpath('//*[@id="query"]')
        input_search.send_keys(search_input)
        input_search.send_keys(Keys.RETURN)

        date = []
        while True:
            dict = {}
            try:
                WebDriverWait(driver, 10).until(
                    EC.title_contains(search_input)
                )

            except Exception as e:
                print(e)

            time.sleep(3)
            # 解析url
            response = etree.HTML(driver.page_source)
            try:
                for i in range(20):
                    info_a = '//*[@id="sogou_vr_11002601_title_%s"]'%(str(i))
                    xpath_str = info_a + '//text()'
                    title = response.xpath(xpath_str)

                    if len(title) == 0:
                        break
                    new_title = ''.join(title)
                    s = self.get_info(info_a, driver, new_title)
                    if s == 1:
                        raise '没有下一页了！'
                    dict['title'] = new_title
                    print('---',new_title )
            except:
                print('这一页遍历完了！！！')
            try:
                next_page = WebDriverWait(driver, 10).until(

                    EC.visibility_of(driver.find_element_by_xpath('//*[@id="sogou_next"]'))
                )

                next_page.click()
            except Exception as e:
                print(e)
                break

    def get_info(self,xpath_str,driver,title):
        now_handle = driver.current_window_handle  # 获取当前窗口句柄
        try:
            # 再进一层 再退出来
            info_a = driver.find_element_by_xpath(xpath_str)
            info_a.click()
            time.sleep(3)

        except Exception as e:
            try:
                next_page = WebDriverWait(driver, 10).until(

                    EC.visibility_of(driver.find_element_by_xpath('//*[@id="sogou_next"]'))
                )

                next_page.click()
            except:

                return 1
            print(e)
        # 选择后窗口 关掉新窗口
        img_url_list = set()
        content_list = set()
        handles = driver.window_handles
        for new_handle in handles:
            if new_handle != now_handle:
                driver.switch_to.window(new_handle)
                response = etree.HTML(driver.page_source)
                sec_list = response.xpath('//*[@id="js_content"]//section')
                for sec in sec_list:
                    try:
                        img_url = sec.xpath('.//img/@data-src')
                        #print('--1-->',img_url)
                        if len(img_url) != 0:
                            for url in img_url:

                                img_url_list.add(url)
                        content = sec.xpath('.//span//text()')
                        if len(content) != 0:
                            for c in content:
                                content_list.add(c)
                        #print('--2->',content)
                    except:
                        print('xpath出错')

                p_list1 = response.xpath('//*[@id="js_content"]//p')
                for p in p_list1:
                    try:
                        img_url = p.xpath('.//img/@data-src')
                        if len(img_url) != 0:
                            for url in img_url:
                                img_url_list.add(url)

                        #print('--3-->',img_url)
                        content = p.xpath('.//span//text()')
                        if len(content) != 0:
                            for c in content:
                                content_list.add(c)
                        # print('--4->',content)
                    except:
                        print('xpath出错')
                driver.close()
                print('-----插图---->',img_url_list)
                print('----内容-->', content_list)
                driver.switch_to.window(now_handle)
                for url in list(img_url_list):
                    i = 0
                    data = urllib.request.urlopen(url).read()
                    path = './%s/'%(title)+str(i)+'.jpg'
                    print(path)
                    f = open(path,'wb')
                    f.write(data)
                    f.close()
        return 2


        # time.sleep(2)
          # 返回主窗口
        # driver.switch_to.window('风景的相关公众号文章-搜狗微信搜索')


    def crawl(self,root_url,search_input):
        chrome_opt = webdriver.ChromeOptions()
        prefs = {'profile.managed_default_content_settings.images':2}
        chrome_opt.add_experimental_option('prefs',prefs)

        driver = webdriver.Chrome(chrome_options=chrome_opt)
        #cookie_dict = {}
        #driver.add_cookie()
        driver.get(root_url)
        time.sleep(3)
        self.get_search_content(driver,search_input)

if __name__ == '__main__':

    wSpider = weixin_spider()
    wSpider.crawl('http://weixin.sogou.com/','风景')
