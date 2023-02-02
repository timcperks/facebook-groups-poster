from selenium import webdriver
from time import sleep
import random
import os
from pyperclip import copy as clipCopy
from sys import argv
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

# Save the group URL
groups = []

# The URLs with Errors will be add to here
error_url = []

# String to hold the message sege from the txt file
msg = ""

# This list will hold the login Information taken from a txt file
login = []

user_acc = 0

# Google Chrome Driver
driver = None

# images Folder
imgFolder = ''
images = []

def refreshUsers() :
    '''
    get users 
    '''
    global login
    login = []
    # Grab usernames & passwords
    with open('signin.txt', 'r', encoding='UTF-8') as txt :
        for line in txt :
            login.append(line.split(','))

    # printing all users 
    print('All users : ')
    for i in range(len(login)) :
        print(i, login[i][0])
        
def selectUser() :
    '''
    select the acc you want to use 
    '''
    global user_acc, login
    if len(login) :
        try :
            user_acc = int(input("\nSelect a user ID : write -1 to sign-in manually"))
        except :
            print('Bad entry, Sign-in manually')
            user_acc = -1
    else :
        user_acc = -1
        print('No sign-in information found, Please sign-in manually')

    if not user_acc : user_acc = -1
            
def urlUpdate(urlFile='') :
    '''
    update groups file 
    '''
    if(len(urlFile) == 0) :
        urlFile = 'liteURL'

    global groups
    groups = []
    # Grab the URLs
    with open(urlFile+".ebd3", 'r', encoding='UTF-8') as txt :
        for line in txt :
            groups.append(line.split(',')[0])
    
    # print number of urls to visit
    print("I will post to ", len(groups),' groups\n')

def msgUpdate(msgFile='') :
    '''
    select msg file 
    '''
    #msgFile = input('write message file name (Text)')
    if(len(msgFile) == 0) :
        msgFile = 'Text'

    global msg
    msg = ''
    # Grab the message
    with open(msgFile+'.txt', 'r', encoding='UTF-8') as txt :
        for line in txt :
            line = line.replace('\t', '     ')
            msg += line

def imgUpdate(folder = '') :
    '''
    select img file
    '''
    #imgFolder = input('write img file name (images)')

    if(len(folder) == 0) :
        folder = 'images'
    
    # Collect images
    global images, imgFolder
    imgFolder = folder

    images = []
    for (_, _, files) in os.walk(folder) :
        images += files

