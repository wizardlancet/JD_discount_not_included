# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 16:06:15 2017
Jingdong 10/30/2017 不参加活动的特例书籍
@author: wangzilong-ti
"""

url = "https://search.jd.com/Search?keyword=%E7%89%B9%E4%BE%8B%E5%95%86%E5%93%81%E4%B8%8D%E5%8F%82%E5%8A%A0&enc=utf-8&wq=%E7%89%B9%E4%BE%8B%E5%95%86%E5%93%81%E4%B8%8D%E5%8F%82%E5%8A%A0&pvid=90d595ef21834071a9cfdef5f536e226"



from splinter import Browser
from bs4 import BeautifulSoup
import time

executable_path = {'executable_path':r'C:\Program Files (x86)\Google\Chrome\Application'}
executable_path = {'executable_path':r'E:\program\chromedriver'}
#executable_path = {'executable_path':r'C:\Program Files\Mozilla Firefox'}
browser = Browser()
browser.visit(url)


items = []

scroll_js="var q=document.documentElement.scrollTop=10000"
while True:
    time.sleep(0.1)
    browser.execute_script(scroll_js)
    time.sleep(0.5)
    goods = browser.find_by_id('J_goodsList')[0]
    soup = BeautifulSoup(goods.html)
    goods_lists = soup.html.body.ul
    items += goods_lists.find_all('li',class_='gl-item')
    next_btn = browser.find_by_css('.pn-next')[0]
    if next_btn.has_class('disabled'):
        break
    else:
        next_btn.click()
        
print len(items)

z = items[1107]

extract_desc = lambda x: x.div.a.attrs['title'].replace(u'【特例商品不参加每满100减50促销】','')
extract_price = lambda x: x.div.find('div',class_='p-price').i.getText()
extract_name = lambda x: x.div.find('div',class_='p-name').a.em.getText().replace(u'[特例商品不参加每满100减50促销]','')
extract_shop = lambda x: x.div.find('div',class_='p-shopnum').a.getText() if x.div.find('div',class_='p-shopnum').a else ""
extract_comm = lambda x: x.div.find('div',class_='p-commit').a.getText()


description = map(extract_desc, items)
price = map(extract_price, items)
name = map(extract_name, items)
shop = map(extract_shop, items)
comm = map(extract_comm, items)

wan = lambda x: 10000 if x.find(u'万') else 1
numerized_comm = [float(p.replace(u'+','').replace(u'万',''))*wan(p) for p in comm]]


import pandas as pd
df = pd.DataFrame({'name':name,'desc':description,'shop':shop,'price':price,'comm':comm,'numerized_comm':numerized_comm})

df.to_excel('booklist.xls')
