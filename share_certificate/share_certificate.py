from typing import List

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service

from base_class.sys_base_classes import Share
from utils.log_helper import qlogger
from utils.web_helper import get_driver


def get_single_share_certificate_websites(
        driver: webdriver.Edge,
        share_certificate_webs: str = r"http://quote.eastmoney.com/center"
        ):
    """
    获取全部单个基金的网址
    :param share_certificate_webs:
    :return:
    """

    driver.get(share_certificate_webs)
    driver.implicitly_wait(10)
    left_list = driver.find_elements(By.CLASS_NAME, "level1-wrapper")[0]
    hsj = left_list.find_elements(By.ID, "menu_hs_market")[0]
    share_web_pafe = hsj.get_attribute("href")

    driver.get(share_web_pafe)
    driver.implicitly_wait(10)
    table_body = driver.find_elements(By.TAG_NAME, "tbody")[0]
    records = table_body.find_elements(By.TAG_NAME, "tr")
    web_sites:List[Share] = []
    for rec in records:
        code = rec.find_elements(By.TAG_NAME, "a")[0].text
        name = rec.find_elements(By.TAG_NAME, "a")[1].text
        web_site = rec.find_elements(By.TAG_NAME, "a")[0].get_attribute("href")
        s = Share(code,name,web_site)
        qlogger.info(s)
        web_sites.append(s)
    print()

if __name__ == "__main__":
    driver = get_driver()
    get_single_share_certificate_websites(driver)