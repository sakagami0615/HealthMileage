from selenium import webdriver
from selenium.webdriver.chrome.options import Options



def TestSelenium():

	chrome_options = Options()
	chrome_options.add_argument('--headless')
	chrome_options.add_argument('--no-sandbox')
	chrome_options.add_argument('--disable-dev-shm-usage')

	"""
	Sample test
	"""
	d = webdriver.Chrome(options=chrome_options)
	d.get('https://www.google.com')
	print(d.title)
	d.quit()


if __name__ == '__main__':
	TestSelenium()
	
