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
from module.Mailler.MaillOrder import MaillOrder
from module.Mailler.MaillExtractor import MaillExtractor
from module.Mailler import MailUtility

from module.Mailler.MaillParam import Param as MAILPARAM


# ----------------------------------------------------------------------------------------------------
# テストコード
# ----------------------------------------------------------------------------------------------------
def TestMailSend():
	
	mailer = MaillOrder()

	to = mailer.GetLoginAdress()
	subject = MailUtility.ConvertFormattedSubject('TEST : TestMailSend()')
	body = 'process test program'
	mailer.SendMail(to, subject, body)

	print('-'*20)
	print(to)
	print(subject)
	print(body)
	print('-'*20)


if __name__ == '__main__':
	TestMailSend()
	