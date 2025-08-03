import os
from dotenv import load_dotenv
load_dotenv()


MANGA_BRANCHID_JSON = "./manga_branch_id.json"
READING_LIST_JSON = "./reading_list.json"
MAX_COUNT_COMMENTS = 41
MAX_COUNT_CHAPTERS_BEFORE_LIGHTING = 10



headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
    "Accept": "*/*",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Referer": "https://remanga.org/",
    "Content-Type": "application/json",
    "Authorization": os.getenv('AUTORIZATION'),
    "Origin": "https://remanga.org",
    "DNT": "1",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Priority": "u=0",
}

commentTitlePayload = {
    "text": (
        '<p dir="ltr"><span style="white-space: pre-wrap;">'
        'Хочу карточку за комментарий'
        '</span></p><p dir="ltr"><br></p>'
    ),
    "title": 51969
}

commentChapterPayload = {
    "text": (
        '<p dir="ltr"><span style="white-space: pre-wrap;">'
        'Хочу карточку за комментарий'
        '</span></p><p dir="ltr"><br></p>'
    ),
    "chapter": 1818647,
    "page": 1
}

commentUrl = "https://api.remanga.org/api/v2/activity/comments/"
chaptersUrl = "https://api.remanga.org/api/v2/titles/chapters/?chapter=&user_data=1"
readChapterUrl = "https://api.remanga.org/api/activity/views/"
# Для получения молний за ежедневное посещение
currentUserUrl = "https://api.remanga.org/api/v2/users/current/"
my_id = 31134