from selenium import webdriver
from selenium.webdriver.edge.service import Service

def get_driver() -> webdriver.Edge:
    driver_path = r"D:\Python3_11\msedgedriver.exe"
    driver = webdriver.Edge(service=Service(executable_path=driver_path))
    return driver