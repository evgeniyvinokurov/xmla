from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import random
import string

import asyncio


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


url = 'localhost:8080/catalog/'

browser = webdriver.Firefox()
browser.get(url)

async def buy():
	name = get_random_string(8) + "_tab"
	browser.execute_script("window.open('about:blank','" + name + "');")
	browser.switch_to.window(name)
	browser.get(url)

	try:
		els = browser.find_elements(By.CLASS_NAME, "catalog-card");
		el = random.choice(els)

		action = ActionChains(browser)
		action.move_to_element(to_element=el).perform();
		el.find_element(By.CLASS_NAME, 'product-card__buy').click()

		browser.find_element(By.CLASS_NAME, 'cart').click()
		elem = browser.find_element(By.CLASS_NAME, 'cart-total__email')
		elem.send_keys(get_random_string(8) + "@test.com")
		browser.find_element(By.CLASS_NAME, 'cart-total__email-ok').click()
		browser.find_element(By.CLASS_NAME, 'cart-total__confirm').click()
	except:
		pass

async def buy2():
	name = get_random_string(8) + "_tab"
	browser.execute_script("window.open('about:blank','" + name + "');")
	browser.switch_to.window(name)
	browser.get(url)

	try:
		els = browser.find_elements(By.CLASS_NAME, "catalog-card");
		el = random.choice(els)

		action = ActionChains(browser)
		action.move_to_element(to_element=el).perform();
		el.find_element(By.CLASS_NAME, 'product-card__buy').click()
		el2 = random.choice(els)

		action = ActionChains(browser)
		action.move_to_element(to_element=el2).perform();
		el2.find_element(By.CLASS_NAME, 'product-card__buy').click()

		browser.find_element(By.CLASS_NAME, 'cart').click()
		elem = browser.find_element(By.CLASS_NAME, 'cart-total__email')
		elem.send_keys(get_random_string(8) + "@test.com")
		browser.find_element(By.CLASS_NAME, 'cart-total__email-ok').click()
		browser.find_element(By.CLASS_NAME, 'cart-total__confirm').click()
	except:
		pass


async def main():
	try:
		await asyncio.gather(buy(), buy(), buy())
		await asyncio.gather(buy2(), buy2())
	finally:
		browser.quit()

asyncio.run(main())
