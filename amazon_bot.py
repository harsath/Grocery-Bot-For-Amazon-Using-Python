from bs4 import BeautifulSoup

#Importing Selenium Packages
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By 
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

#from selenium.common.exceptions import TimeOutException

import re
import time

class AmazonBot:
	#Init the Constructor Class:
	def __init__(self,items):
		self.amazon_url = "https://www.amazon.in"
		self.items = items
		self.binary = FirefoxBinary('geckodriver')
		#Creating the Instance for Web Driver(FireFox)
		self.profile = webdriver.FirefoxProfile()
		self.options = Options()
		self.driver = webdriver.Firefox()
		self.driver.get(self.amazon_url)

	def search_items(self):
		#PlaceHolders for Items
		urls = []
		prices = []
		name_of_items = []
		for items in self.items:
			print(f'Searching for {items} in Amazon.....')
			self.driver.get(self.amazon_url)

			#Getting the Input Box:
			search_inputbox = self.driver.find_element_by_id("twotabsearchtextbox")
			search_inputbox.send_keys(items)
			time.sleep(1)

			#Getting the Button:
			search_button = self.driver.find_element_by_xpath('//*[@id="nav-search"]/form/div[2]/div/input')
			search_button.click()

			time.sleep(1)
			#Getting the Data of First Item(Amazon's Best Choice)
			first_result = self.driver.find_element_by_id('result_0')
			
			data_asin = first_result.get_attribute('data-asin')
			product_url_1 = "https://www.amazon.in/dp/"+data_asin
		
			product_name = self.get_product_name(product_url_1)
			product_price = self.get_product_price(product_url_1)

			urls.append(product_url_1)
			prices.append(product_price)
			name_of_items.append(product_name)

			#Printing in the Terminal:
			print('-------------------------------------------')
			print(f"Product: {product_name} \nUrl: {product_url_1} \nProduct Price: {product_price}")
			print("-------------------------------------------")
			time.sleep(1)

		return urls, prices, name_of_items

	def get_product_name(self,url):
		self.driver.get(url)
		try:
			product_names = self.driver.find_element_by_id('productTitle').text
		except:
			product_names = "Product Name Not Found"

		return product_names

	def get_product_price(self,url):
		self.driver.get(url)
		try:
			prices = self.driver.find_element_by_id("priceblock_ourprice").text
		except:
			prices = self.driver.find_element_by_id("priceblock_dealprice").text

		if prices is None:
			prices = "Price Not Found"
		return prices




