from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
import os
import time


def post_facebook(text, img):
    # Open browser in virtual display and hide it, open facebook
    # Disable notifications
    Display(visible=0, size=(800, 600)).start()
    opts = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    opts.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=opts)
    driver.get('https://www.facebook.com')

    # Type user credentials
    driver.find_element_by_id('email').send_keys('asalgado21@gmail.com')
    driver.find_element_by_id('pass').send_keys('carmar1971?', Keys.ENTER)

    # Go to page
    driver.find_element_by_id('logoutMenu').click()
    driver.find_element_by_xpath('//div[text()="Salud y pimienta"]').click()
    time.sleep(10)

    # Write post
    xpath = '//div[text()="Escribe una publicación..."]'
    d = driver.find_element_by_xpath(xpath)
    driver.execute_script("arguments[0].click();", d)

    actions = ActionChains(driver)
    actions.send_keys(text)
    actions.perform()

    # Add Image
    driver.find_element_by_xpath('//div[text()="Foto/video"]').click()
    time.sleep(10)

    xpath = '//input[@data-testid="media-attachment-add-photo"]'
    driver.find_element_by_xpath(xpath).send_keys(os.getcwd()+"/"+img)
    time.sleep(10)

    # Submit post
    driver.find_element_by_xpath('//span[text()="Compartir"]').click()
