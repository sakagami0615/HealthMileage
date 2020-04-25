# ----------------------------------------------------------------------------------------------------
# モジュールフォルダのパスを追加
# ----------------------------------------------------------------------------------------------------
import os, sys
if sys.path.count('api/module') == 0:
	if os.path.basename(os.getcwd()) == 'HealthMileage':
		sys.path.append('api/module')
	elif os.path.basename(os.getcwd()) == 'api':
		os.chdir('../')
		sys.path.append('api/module')
	else:
		exit()


# ----------------------------------------------------------------------------------------------------
# モジュールimport
# ----------------------------------------------------------------------------------------------------
import datetime
import math
import random
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary

from module.Health import HealthUtility

from module.Health.HealthParam import Param as HEALTHPARAM
from module.Health.HealthXPath import XPath as XPATH



# ----------------------------------------------------------------------------------------------------
# Driverクラス
# ----------------------------------------------------------------------------------------------------
class HealthDriver:

	def __init__(self):

		self.driver = None

	
	# ----------------------------------------------------------------------------------------------------
	# Seleniumのドライバを開く
	# ----------------------------------------------------------------------------------------------------
	def OpenDriver(self):

		chrome_options = Options()
		chrome_options.add_argument('--headless')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_argument('--disable-dev-shm-usage')
		self.driver = webdriver.Chrome(chrome_options=chrome_options)
	
	
	# ----------------------------------------------------------------------------------------------------
	# Seleniumのドライバを閉じる
	# ----------------------------------------------------------------------------------------------------
	def CloseDriver(self):

		self.driver.close()


	# ----------------------------------------------------------------------------------------------------
	# サイトにログインする
	# ----------------------------------------------------------------------------------------------------
	def Login(self, login_id, login_pswd):

		print('■ Access HomePage')
		self.driver.get(HEALTHPARAM.PEPUP_HOME_URL)
		HealthUtility.Sleep()

		# 既にログインされているかを判定
		print('■ Login')
		meta = self.driver.find_element_by_xpath(XPATH.LOGIN_CHECK_DESC)
		if meta.get_attribute('content') == XPATH.LOGIN_CHECK_CONTENT:
			print('  >> Success')
			return True

		# ログイン処理
		self.driver.find_element_by_xpath(XPATH.LOGIN_EMAIL).send_keys(str(login_id))
		HealthUtility.Sleep('delta')
		self.driver.find_element_by_xpath(XPATH.LOGIN_PSWD).send_keys(str(login_pswd))
		HealthUtility.Sleep('delta')
		
		self.driver.find_element_by_xpath(XPATH.LOGIN_COMMIT).click()
		HealthUtility.Sleep()
		
		# ログイン成功確認
		meta = self.driver.find_element_by_xpath(XPATH.LOGIN_CHECK_DESC)
		if meta.get_attribute('content') == XPATH.LOGIN_CHECK_CONTENT:
			print('  >> Success')
			return True

		print('  >> Failuer')
		return False


	# ----------------------------------------------------------------------------------------------------
	# わくわくマイレージのページにアクセスする
	# ----------------------------------------------------------------------------------------------------
	def AccessMileage(self):
		
		print('■ Access InputMileage')
		self.driver.find_element_by_xpath(XPATH.MILLAGE_ACCESS).click()
		HealthUtility.Sleep()
	