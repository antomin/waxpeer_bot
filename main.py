import undetected_chromedriver
from settings import REPEAT_MSG
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from handlers import item_handler, get_stickers
from common import RARITY_DICT, read_cache, write_to_cache
from selenium.webdriver.support.select import Select

URL = 'https://waxpeer.com/?game=csgo&sort=DESC&order=date&all=0&exterior=FN&exterior=MW&exterior=FT&exterior=WW&exterior=BS'
# URL = 'https://waxpeer.com/en?game=csgo&sort=DESC&order=deals&all=0'


def main():
    options = undetected_chromedriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.headless = True
    driver = undetected_chromedriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    # try:
    driver.get(URL)
    time.sleep(3)
    wait.until(EC.presence_of_element_located((By.XPATH, '//i[@class="i-times f14"]'))).click()
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="catalog__list"]')))
    while True:
        items = driver.find_elements(By.XPATH, '//div[@class="item_wrap"]')
        for item in items:
            item_url = item.find_element(By.XPATH, './div[@class="item_body"]/a').get_attribute('href')
            item_id = item_url.split('/')[-1]
            if not REPEAT_MSG and item_id in read_cache():
                continue
            stickers_info = get_stickers(item)
            if stickers_info == 'search_not_found':
                continue
            price = item.find_element(By.XPATH, './/div[@class="prices f"]//span[@class="c-usd"]').text
            steam_price = item.find_element(By.XPATH,
                                            './/div[@class="item_top f ft gray"]//span[@class="c-usd"]').text
            name_model = item.find_element(By.XPATH, './/a[@class="name ovh"]').text
            name_gray = item.find_element(By.XPATH, './/div[@class="gray"]').text
            rarity = item.find_element(By.XPATH, './/div[@class="thumb_bg"]').get_attribute('style')
            try:
                item_float = item.find_element(By.XPATH, './/p[@class="num"]').text
            except Exception:
                item_float = None
            item_content = {
                'id': item_url.split('/')[-1],
                'url': item_url,
                'price': float(price.replace(' ', '')),
                'steam_price': float(steam_price.replace(' ', '')),
                'title': name_model.replace('\n', ' ') + ' (' + name_gray + ')',
                'item_float': float(item_float) if item_float else None,
                'stickers': stickers_info[0],
                'stickers_sum_price': stickers_info[1],
                'rarity': RARITY_DICT.get(rarity)
            }

            item_handler(item_content)
            write_to_cache(item_content['id'])

        driver.refresh()
        # Select(driver.find_element(
        #     By.XPATH, '//select[@class="btn-dark ordersort-top__order py10"]')).select_by_value('date')

        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="catalog__list"]')))

    # except Exception as error:
    #     print(error)
    #
    # finally:
    #     driver.close()
    #     driver.quit()


if __name__ == '__main__':
    while True:
        main()
