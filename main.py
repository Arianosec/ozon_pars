import time
import json
from selenium.common.exceptions import NoSuchElementException
from seleniumbase import Driver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


def main():
    result = []
    try:
        driver = Driver(uc=True)
        cat_url = []
        driver.get(url="https://www.ozon.ru/seller/")
        categories_list = driver.find_elements(By.CLASS_NAME, "hr3")
        for l in categories_list:
            url1 = l.get_attribute("href")
            cat_url.append(url1)
        for url in cat_url:
            shop_list = []
            driver.get(url)

            lastHeight = driver.execute_script("return document.documentElement.scrollHeight")

            while True:
                driver.execute_script(f"window.scrollTo(0, {lastHeight});")
                time.sleep(1)
                newHeight = driver.execute_script("return document.documentElement.scrollHeight")

                if newHeight == lastHeight:
                    break
                lastHeight = newHeight

            sellers = driver.find_elements(By.CLASS_NAME, "hq7")
            for seller in sellers:
                url2 = seller.get_attribute("href")
                print(url2)
                shop_list.append(url2)

            for shop in shop_list:
                id_s = shop.split("/")[4]
                id = id_s.split("-")[-1]
                driver.get(shop)
                time.sleep(1)
                logo = driver.find_element(By.CLASS_NAME, "h1x")
                logo.click()
                time.sleep(1)
                try:
                    name = driver.find_element(By.XPATH, "//div[contains(@class,'pe7')]/div[contains(@class,'')]/div[contains(@class, '')]/div/span[contains(@class, 'tsBody400Small')]").text
                except NoSuchElementException:
                    name = ''
                inn = name[-15:]
                if inn.isdigit():
                     pass
                else:
                     inn = ''
                for num in '1234567890':
                     name = name.replace(num, '')
                     name = name.replace("\n", '')
                work_type = driver.find_element(By.XPATH, "//div[contains(@class,'b6121-a5')]/div/div/div/div/div[5]/div/div/div[2]/span").text
                result.append({
                        "name": name,
                        "ogrn": inn,
                        "link": shop,
                        "seller_id":id,
                        "work_type": work_type})
        with open("result.json", "a", encoding="utf-8") as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

    except Exception as ex:
        print(ex)

    finally:
        driver.close()
        driver.quit()


if __name__ == "__main__":
     main()