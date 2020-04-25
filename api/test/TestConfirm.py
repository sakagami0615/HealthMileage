# ----------------------------------------------------------------------------------------------------
# モジュールフォルダのパスを追加
# ----------------------------------------------------------------------------------------------------
import os, sys
if os.path.basename(os.getcwd()) == 'HealthMileage':
	sys.path.append('api')
elif os.path.basename(os.getcwd()) == 'test':
	os.chdir('../../')
	sys.path.append('api')
elif os.path.basename(os.getcwd()) == 'api':
	os.chdir('../')
	sys.path.append('api')
else:
	exit()


# ----------------------------------------------------------------------------------------------------
# モジュールimport
# ----------------------------------------------------------------------------------------------------
from module.Health.HealthRunConfirm import HealthRunConfirm

# ----------------------------------------------------------------------------------------------------
# テストコード
# ----------------------------------------------------------------------------------------------------
def TestConfirm():

	confirm = HealthRunConfirm()
	(is_success, ack_message) = confirm.RunConfirm()
	print(ack_message)


if __name__ == '__main__':
	TestConfirm()
