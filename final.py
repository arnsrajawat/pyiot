import matplotlib.pyplot as plt
import pandas as p
import time
import datetime
import schedule
import serial
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
X=0
def job():
    now=datetime.datetime.now()
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    filename2=str(yesterday)
    path ="/home/pi/"+filename2+".csv"
    df= p.read_csv(path)
    plt.figure(1)
    plt.subplot(221)
    pl=df.plot(x='TIME',y='POWER',color='red')
    plt.xlabel('TIME')
    plt.ylabel('POWER')
    plt.title('FLUXGEN ENERGY  MONITORING')
    plt.subplot(222)
    pl=df.plot(x='TIME',y='WATER',color='blue')
    plt.xlabel('TIME')
    plt.ylabel('WATER FLOW')
    plt.title('FLUXGEN WATER MONITORING')
    plt.subplot(223)
    pl=df.plot(x='TIME',y='ENERGY',color='green')
    pl=df.plot(x='TIME',y='CURRENT',color='black')
    plt.xlabel('TIME')
    plt.ylabel('ENERGY/CURRENT_red')
    plt.subplot(224)
    pl=df.plot(x='TIME',y='WATER LEVEL',color='red')
    plt.xlabel('TIME')
    plt.ylabel('WATER LEVEL')
    plt.savefig(filename2+".png")
    fromaddr = "fluxgenenergy@gmail.com"
    toaddrs = ['hsgkmurthy@gmail.com','arunsuggi@gmail.com','shivu@fluxgentech.com']
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ','.join(toaddrs)
    msg['Subject'] = "Energy and water"
    body = "Graph for"+" "+"Energy"+" "+filename2
    msg.attach(MIMEText(body, 'plain'))
    filename = filename2+ ".png"
    attachment = open("/home/pi/"+ filename2+ ".png", "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(part)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "9942880143")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddrs, text)
    server.quit()
schedule.every(1).day.at("00:05").do(job)



def job2():
    global X
    ser = serial.Serial('/dev/ttyUSB0', 9600,timeout=5)
    ser.write('E')
    ser.inWaiting()
    y=ser.readline()
    u=y.strip()
    X = float(u)
    
schedule.every(1).day.at("00:00").do(job2)
def job3():
    
    yesterday = today - datetime.timedelta(days=1)
    filename2=str(yesterday)
    fromaddr = "fluxgenenergy@gmail.com"
    toaddrs = ['arunsuggi@gmail.com','shivu@fluxgentech.com']
 
    msg = MIMEMultipart()
 
    msg['From'] = fromaddr
    msg['To'] = ','.join(toaddrs)
    msg['Subject'] = "Energy and water"
 
    body = "Meter value for"+" "+ filename2
 
    msg.attach(MIMEText(body, 'plain'))

    filename = filename2+ ".csv"
    attachment = open("/home/pi/"+filename2+".csv", "rb")
 
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
    msg.attach(part)
 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "9942880143")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddrs, text)
    server.quit()
        
schedule.every(1).day.at("00:10").do(job3)
def job4():
    ser = serial.Serial('/dev/ttyUSB1', 9600,timeout=5)
    ser.write('@')
schedule.every(1).day.at("00:00").do(job4)


while True:
    ser = serial.Serial('/dev/ttyUSB0', 9600,timeout=5)
    ser.write('P')
    ser.inWaiting()
    s=ser.readline()
    P=s.strip()
    c=len(P)
    if c > int(0):
        o=0
    else:
        
        P= float(220.2)
    time.sleep(1)
    ser.write('E')
    ser.inWaiting()
    g=ser.readline()
    E = g.strip()
    d=len(E)
    if d > int(0):
        o=0
    else:
        
        E= float(0.0)
    time.sleep(1)
    ser.write('V')
    ser.inWaiting()
    s=ser.readline()
    V=s.strip()
    e=len(V)
    if e > int(0):
        o=0
    else:
        
        V= float(220.2)
    time.sleep(1)
    ser.write('A')
    ser.inWaiting()
    s=ser.readline()
    A=s.strip()
    z=len(A)
    if z > int(0):
        o=0
    else:
        
        A= float(1.2)
    time.sleep(1)
    ser = serial.Serial('/dev/ttyUSB1', 9600,timeout=5)
    ser.write('$')
    ser.inWaiting()
    s=ser.readline()
    W=s.strip()
    g=len(W)
    if g > int(0):
        o=0
    else:
        
        W= float(0.0)
    ser = serial.Serial('/dev/ttyUSB2', 9600,timeout=5)
    ser.write('L')
    ser.inWaiting()
    s=ser.readline()
    t=s.strip()
    b=len(t)
    if b > int(0):
        o=0
    else:
        
        t= float(0.0)
    now=datetime.datetime.now()
    timestamp=now.strftime("%Y/%m/%d,%H:%M")
    today = datetime.date.today()
    S = float(E)
    E1 = S-X
    final=str(timestamp)+","+str(V)+","+str(A)+","+str(P)+","+str(E1)+","+str(W)+","+str(t)
    print final
    filename1=str(today)
    f=open(filename1 +".csv","a")
    f=open(filename1 +".csv","r+")
    data=f.read()
    n=len(data)
    e=int(n)
    if e<= int(0):
        f.write("DATE"+","+"TIME"+","+"VOLTAGE"+","+"CURRENT"+","+"POWER"+","+"ENERGY"+","+"WATER"+","+"WATER LEVEL")
        f.write("\n")
    else:
        f.write(str(final))
        f.write("\n")
        f.close()
    time.sleep(5)
    schedule.run_pending()
    ser.flushInput()
    ser.flushOutput()
        
        


