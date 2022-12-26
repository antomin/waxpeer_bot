import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from common import get_driver
from handlers import parse_item

URL = 'https://waxpeer.com/?game=csgo&sort=DESC&order=date&all=0&exterior=FN&exterior=MW&exterior=FT&exterior=WW&exterior=BS'


def main():
    driver = get_driver()
    driver_wait = WebDriverWait(driver, 10)

    try:
        driver.get(URL)
        time.sleep(5)
        driver_wait.until(EC.presence_of_element_located((By.XPATH, '//i[@class="i-times f14"]'))).click()
        driver_wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="catalog__list"]')))

        while True:
            items = driver.find_elements(By.XPATH, '//div[@class="item_wrap"]')

            for item in items:
                parse_item(item)

            # driver.refresh()

            driver.find_element(By.XPATH, '//button[@class="btn-dark ordersort-top__order cselect_d"]').click()
            time.sleep(1)
            menus = driver.find_elements(
                By.XPATH, '//div[@class="cselect ordersort open"]//ul[@class="list cselect__list"]/li'
            )
            menus[1].click()
            driver_wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="catalog__list"]')))
    except Exception as error:
        print(error)

    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    while True:
        main()
