 # -*- coding: utf-8 -*-

import os, sys
import urllib.request
import json
import datetime
import time

def read_ids(file):
    f = open(file, 'r')
    for line in f.readlines():
        l = line.rstrip()
        if l  != '':
            yield l
    f.close()

#定义页面打开函数
def use_proxy(url, proxy_addr):
    req = urllib.request.Request(url)
    req.add_header("User-Agent", r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
    proxy=urllib.request.ProxyHandler({'http' : proxy_addr})
    opener=urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    try:
        data=urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
    except:
        return ''
    return data

#获取微博主页的containerid，爬取微博内容时需要此id
def get_containerid(url):
    data = use_proxy(url, proxy_addr)
    if data != '':
        try:
            content=json.loads(data).get('data')
        except:
            return ''
    else:
        return ''
    for data in content.get('tabsInfo').get('tabs'):
        if( data.get('tab_type') == 'weibo' ):
            containerid = data.get('containerid')
    return containerid

#获取微博大V账号的用户基本信息，如：微博昵称、微博地址、微博头像、关注人数、粉丝数、性别、等级等
def get_userInfo(id):
    url='https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
    data = use_proxy(url, proxy_addr)
    if data != '':
        content = json.loads(data).get('data')
        userinfo = content.get('userInfo')
    else:
        return 1
    if userinfo is None:
        print('invalid id: ', id)
        return 1
    name = content.get('userInfo').get('screen_name')
   
    """
    description = content.get('userInfo').get('description')
    profile_url = content.get('userInfo').get('profile_url')
    verified = content.get('userInfo').get('verified')
    guanzhu = content.get('userInfo').get('follow_count')
    profile_image_url = userinfo.get('profile_image_url')
    fensi = content.get('userInfo').get('followers_count')
    gender = content.get('userInfo').get('gender')
    urank = content.get('userInfo').get('urank')
    print("微博昵称："+name+"\n"+"微博主页地址："+profile_url+"\n"+"微博头像地址："+profile_image_url+"\n"+"是否认证："+str(verified)+"\n"+"微博说明："+description+"\n"+"关注人数："+str(guanzhu)+"\n"+"粉丝数："+str(fensi)+"\n"+"性别："+gender+"\n"+"微博等级："+str(urank)+"\n")
    """
    print("微博昵称："+name)
    return 0

def is_inner_days(daysBefore, dateString):
    today = datetime.date.today()
    createDate = None
    if len(dateString.split('-')) == 2:
        dateString = str(today.year) + '-' + dateString
    timeFormat = '%Y-%m-%d'

    if("-" in dateString):
        createDate = datetime.datetime.strptime(dateString, timeFormat).date()
    else:
        createDate = datetime.date.today()
    interval = today - createDate
    if interval.days > daysBefore:
        return False
    else:
        return True

#获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等
def get_weibo(id, file):
    i=1
    while True:
        WillContinue = True
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
        if get_containerid(url) != '':
            print(get_containerid(url))
        else:
            print('invalid id ^v^: ', id)
            break
        weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + '&containerid=' + get_containerid(url) + '&page=' + str(i)
        data = use_proxy(weibo_url ,proxy_addr)
        if data != '':
            content = json.loads(data).get('data')
        else:
            continue
        cards = content.get('cards')
        if(len(cards) > 0):
            for j in range(len(cards)):
                print("-----正在爬取第" + str(i) + "页，第" + str(j+1) + "条微博------")
                card_type=cards[j].get('card_type')
                if(card_type == 9):
                    mblog = cards[j].get('mblog')
                    attitudes_count = mblog.get('attitudes_count')
                    comments_count = mblog.get('comments_count')
                    created_at = mblog.get('created_at')
                    if not is_inner_days(DAYS, created_at):
                        WillContinue = False
                        break
                    reposts_count = mblog.get('reposts_count')
                    scheme = cards[j].get('scheme')
                    text = mblog.get('text')
                    
            i += 1
        else:
            break

        if not WillContinue:
            break

if __name__=="__main__":
    DAYS = 30
    proxy_addr = "122.241.72.191:808"
    idfile = "id.txt"
    
    t = 1
    for id in read_ids(idfile):
        print('\n')
        print('************************爱爬微博  Begin**********************')
        file = id + '.txt'
        open(file, 'w').close()
        if get_userInfo(id) != 0:
            os.rename(file, file[:-4] + '(空)' + file[-4:])
            continue
        get_weibo(id, file)
        print('************************爱爬微博 End************************')
        if t < 6:
            time.sleep(2)
            t += 1
        else:
            time.sleep(30)
            t = 1
            
            
            
            
            
            
            
            
            
            
            
            
        
        
