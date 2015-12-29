import smtplib, os, urllib2, csv, sys, re
from smtplib import SMTPException

request = urllib2.urlopen("http://checkip.dyndns.org").read()
ip = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", request)

parameters = csv.reader(open('checkip.csv','rb'), delimiter=',')
parameters = next(parameters)

if ip[0] != parameters[2]:
	print "IP address has changed"
	parameters[2] = ip[0]

	message = """From: From Yun
To: To Yun 
Subject: IP Check
ip has changed to %s
""" %(parameters[2])

	try:
		session = smtplib.SMTP('smtp.gmail.com', 587)
		session.ehlo()
		session.starttls()
		session.ehlo()
		session.login(parameters[0],parameters[1])
		session.sendmail(parameters[0], [parameters[0]], message)
		session.quit()
		
		writer = csv.writer(open('checkip.csv', 'w'))
		writer.writerows([parameters])
		print "Successfully sent email"
	except SMTPException:
	   print "Error: unable to send email"