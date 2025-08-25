from playwright.sync_api import sync_playwright
import time
import re
from jsonLoader import jsonLoader


PATH="./data/new_reading_list.json"
HREFS_PATH="./data/hrefs.txt"
ERROR_HREFS_PATH="./data/error_chapters.txt"


def extractMangaURLs(targetURLCount):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # поменяй на True для работы без окна
        page = browser.new_page()
        page.goto("https://remanga.org/manga/", wait_until="networkidle")

        page.wait_for_selector('button:has-text("По популярности")')
        page.click('button:has-text("По популярности")')

        page.wait_for_selector('span:has-text("По кол-ву эпизодов")')
        page.click('span:has-text("По кол-ву эпизодов")')
        time.sleep(2)

        page.wait_for_selector('a[data-sentry-component="TitlesFeedContent"]')

        last_count = 0
        retries = 0

        while True:
            # Получаем количество найденных ссылок
            links = page.query_selector_all('a[data-sentry-component="TitlesFeedContent"]')
            current_count = len(links)
            print(f"{current_count}/{targetURLCount}", end='\r')

            if current_count >= targetURLCount:
                break

            if current_count == last_count:
                retries += 1
                if retries > 5:
                    print("Больше ссылок не грузится, выходим.")
                    break
            else:
                retries = 0
                last_count = current_count

            # Скроллим вниз
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(2)

        # Собираем все href
        hrefs = page.eval_on_selector_all(
            'a[data-sentry-component="TitlesFeedContent"]',
            "els => els.map(e => e.href)"
        )

        print(f"Итоговое количество найденной манги: {len(hrefs)}")

        with open(HREFS_PATH, "w", encoding="utf-8") as f:
            for link in hrefs:
                f.write(link + "\n")
        browser.close()

        return hrefs

def getBranchIdAndTitle(chapters_url):
    branch_ids = set()
    title = "Неизвестно"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        # Отслеживаем сетевые запросы
        try:
            def handle_request(request):
                url = request.url
                if "api/v2/titles/chapters" in url and "branch_id=" in url:
                    match = re.search(r"branch_id=(\d+)", url)
                    if match:
                        branch_ids.add(match.group(1))
            page.on("request", handle_request)
            page.goto(chapters_url, wait_until="networkidle")
            page.wait_for_timeout(500)
        except Exception as e:
            print(f"Не удалось получить данные с ссылки: {chapters_url}\n", e)
            with open(ERROR_HREFS_PATH, "w+", encoding="utf-8") as f:
                f.write(chapters_url + '\n')
            
        # Название тайтла
        try:
            title_selector = 'p.cs-text.text-2xl.leading-2xl.font-bold.text-foreground.cs-layout-title-text'
            page.wait_for_selector(title_selector, timeout=3000)
            title = page.locator(title_selector).first.text_content().strip()
        except Exception as e:
            print("Не удалось извлечь название:", e)

        browser.close()

    try:
        return {
                "title": title,
                "branch_id": int(list(branch_ids)[0]),
                "current_page": 1
            }
    except Exception as e:
        print(f"\n{e}\n")
        return {}

def getMangaBranchId(saveFile=True, targetURLCount=30):
    urls = extractMangaURLs(targetURLCount)
    data = {
        "in_queue": [],
        "current": None,
        "finished": []
    }
    for i in range(len(urls)):
        new_item = getBranchIdAndTitle(urls[i][:len(urls[i])-4] + "chapters/")
        if new_item:
            data["in_queue"].append(new_item)
            print(f"Загружено {i + 1}/{len(urls)}: {new_item['title']}" + " " * 50, end="\r")
            if saveFile:
                jsonLoader.SaveFile(PATH, data)
    print("\n")
    return data


if __name__ == "__main__":
    getMangaBranchId(targetURLCount=2000)