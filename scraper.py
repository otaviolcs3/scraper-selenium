from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import sqlite3
import time
from typing import List

NUM_IMAGES = 1000
SEARCH_TERM = "dogs"

def get_img_urls(num: int, query: str) -> List[str]:
    opts = Options()
    opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)
    driver.maximize_window()
    driver.get("https://www.freeimages.com/")
    driver.find_element(By.ID, "search-input").send_keys(SEARCH_TERM)
    driver.find_element(By.ID, "search-submit-button").click()

    images_urls = []
    while len(images_urls) < num:
        try:
            pictures = driver.find_elements(By.XPATH, "//article/a/figure/picture/img")
            images_urls.extend(
                [pic.get_attribute("src") for pic in pictures if pic.get_attribute("src").startswith("https://")]
            )
        except Exception as e:
            print(e)
            continue
        try:
            driver.switch_to.window(driver.window_handles[-1])
            # scrolling down...
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            seemore_button = driver.find_element(By.XPATH, "//button[@data-testid='pagination-button-next']")
            driver.execute_script("arguments[0].scrollIntoView(true);window.scrollBy(0, -50);", seemore_button)
            # next page
            seemore_button.click()
            time.sleep(0.5)
        except Exception as e:
            print(e)
            break
    driver.quit()
    if len(images_urls) > num:
        images_urls = images_urls[:num]
    return images_urls

def insert_into_db(urls: List[str], desc: str):
    conn = sqlite3.connect("images.db")
    cur = conn.cursor()

    def create_table():
        cur.execute("CREATE TABLE IF NOT EXISTS images(id INTEGER PRIMARY KEY, url TEXT, description TEXT)")
        conn.commit()

    def insert_urls(urls: List[str], desc: str):
        cur.executemany("INSERT INTO images (url, description) VALUES (?, ?)", zip(urls, len(urls) * [desc]))
        conn.commit()
    
    create_table()
    insert_urls(urls, desc)

if __name__ == "__main__":
    urls = get_img_urls(NUM_IMAGES, SEARCH_TERM)
    insert_into_db(urls, SEARCH_TERM)
