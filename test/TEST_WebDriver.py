import os, sys
if os.path.basename(os.getcwd()) == 'test':
	os.chdir('../../')
	sys.path.append('HealthMileageBot')
elif os.path.basename(os.getcwd()) == 'HealthMileageBot':
	os.chdir('../')
	sys.path.append('HealthMileageBot')
else:
	exit()


from src.WebDriver import WebDriver


def TEST_WebDriver():
	
	URL = 'https://pepup.life/users/sign_in'

	web_driver = WebDriver(is_hidden=False)

	try:
		web_driver.driver.get(URL)
		page_source = web_driver.driver.page_source
	except:
		return False, None
	
	return True, page_source




if __name__ == '__main__':

	print()
	print('-'*50)
	print('TEST_ParseInputMessage BEGIN')
	print('-'*50)

	result_flg, page_source = TEST_WebDriver()
	print('success flag : {}'.format(result_flg))

	print('-'*50)
	print('TEST_ParseInputMessage END')
	print('-'*50)
	print()