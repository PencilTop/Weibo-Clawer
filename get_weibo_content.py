import os, sys
from urllib import request
import json
import datetime, time

DAYS = 30
RETRYTIMES = 10
PAUSESECONDS = 60
header = ("User-Agent", 
               r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
proxy_addr = "122.241.72.191:808"
url_front = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='

def read_ids(filepath):
    try:
        with open(filepath, 'r') as f:
            for line in f.readlines():
                line = line.strip()
                if line != '':
                    yield line
    except FileNotFoundError:
        print('file {} is not found.'.format(filepath))
    except IOError as e:
        print(e.args)
        print('file {} read file stream error'.format(filepath))
    except Exception as e:
        print(e.args)
        print('no reason error.')

def is_inner_days(daysBefore, dateString):
    today = datetime.date.today()
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

        
def use_proxy(url):
    req = request.Request(url)
    req.add_header(*header)
    proxy = request.ProxyHandler({'http' : proxy_addr})
    opener = request.build_opener(proxy, request.HTTPHandler)
    request.install_opener(opener)
    try:
        return request.urlopen(req).read().decode('utf-8', 'ignore')
    except Exception as e:
        print('url: ',url, '\t请求失败' )
        return 

def get_containerid(url):
    retry = 1
    while True:
        data = use_proxy(url)
        if data is None and retry < RETRYTIMES:
            print("正在进行第", retry, "次重试...")
            time.sleep(PAUSESECONDS)
        elif data is None and retry == RETRYTIMES:
            sys.exit("重试次数已超过最大限制，数据仍无法获取，程序退出。")
        else:
            break
        retry += 1
    content = json.loads(data).get('data')    
    tabsinfo = content.get('tabsInfo')
    if tabsinfo is None:
        return
    else:
        for tab in tabsinfo.get('tabs'):
            if tab.get('tab_type') == 'weibo':
                return tab.get('containerid')

def get_user_info(id):
    url = url_front + id
    data = use_proxy(url)
    content = json.loads(data).get('data')
    userinfo = content.get('userInfo')
    if userinfo is None:
#        print('really invalid id: ', id)
        return 
    else:
        screen_name = userinfo.get('screen_name')
        description = userinfo.get('description')
        profile_url = userinfo.get('profile_url')    
        verified = userinfo.get('verified')
        follow_count = userinfo.get('follow_count')
        profile_image_url = userinfo.get('profile_image_url')
        followers_count = userinfo.get('followers_count')
        gender = userinfo.get('gender')      
        urank = userinfo.get('urank')       
        print("微博昵称：{0}\n微博主页地址：{1}\n微博头像地址：{2}\n\
是否认证：{3} \n微博说明：{4} \n关注人数：{5} \n粉丝数：{6}\n性别：{7}\n \
微博等级：{8}".format(screen_name,
                    profile_url,
                    profile_image_url,
                    verified,
                    description,
                    follow_count,
                    followers_count,
                    gender,
                    urank))   
        return (screen_name, profile_url, profile_image_url, 
                verified, description, int(follow_count), int(followers_count),
                gender, urank)
    
def get_weibo(id):
    contents = []
    i = 1
    while True:
        WillContinue = True
        url = url_front + id
        containerid = get_containerid(url)
        if containerid is None:
            print(id, "找不到containerid，不是有效的ID。")
            break
        print("containerid:", containerid)
        weibo_url = url_front + id + '&containerid=' + containerid + '&page=' + str(i)
        retry = 1
        while True:
            data = use_proxy(weibo_url)
            if data is None and retry < RETRYTIMES:            
                print("正在进行第", retry, "次重试...")
                time.sleep(PAUSESECONDS)
            elif data is None and retry == RETRYTIMES:
                sys.exit("重试次数已超过最大限制，数据仍无法获取，程序退出。")
            else:
                break
            retry += 1
        content = json.loads(data).get('data')
        cards = content.get('cards')
        cardsnum = len(cards)
        if cards is None or cardsnum == 0:   
            print("id:", id, "微博内容获取结束。")
            break
        for j in range(cardsnum):
            print("-----正在爬取第", i, "页，第" , j+1, "条微博")
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
                contents.append((created_at, int(attitudes_count),int(comments_count),
                       int(reposts_count), scheme, text))
        i += 1        
        if not WillContinue:
            break  
    return contents       
    
        
                                
if __name__=='__main__':  
    for id in read_ids('id.txt'):
        info = get_user_info(id)
        print('-'*80)
        print(info)
#        print(use_proxy(url_front + id))
        print('-'*80)
        contents = get_weibo(id)
        print('-'*80)
        print(contents)
        print('\n'*3)
        time.sleep(3)


    
    
    
    
    
    
    
    
    
    