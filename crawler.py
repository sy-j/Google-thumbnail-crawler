from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os
import urllib.request
from multiprocessing import Pool
import pandas as pd

import random

print(random.random())

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' + directory)


def crawl(keyword):
    # keyword = 'Acer tataricum subsp. ginnala'

    chrome_driver = 'C:\\Users\\infoboss\\Desktop\\chromedriver_win32\\chromedriver'
    driver = webdriver.Chrome(executable_path=chrome_driver)

    driver.get('https://www.google.com/search?q='+keyword+'&tbm=isch')
    # https: // www.google.com / search?q = arabidopsis & tbm = isch & tbs = il:cl

    elem = driver.find_element_by_tag_name("body")
    print(keyword+' 스크롤 중 .............')
    while True:
      for i in range(10):
          elem.send_keys(Keys.PAGE_DOWN)
          time.sleep(random.random()/7)
      try:
        driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[2]/input').click()  # 결과 더보기
      except:
        pass
      try:
          driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div[2]/span').click()  # 나머지 검색결과는 내가 찾고 있는 항목이 아닐 수도 있습니다.
      except:
          pass
      try:
          driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[1]/div[2]/div[3]/div/span').click()  # 더 이상 로드할 수 없습니다..
      except:
          pass
      try:
        text = driver.find_element_by_xpath('//*[@id="islmp"]/div/div/div/div[1]/div[2]/div[1]/div[2]/div[1]/div').text
        # print(text)
        if text == '더 이상 표시할 콘텐츠가 없습니다.':
          break
      except:
        pass

    images = driver.find_elements_by_css_selector("img.rg_i.Q4LuWd")
    print(keyword+' 찾은 이미지 개수:', len(images))

    for i in range(100):
        elem.send_keys(Keys.PAGE_UP)
        time.sleep(random.random() / 7)

    # driver.execute_script("window.scrollTo(0, 0);")


    links=[]
    cnt = 0
    i = 0
    for img in images:
        i += 1
        print(i)
        print(img.get_attribute('src'))
        if img.get_attribute('src') != None:
            links.append(img.get_attribute('src'))
        else:
            result = None
            while result is None:
                time.sleep(3)
                result = img.get_attribute('src')
                for j in range(5):
                    elem.send_keys(Keys.PAGE_DOWN)
                for j in range(4):
                    elem.send_keys(Keys.PAGE_UP)
            # print('none detected')
            links.append(img.get_attribute('src'))
            print(result)
            cnt += 1
            # pass
    print(cnt)
    print(len(links))
    # for i in range(100):
    #     elem.send_keys(Keys.PAGE_UP)
    # # for i in range(1,len(images)):
    # for i in range(1,20):
    #     try:
    #         driver.find_element_by_xpath('//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img').click()
    #         time.sleep(2)
    #         link = driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img').get_attribute('src')
    #
    #         print(link)
    #         links.append(link)
    #         driver.find_element_by_xpath('//*[@id="Sva75c"]/div/div/div[2]/a').click()
    #         print(keyword+' 링크 수집 중..... number :'+str(i)+'/'+str(len(images)))
    #     except:
    #         print('fail')
    #         continue



    createFolder('C:\\Users\\infoboss\\Pictures\\poc\\'+keyword)

    forbidden=0
    for k,i in enumerate(links):
        try:
            url = i
            start = time.time()
            urllib.request.urlretrieve(url, "C:\\Users\\infoboss\\Pictures\\poc\\"+keyword+"\\"+str(k-forbidden)+'.jpg')
            print(str(k+1)+'/'+str(len(links))+' '+keyword+' 다운로드 중....... Download time : '+str(time.time() - start)[:5]+' 초')
        except:
            forbidden += 1
            print(forbidden)
            continue
    print(keyword+' ---다운로드 완료---')

    #
    # //*[@id="islmp"]/div/div/div/div[2]
    # 나머지 검색결과는 내가 찾고 있는 항목이 아닐 수도 있습니다.
    #
    # //*[@id="islmp"]/div/div/div/div[2]/span


if __name__ == '__main__':
    data = pd.read_csv('C:\\Users\\infoboss\\Downloads\\poclist.csv')
    for i in range(58, len(data)):
        print(data.iloc[i]['name'])
        crawl(keyword=data.iloc[i]['name'])
