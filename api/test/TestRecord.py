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
from module.Health.HealthRunRecord import HealthRunRecord


# ----------------------------------------------------------------------------------------------------
# テストコード
# ----------------------------------------------------------------------------------------------------
def TestRecord():

	record = HealthRunRecord()
	(is_success, ack_message) = record.RunRecord()
	print(ack_message)

if __name__ == '__main__':

	TestRecord()

