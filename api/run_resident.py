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
import time
import module.Main.resident as Resident


# ----------------------------------------------------------------------------------------------------
# 定数パラメータ
# ----------------------------------------------------------------------------------------------------
# 再起動までの待機時間
WAIT_RESTART_MIN = 10
WAIT_RESTART_SEC = WAIT_RESTART_MIN*60

# 再起動許容回数
MAX_RESTART_NUM = 10


# ----------------------------------------------------------------------------------------------------
# main function
# ----------------------------------------------------------------------------------------------------
if __name__ == '__main__':

	for count in range(MAX_RESTART_NUM):

		if count == 0:
			print('----------------------------------------')
			print('常駐システムを起動')
			print('----------------------------------------')
		else:
			print('----------------------------------------')
			print('常駐システムを再起動')
			print('----------------------------------------')
		
		Resident.Run()

	print('----------------------------------------')
	print('timeout {} minute [{}/{}]'.format(WAIT_RESTART_SEC, count + 1, MAX_RESTART_NUM))
	print('----------------------------------------')
	time.sleep(WAIT_RESTART_SEC)