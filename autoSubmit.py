from selenium import webdriver
import time
import http.client 
import urllib.request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import sys
from selenium.webdriver.chrome.options import Options
# 打开浏览器

def submit(username,password):
    try:
        chrome_opt = webdriver.ChromeOptions()
        No_Image_loading = {"profile.managed_default_content_settings.images": 2}
        chrome_opt.add_experimental_option("prefs", No_Image_loading)

        wd =webdriver.Chrome(chrome_options=chrome_opt)
        wd.set_window_size(1280,1000)
        wd.implicitly_wait(30)#隐式等待
        wd.get('https://ehall.jlu.edu.cn/sso/login')
       
        #time.sleep(10)
        wd.find_element_by_name('username').send_keys(username)
        wd.find_element_by_name('password').send_keys(password)
        wd.find_element_by_id('login-submit').click()
        print('clicked')
        wd.get('https://ehall.jlu.edu.cn/infoplus/form/JLDX_BK_XNYQSB/start')
        time.sleep(1)
        print(wd.current_url)#打印当前的url
        wd.get(wd.current_url)
        time.sleep(3)
        print('聚焦')

        js = "window.scrollTo(0,document.body.scrollHeight)" 
        wd.execute_script(js)

        wd.find_element_by_name('fieldCNS').click()
        print('2clicked')
        wd.find_element_by_class_name('command_button_content').click()
        time.sleep(1)
        wd.find_element_by_xpath('/html/body/div[7]/div/div[2]/button[1]').click()
        time.sleep(4)
        wd.find_element_by_xpath('/html/body/div[8]/div/div[2]/button').click()
        time.sleep(5)
        out=username+"="+time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time()))+".jpg"
        wd.save_screenshot(out)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        print('clear')
        wd.quit()
        return out
    except:
        wd.quit()
        return 'NULL='
#发送邮件函数
def send(sender,receivers,code,img,text):
    message =  MIMEMultipart('related')
    subject = text
    message['Subject'] = text
    message['From'] = sender
    message['To'] = receivers
    content = MIMEText('<html><body><img src="cid:imageid" alt="imageid"></body></html>','html','utf-8')
    message.attach(content)

    file=open(img, "rb")
    img_data = file.read()
    file.close()

    img = MIMEImage(img_data)
    img.add_header('Content-ID', 'imageid')
    message.attach(img)

    try:
        server=smtplib.SMTP_SSL("smtp.qq.com",465)
        server.login(sender,code)
        server.sendmail(sender,receivers,message.as_string())
        server.quit()
        print ("邮件发送成功")
    except smtplib.SMTPException as e:
        print(e)


with open('inf.txt', 'r') as f:
    list = f.readlines()
for i in range(0, len(list)):
    list[i] = list[i].rstrip('\n')
#人数    
num =len(list)
#错误信息最多重试次数
times=3
failTime=0
success=0
code='qq邮箱码'
sender='1584160851@qq.com'
#授权码

for i in range(num):
    failTime=0
    for j in range(times):
        name=list[i].split(" ")[0]
        password=list[i].split(" ")[1]

        fileName=submit(name,password)
        t=fileName.split("=")[0]
        if  t is not 'NULL':
            for k in range(0, len(list)):
                print(list[k].split(" ")[0]+"xx"+t+str(list[k].split(" ")[0] == t))
                if list[k].split(" ")[0] == t:
                    print(str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))\
                          +"通知qq:"+list[k].split(" ")[2]+'-'+str(fileName.split("=")[1]))
                    
                    receivers=list[i].split(" ")[2]
                    img=fileName
                    text=str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))\
                          +"通知qq:"+list[k].split(" ")[2]+"-"+str(fileName.split("=")[1])
                    #授权码
                    send(sender,receivers,code,img,text)
                    failTime=0
                    success=success+1
                    break
            break
        else :
            failTime =failTime+1
            receivers=list[i].split(" ")[2]
            img='fail.jpg'
            text='fail '
            #授权码
            send(sender,receivers,code,img,text)
            if failTime == times -1:#每次发送都失败
                with open('fail.txt', 'w+') as ff:
                    ff.write(time.strftime('%Y-%m-%d %H:%M:\
                    %S',time.localtime(time.time()))+":"+"\n"+"\t"+name)
print("成功"+str(success))
print("失败"+str(num-success))

            

        
