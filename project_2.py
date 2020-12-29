import requests
from bs4 import BeautifulSoup
import collections #iterable 객체를 판별하기 위한 import


#[오늘의 날씨]
# 흐림, 어제보다 00도 높아오
# 현재 00도C (최저 00/ 최고 00)
# 오전 강슈확률 00% / 오후 강수 확률 00%

#미세먼지 00 / 좋음
#초미세먼지 00 / 좋음

#[헤드라인 뉴스]
#1. 무슨무슨 일이...
# (링크 : https://...)
#2. 어떤 어떤 일이...
# (링크 : https://...)
#3. 이런 저런 일이...
# (링크 : https://...)
def pirnt_news(index, title, link):
    print("{}. {}".format(index + 1, title))
    print(" (링크 : {})".format(link))


def create_soup(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63"
    }
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup

def scrape_weather():
    print("[오늘의 날씨]")
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8"
    soup = create_soup(url)
    # 흐림, 어제보다 00도 높아오
    cast = soup.find("p", attrs={"class":"cast_txt"}).get_text()
    # 현재 00도C (최저 00/ 최고 00)
    curr_temp = soup.find("p", attrs={"class":"info_temperature"}).get_text().replace("도씨","")
    min_temp = soup.find("span", attrs={"class":"min"}).get_text()#최저 온도
    max_temp = soup.find("span", attrs={"class":"max"}).get_text()#최고 온도
    # 오전 강슈확률 00% / 오후 강수 확률 00%
    morning_rain_rate = soup.find("span", attrs={"class":"point_time morning"}).get_text().strip() #오전 강수 확률
    after_rain_rate = soup.find("span", attrs={"class": "point_time afternoon"}).get_text().strip() #오후 강수 확률

    # 미세먼지 00 / 좋음
    # 초미세먼지 00 / 좋음
    dust = soup.find("dl", attrs={"class":"indicator"})
    pm10 = dust.find_all("dd")[0].get_text()#미세먼지
    pm25 = dust.find_all("dd")[1].get_text()#초미세먼지

    #출력
    print(cast)
    print("현재 {} (최저 {} / 최고 {}) ".format(curr_temp,min_temp,max_temp))
    print("오전 {} / 오후 {}".format(morning_rain_rate, after_rain_rate))
    print()
    print("미세먼지 {}".format(pm10))
    print("초미세먼지 {}".format(pm25))
    print()

def scrape_headline_news():
    print("[헤드라인 뉴스]")
    url = "https://news.naver.com"
    soup = create_soup(url)
    #news_list = soup.find("ul", attrs={"class":"hdline_article_list"}).find_all("li", limit=3)
    news_list = soup.find("ul", attrs={"class":"hdline_article_list"}).find_all("li")
    for index, news in enumerate(news_list):
        title = news.find("a").get_text().strip()
        link = url + news.find("a")["href"]
        pirnt_news(index,title,link)
    print()

def scrape_it_news():
    print("[IT 뉴스]")
    url = "https://news.naver.com/main/list.nhn?mode=LS2D&mid=shm&sid1=105&sid2=230"
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"type06_headline"}).find_all("li")
    for index, news in enumerate(news_list):
        a_idx = 0
        img = news.find("img")
        if img:
            a_idx = 1 # img 가 있으면 2번째 a 태그의 정보를 사용
        title = news.find_all("a")[a_idx].get_text().strip()
        link = news.find_all("a")[a_idx]["href"]
        pirnt_news(index, title, link)
    print()

if __name__ == "__main__":
    scrape_weather() #오늘의 날씨 정보 가져오기
    scrape_headline_news() #헤드라인 뉴스 정보 가져오기
    scrape_it_news()
