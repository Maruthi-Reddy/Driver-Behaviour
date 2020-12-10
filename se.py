from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

driver=webdriver.Chrome()

driver.get("http://127.0.0.1:5000/")
driver.find_element_by_name("accx").send_keys(".20")
driver.find_element_by_name("accy").send_keys(".20")
driver.find_element_by_name("accz").send_keys(".20")
driver.find_element_by_name("gccx").send_keys(".20")
driver.find_element_by_name("gccy").send_keys(".20")
driver.find_element_by_name("gccz").send_keys(".20")
time.sleep(5)
driver.find_element_by_xpath("/html/body/div[2]/form/div[7]/button").click()

driver.find_element_by_name("csvfile").send_keys("E:/Driver-behaviour-main/test.csv")
time.sleep(10)
driver.find_element_by_xpath("/html/body/form/div/input[2]").click()
time.sleep(15)
driver.close()


