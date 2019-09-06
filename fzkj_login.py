import logging
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)


def selenium_login(username, password):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.maximize_window()
    driver.get(
        'http://authserver.cidp.edu.cn/authserver/login?service=http%3A%2F%2Fehall.cidp.edu.cn%2Flogin%3Fservice%3Dhttp%3A%2F%2Fehall.cidp.edu.cn%2Fnew%2Findex.html')
    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_xpath('//*[@id="casLoginForm"]/p[5]/button').click()
    time.sleep(5)
    try:
        driver.find_element_by_xpath(
            '//*[@id="ampTabContentItem0"]/div[1]/pc-card-html-4764378802414004-01/amp-w-frame/div/div[2]/div[1]/div/div/div/div/div/div/div[2]/div/widget-app-item[4]/div/div').click()
    except:
        # 登陆失败关闭driver
        driver.quit()
        return False
    time.sleep(2)
    n = driver.window_handles
    driver.switch_to.window(n[1])
    try:
        driver.switch_to.frame('divFrame1')
    except:
        # 登陆失败关闭driver
        driver.quit()
        return False
    driver.find_element_by_xpath('//*[@id="divSubMenuList"]/div[5]/div[3]/a/dl').click()
    cookies = driver.get_cookies()
    cookies_dict = {}
    for cookie in cookies:
        cookies_dict[cookie['name']] = cookie['value']
    driver.quit()
    return cookies_dict