def connect(headless=0) :
    global driver
    global login
    # Select users
    refreshUsers()
    selectUser()
    # Create Chrome Option object
    options = webdriver.ChromeOptions()

    # This options will help selenium bypass cloudflare
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    if headless : options.add_argument("headless")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
        Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
        })
    """
    })

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})


    # go to facebook.com site
    driver.get('https://mbasic.facebook.com/login/save-device/cancel/?flow=interstitial_nux&nux_source=regular_login')
    print("Going to Facebook to sign in ")
    
    if user_acc != -1 :
        driver.find_element_by_name('email').send_keys(login[user_acc][1])
        driver.find_element_by_name('pass').send_keys(login[user_acc][2], Keys.ENTER)

        # This will give you some time to prepare the browser
        print("User logged in successfully, press any key to continue")
    else :
        print("please login manually")

def updateAll(msg, img, url='') :
    urlUpdate(url)
    msgUpdate(msg)
    imgUpdate(img)

def writePost(group) :
    '''
    post to group using Keys 
    '''
    global driver, images, msg, imgFolder, error_url

    print(group[group.find('f'):group.find('?')],end=":\t") # print the url
    while(1) :
        try :
            driver.get(group) # go to the group

            # make sure you are in the right url
            url_1 = group[group.find('f'):]
            url_2 = driver.current_url[driver.current_url.find('f'):]
            if (url_1 == url_2) :
                break
        except :
            sleep(1)

    try :
        driver.find_element_by_xpath('//*[@id="root"]/div[1]/form/input[3]').click()

    except :
        print("⛔️ error", end=' ')
        if group not in error_url :
            error_url.append(group)
    sleep(2)
def GroupJoinURLS(filename='liteURL'):
    global driver
    while(1) :
        try :
            driver.get(group) # go to the group

            # make sure you are in the right url
            url_1 = group[group.find('f'):]
            url_2 = driver.current_url[driver.current_url.find('f'):]
            if (url_1 == url_2) :
                break
        except :
            sleep(1)

    ids = []
    with open(filename+'.ebd3', encoding='UTF-8') as f:
        for line in f:
            ids.append(line.split(',')[0].split('/')[-1])
    action_id = 'https://mbasic.facebook.com/a/group/join/?group_id={id}&gfid={fid}'
    for id in ids:
        driver.get(action_id.format(id=id))
        sleep(60)
    for id in ids:
        driver.get(action_id.format(id=id))
        sleep(60)       
    
def GroupJoinURLS(group):
    global driver, images, msg, imgFolder, error_url

    print(group[group.find('f'):group.find('?')],end=":\t") # print the url
    while(1) :
        try :
            driver.get(group) # go to the group

            # make sure you are in the right url
            url_1 = group[group.find('f'):]
            url_2 = driver.current_url[driver.current_url.find('f'):]
            if (url_1 == url_2) :
                break
        except :
            sleep(1)

    ids = []
    with open(filename+'.ebd3', encoding='UTF-8') as f:
        for line in f:
            ids.append(line.split(',')[0].split('/')[-1])
    action_id = 'https://mbasic.facebook.com/a/group/join/?group_id={id}'
    for id in ids:
        driver.get(action_id.format(id=id))
        sleep(60)
    
def writePostPaste(group) :
    '''
    post to group using Copy Paste 
    '''
    global driver, images, msg, imgFolder, error_url

    print(group[group.find('f'):group.find('?')],end=":\t") # print the url
    while(1) :
        try :
            driver.get(group) # go to the group

            # make sure you are in the right url
            url_1 = group[group.find('f'):]
            url_2 = driver.current_url[driver.current_url.find('f'):]
            if (url_1 == url_2+'\n') :
                break
        except :
            sleep(1)

    try :

        # Add Images
        for i in range(len(images)) :
            if(i%3 == 0) :
                buttons = driver.find_elements_by_name('view_photo')
                buttons[0].click()
                sleep(1) 
            
            # Click add image
            imgLoc = "D:\\facebook-group-post\\"+imgFolder+"\\"+images[i]
            tagName = 'file'+str(i%3+1)
            buttons = driver.find_elements_by_name(tagName)
            buttons[0].send_keys(imgLoc)
            if (i%3-2 == 0 or i == len(images)-1 ) :
                driver.find_element_by_name('add_photo_done').click()

        sleep(1)
        
        # Add text
        clipCopy(msg)
        sleep(0.5)
        driver.find_element_by_tag_name('textarea').send_keys(Keys.CONTROL+'v')
        sleep(.5)

        # Submit
        buttons = driver.find_elements_by_name('view_post')
        buttons[0].click()
        print("✅ posted", end=' ')
    except :
        print("⛔️ error", end=' ')
        if group not in error_url :
            error_url.append(group)
    sleep(2)

def writeError() :
    global error_url
    with open('error.ebd3', 'w', encoding='UTF-8') as txt :
        for x in error_url :
            txt.write(x)
    print('Urls with errors has been written to error.ebd3')

def writePostToGroups(groups=groups, method=writePost, delay=0, stop=True) :
    print('bulk share will start >>> after the first post sharing you can modify the post ')
    progress = 0
    global error_url
    for group in groups :
        print(groups.index(group), end = '\t')
        method(group)
        progress += 1/len(groups)
        print(str(int(progress*100))+'%')
        sleep(delay)
        if stop :
          print('Write "yes" if you want to continue without stop')
          if input().lower() == 'yes' : stop = False
    writeError()

def collectGroupURLS(filename='liteURL'):
    global driver
    driver.get('https://mbasic.facebook.com/groups/?seemore')
    g_urls = driver.find_elements_by_xpath('//li[@class="bl"]//a')
    with open(filename+'.ebd3', 'w', encoding='UTF-8') as f:
        for u in g_urls:
            href = u.get_attribute('href').replace('https://m', 'https://mbasic')
            f.write(f"{u.get_attribute('href')},{u.text}\n")
    
def blockSolve(i) :
    try :
        driver.get(i)
        driver.find_elements_by_class_name('_56bf')[0].click()
        sleep(5)
        driver.find_elements_by_class_name('_a5o')[9].click()
        sleep(5)
        driver.find_elements_by_class_name('_3gk8')[3].click()
        sleep(5)
        driver.find_elements_by_class_name('_335k')[8].click()
        sleep(2)
        return 1
    except :
        return 0

def collectNotifications(someString = 'ينتهك منشورك معايير مجتمعنا') :
    global driver
    notif = []
    x = []
    driver.get('https://m.facebook.com/notifications.php?no_hist=1')
    driver.find_element_by_class_name('async_elem').click()
    
    while(len(x) < 10) :
        x = driver.find_element_by_id('notifications_list').find_elements_by_class_name('acw')    
        sleep(1)

    for i in x :
        if someString in i.text :
            notif.append(i.find_element_by_tag_name('a').get_attribute('href'))
    return notif

if __name__ == '__main__' :
    print('الأوامر المتاحة')
    print('-'*50)
    print('لبدأ المتصفح')
    print('connect()')
    print('')
    print('تحديد الجميع - ملف نصي للبوست - مجلد للصور - رقم المستخدم المخزن - اسم الملف الحاوي على روابط المجموعات')
    print('updateAll(msg, image folder, Groups url)')
    print('')
    print('يوجد طريقتين للنشر')
    print('')
    print('الطريقة الأولى تحاكي الكتابة على الكيبورد')
    print('writePost(group ID)')
    print('')
    print('الطريقة الثانية نسخ و لصق من الضروري جداً إستخدام تأخير عند النشر الجماعي بهذه الطريقة')
    print('writePostPaste(group ID)')
    print('')
    print('للنشر بشكل جماعي')
    print('writePostToGroups(groups List, method to use writePost is default, delay 0 is default, stop default is True)')
    print('')
    print('-'*50)
    print('متغيرات مهمة - هذه المتغيرات تتحدد بعد تطبيق أمر updateALL')
    print('')
    print('groups يحوي المجموعات التي تم إستخراجها من الملف')
    print('images يحوي عناوين الصور التي تتواجد في المجلد المحدد')
    print('msg يحوي النص المستخرج')
    print('-'*50)
    print('يمكنك أيضاً تحديد البيانات بشكل فردي')
    print('')
    print('لتحديد نص المنشور')
    print('msgUpdate(File name)')
    print('')
    print('مجلد الصور')
    print('imgUpdate(Folder name)')
    print('')
    print('المستخدم - هذا الأمر ضروري فقط في حالة أردت إستخدام نظام تسجيل الدخول الآلي')
    print('selectUser(User ID)')
    print('')
    print('ملف الروابط إذا لم تحدده سيتم إستخدام الملف الإفتراضي liteURL.ebd3')
    print('urlUpdate(File name)')
    
if len(argv) > 3 :
    updateAll(argv[1], argv[2], argv[3])
    connect()
    sleep(5)
    if (argv[4] == 'paste') :
        writePostToGroups(groups, writePostPaste, 0)
    else :
        writePostToGroups(groups)
    sleep(3)
    
    while(len(error_url) > 8) :
        groups = error_url[:]
        error_url = []
        writePostToGroups(groups)
    
    while(1) :
        blocks = collectNotifications()
        if len(blocks) != 0 :
            for notif in blocks :
                blockSolve(notif)
        else :
            break

    driver.quit()
    exit()
