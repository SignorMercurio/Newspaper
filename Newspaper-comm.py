from bs4 import BeautifulSoup, SoupStrainer
import requests
import re

# constants
base_url = 'http://www.comm.ecnu.edu.cn'
news_url = base_url + '/htmlaction.do?method=toGetSubNewsList&menuType=11&pageNo='
headers = {
  'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Mobile Safari/537.36'
}
max_page = 7

# for pandas
time = []
visit = []

# Filter the DOM first
only_news = SoupStrainer(class_='news_area_text')
only_detail = SoupStrainer('div',id='view_record')

def page2url(i):
  return news_url + str(i)

def getNewsList(soup):
  return soup('a', href=re.compile(r'.*htmlId=\d'))

def getDate(news):
  return news.select('.newsdate')[0].string

def getArticleURL(news):
  return news['href']

def getVisitCountURL(article_url):
  return base_url + article_url

def fillTable(soup, date):
  global time, visit
  s = soup.find('div').string[5:]
  print(s)
  visit.append(int(s))
  time.append(date[10:])

def iterNews(news_list, r):
  date_regex = r'.*2019-.*'
  for news in news_list:
    date = getDate(news)
    if re.match(date_regex, date):
      article_url = getArticleURL(news)
      if not article_url.startswith('http'):
        soup = BeautifulSoup(r.get(getVisitCountURL(article_url),headers=headers).text,'lxml', parse_only=only_detail)
        try:
          fillTable(soup, date)
        except:
          pass

def export2Excel():
  import pandas as pd
  writer = pd.ExcelWriter('output.xlsx')
  df = pd.DataFrame(data={'time':time, 'visit':visit})
  df.to_excel(writer,'Sheet1', index=False)
  writer.save()

def crawl():
  r = requests.Session()
  r.get(base_url + '/htmlaction.do?method=toIndex')
  for i in range(max_page):
    soup = BeautifulSoup(r.get(page2url(i),headers=headers).text, 'lxml', parse_only=only_news)
    news_list = getNewsList(soup)
    iterNews(news_list, r)


if __name__ == "__main__":
    crawl()
    export2Excel()