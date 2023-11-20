from typing import List

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service


def get_daily_data(fund_website: str, driver: webdriver.Edge):
    """
    获取基金的单日数据
    :param fund_website:
    :return:
    """

    driver.get(fund_website)
    driver.implicitly_wait(10)
    js = 'window.scrollTo(0, 800);' # 往下拉 800 个像素单位
    driver.execute_script(js)
    buttons = driver.find_elements(By.CLASS_NAME, value='highcharts-button')
    for b in buttons:  # 点击成立来 标签
        if b.text != "成立来":
            continue
        b.click()
        driver.implicitly_wait(10)
        break

    fund_net_value = driver.find_element(By.ID, value="highcharts-0")
    t_tags = fund_net_value.find_elements(By.TAG_NAME, value='g')
    highcharts = []
    for gg in t_tags:
        if gg.get_attribute("class") == "highcharts-series highcharts-series-0":
            highcharts.append(gg)
    data_set = []
    kk = highcharts[0].find_elements(By.TAG_NAME, value="path")
    for k in kk:
        if k.get_attribute("stroke-width") != "2":
            continue
        data_set = k.get_attribute("d")
        break

    data_x: List[float] = []
    data_y: List[float] = []
    data_list = data_set.split(" ")
    for idx in range(0, len(data_list), 3):
        # print(f"{data_list[idx]}: {data_list[idx + 1]} {data_list[idx + 2]}")
        data_x.append(float(data_list[idx + 1]))
        data_y.append(1-(float(data_list[idx + 2]) - 85)/425.0)
    driver.close()

    return data_x, data_y


def get_driver() -> webdriver.Edge:
    driver_path = r"D:\Python3_11\msedgedriver.exe"
    driver = webdriver.Edge(service=Service(executable_path=driver_path))
    return driver


def get_open_fund_website(base_web=r"http://fund.eastmoney.com/data/"):
    """
    获取全部可开放式基金网页
    :return:
    """
    page = requests.get(base_web)
    page.encoding = "utf-8"
    # html = page.text
    soup = BeautifulSoup(page.text, features="html.parser")
    company_items = soup.find(name="a", string="点击查看全部开放式基金净值>>")
    website = company_items["href"]
    print(f"find {website}")
    return website


def get_single_fund_websites(open_fund_website: str, base_website=r"http://fund.eastmoney.com"):
    """
    获取全部单个基金的网址
    :param open_fund_website:
    :return:
    """
    page = requests.get(open_fund_website)
    if page.status_code != 200:
        print(f"{page.status_code}:error")
    page.encoding = "gb18030"
    soup = BeautifulSoup(page.text, features="html.parser")
    company_items = soup.find_all(name="td",
                                  attrs={"class": "tol"})
    all_fund_website: List[List[str]] = []
    for idx, company_item in enumerate(company_items):
        # dd = company_item.text.strip()
        ele_one = company_item.find_next(name='nobr').find_next('a')
        all_fund_website.append(
            [ele_one['title'], f"{base_website}/{ele_one['href']}"]
        )
        print(f"text{idx}: {ele_one['title']}, website:{base_website}/{company_item.text}")
    return all_fund_website


