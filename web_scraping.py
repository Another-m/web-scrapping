import requests
import bs4
import re
from pprint import pprint
from data import KEYWORDS, URL
from Send_to_telegramm import send_to_tg


def chek_in_keywords(head):
    counter_keys = 0
    for keyword in KEYWORDS:
        if keyword in head:
            counter_keys += 1
    return counter_keys

def parsing(soup):
    articles = soup.find_all(class_="tm-article-snippet__title")
    articles_date = soup.find_all(class_="tm-article-snippet__datetime-published")

    fist_news = []
    last_news = []
    for en, article in enumerate(articles):

        head_artic = article.find_all("span")
        link_artic = article.find_all('a')

        pattern_head = re.compile(r'<span>(.*)<')
        pattern_link = re.compile(r'href="(.*)">')
        pattern_date = re.compile(r'title="(.*)">')

        head = re.findall(pattern_head, str(head_artic))[0]
        link = "https://habr.com" + str(re.findall(pattern_link, str(link_artic))[0])
        date = re.findall(pattern_date, str(articles_date[en]))[0]

        all_info = {"Дата": date, "Заголовок": head, "Ссылка": link}
        if chek_in_keywords(head) > 0:
            fist_news.append(all_info)
        else:
            last_news.append(all_info)

    all_news = {"Интересные статьи": fist_news, "Остальные статьи": last_news}
    return all_news

def main(URL):
    response = requests.get(URL)
    response.raise_for_status()
    text_webpage = response.text
    soup = bs4.BeautifulSoup(text_webpage, features='html.parser')
    all_news = parsing(soup)

    print()
    pprint(all_news)
    print()

    try:
        send_to_tg(all_news)
        print("\n Интересные статьи успешно опубликованы на телеграм канале")
    except:
        print("\n Не удалось опубликовать статьи на телеграм канале, неверный token, либо Chat ID")



if __name__ == "__main__":
    main(URL)





