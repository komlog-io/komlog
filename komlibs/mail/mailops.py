#coding: utf-8

'''

This file group mail operations related functions and classes


2013/07/30

'''

import smtplib 

fromaddr = ':romuser@gmail.com'  
toaddrs  = 'touser@gmail.com'  
msg = 'There was a terrible error that occured and I wanted you to know!'  
  
  
# Credentials (if needed)  
username = 'username'  
password = 'password'  
  
# The actual mail send  
server = smtplib.SMTP('smtp.gmail.com:587')  
server.starttls()  
server.login(username,password)  
server.sendmail(fromaddr, toaddrs, msg)  
server.quit()  
