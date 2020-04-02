from bs4 import BeautifulSoup, SoupStrainer
import requests
import re

# constants
base_url = 'http://www.soci.ecnu.edu.cn'
news_url = base_url + '/10658/list'
headers = {
  'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Mobile Safari/537.36',
  'Referer': 'http://www.soci.ecnu.edu.cn/2c/24/c10658a273444/page.htm'
}
max_page = 11

# for pandas
titles = []
time = []
visit = []

# Filter the DOM first
only_news = SoupStrainer('div', id='wp_news_w3')

def page2url(i):
  return news_url + str(i+1) + '.htm'

def getNewsList(soup):
  return soup.select('div > table > tr')

def getTitle(news):
  return news('a')[0].string

def getDate(news):
  return news('div')[0].string

def getArticleURL(news):
  return news('a')[0]['href']

def getVisitCountURL(article_url):
  return base_url + '/_visitcountdisplay?siteId=295&type=3&articleId=' + article_url[-15:-9]

def fillTable(soup, title, date):
  global titles, time, visit
  s = soup.find('p').string.strip()
  print('{} | {} | {}'.format(title, date, s))
  visit.append(int(s))
  titles.append(title)
  time.append(date[5:])

def iterNews(news_list, r):
  date_regex = r'^2019-.*'
  for news in news_list:
    title = getTitle(news)
    date = getDate(news)
    if re.match(date_regex, date):
      article_url = getArticleURL(news)
      if not article_url.startswith('http'):
        soup = BeautifulSoup(r.post(getVisitCountURL(article_url),headers=headers).text,'lxml')
        try:
          fillTable(soup, title, date)
        except:
          pass

def export2Excel():
  import pandas as pd
  writer = pd.ExcelWriter('output.xlsx')
  df = pd.DataFrame(data={'title': titles, 'time':time, 'visit':visit})
  df.to_excel(writer,'Sheet1', index=False)
  writer.save()

def crawl():
  r = requests.Session()
  for i in range(max_page):
    soup = BeautifulSoup(r.get(page2url(i),headers=headers).text, 'lxml', parse_only=only_news)
    news_list = getNewsList(soup)
    iterNews(news_list, r)


if __name__ == "__main__":
    crawl()
    export2Excel()