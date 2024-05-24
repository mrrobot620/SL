from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from selenium import webdriver
import os 
from select import select
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC3
from selenium.webdriver.common.action_chains import ActionChains
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
import time
import json

op = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_settings.popups': 0,
    'download.default_directory' : r"/home/administrator/cbs_bag_hold/data",
    'directory_upgrade': True
}
op.add_experimental_option('prefs' , prefs)
driver = webdriver.Chrome(options=op)


@csrf_exempt
def login_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        input_username = data.get("username")
        input_password = data.get("password")

        print(f"Username:  {input_username}")
        print(f"Password:  {input_password}")

        driver.get("http://10.24.0.157/")
        time.sleep(5)
        username = driver.find_element(By.XPATH , "/html/body/div[2]/div[2]/div/div/form/div/div[4]/input[1]")
        username.send_keys(input_username)
        password = driver.find_element(By.XPATH , "/html/body/div[2]/div[2]/div/div/form/div/div[4]/input[2]")
        password.send_keys(input_password)
        time.sleep(2)
        try:
            cross = driver.find_element(By.XPATH , "/html/body/div[4]/div/button")
            cross.click()
        except:
            print("Cross Button Failed")
        time.sleep(1)
        submit = driver.find_element(By.XPATH , "/html/body/div[2]/div[2]/div/div/form/div/div[4]/div[4]/button/span")
        submit.click()
        time.sleep(8)

        try:
            csrf_token = driver.execute_script("return document.querySelector('meta[name=crsf-token]').getAttribute('content)")
            print(f"CSRF Token:  {csrf_token}")
        except Exception as e:
            print(f"Unable to Find CSRF Token")

        session_cookie = driver.get_cookies()
        print(session_cookie)
        selenium_user_agent = driver.execute_script("return navigator.userAgent;")
        print(selenium_user_agent)

        return JsonResponse({"cookies": session_cookie , 'user_agnet': selenium_user_agent})
    else:
        return JsonResponse({'error': 'Error 69'})