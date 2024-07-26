#get from 
import time
import random
import requests

headers = {
        'Origin': 'https://news.cnyes.com/',
        'Referer': 'https://news.cnyes.com/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}
    
def get_newslist_info(page=1, limit=30): 
    r = requests.get(f"https://api.cnyes.com/media/api/v1/newslist/category/headline?page={page}&limit={limit}", headers=headers)
    if r.status_code != requests.codes.ok:
        print('請求失敗', r.status_code)
        return None
    newslist_info = r.json()['items']
    return newslist_info

def get_news_list():
    newslist_info = get_newslist_info()
    new_lists = []
    for news in newslist_info["data"]:
        divider = '-------------------------------------\n'
        title = f'標題：{news["title"]}\n'
        summary = f'概要：{news["summary"]}\n'
        release_time = f'發布時間：{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(news["publishAt"]))}\n'
        link = f'[點擊前往該新聞](https://news.cnyes.com/news/id/{news["newsId"]})\n'
        msg = divider+title+summary+release_time+link
        new_lists.append(msg)
    return new_lists
        

