import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
from pprint import pprint
from collections import OrderedDict
import time
import re
import pymysql
from DBadmin import DBadmin
from DBadmin import insert_detail_multiple_tb
from DBadmin import insert_to_msg_tb
from random import choice
import configparser


#————————————————————————————————————————————————————————
#                     读取配置文件                       |
#————————————————————————————————————————————————————————
#数据库配置信息
cf = configparser.ConfigParser()
cf.read(r"QCC\version2\config.conf", encoding='utf-8')
port = int(cf.get('db','db_port'))
host = cf.get('db','db_host')
user = cf.get('db','db_user')
pwd = cf.get('db','db_pwd')
db = cf.get('db','db_database')
#爬虫配置信息
total = int(cf.get('crawler','total'))
begin = int(cf.get('crawler','begin'))
end = int(cf.get('crawler','end'))
#配置文件路径
path = cf.get('file','config_file_path')
#————————————————————————————————————————————————————————


#————————————————————————————————————————————————————————
#                      数据库管理                        |
#————————————————————————————————————————————————————————
DB = DBadmin(user,pwd,db,port=port)
#实例化类对象 传入用户名，密码，数据库名
database = DB.connect()
select_cursor = database.cursor()  #选取游标
#————————————————————————————————————————————————————————
#我也不知道为什么反正我实例化的游标不能用，那就再整一个游标  |
#————————————————————————————————————————————————————————
db = pymysql.connect(host=host,user=user,password=pwd,port=port,db=db)
insert_cursor = db.cursor()   #插入游标
#————————————————————————————————————————————————————————


def get_detail_html(url:str) -> 'html':
    """Request URL and Return Html"""
    try:
        headers = {'User-Agent':
            "Mozilla/5.0 (Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59"
        }
        # print('—' * 100)
        print('\033[1;33m使用代理：\033[0m None')
        print('—' * 100)
        response = requests.get(url,headers=headers,timeout=5)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException as e:
        return f'We meet some error {e}'
    except TimeoutError as e:
        return f'TIME OUT {e}'


def parse_detail_html(html:str) -> dict:
    """Parse Html Return Uncleaned Dict"""
    try:
        soup = BeautifulSoup(html,'lxml')
        #实例 soup对象
        name = soup.find(name='h1').get_text()
        keys = soup.find(name='table',attrs={'class':'ntable'}).find_all(name='td',attrs={'class':'tb'})
        #筛选字典 key
        values = soup.find(name='table',attrs={'class':'ntable'}).find_all(name='td')
        #筛选字典 value
    except AttributeError as e:
        print(f"We can't get this page... | Error:{e}")
        # raise UserWarning
    else: 
        key = [i.get_text().strip() for i in keys]
        #生成 key值
        value = [i.get_text().strip() for i in values]
        #生成未清洗 value值
        data = OrderedDict()
        #创建有序字典
        for v in value:
            #清洗 value创建字典
            if v in key:
                data[v] = value[int(value.index(v))+1]
            else:
                continue
        data['company_name'] = name
        return data


def parse_data(dirt_data) -> dict:
    """Clean Dict and Return OrderedDict"""
    data = OrderedDict()
    try:
        for k,v in dirt_data.items():
            special_word = ['法定代表人','投资人','经营者']
            if k not in special_word:
                data[k] = re.sub('[查看地图,附近企业,\n,关联,家企业,>,*,最新年报址]', '', v).strip()
                #清洗 value
            else:
                v = re.sub('[查看地图,附近企业,\n,关联,家企业,>,*]', '', v).strip()
                num = ['1','2','3','4','5','6','7','8','9','0']
                while v[-1] in num:
                    v = v[0:-1]
                data[k] = v.strip()
        return data
    except:
        return "We can't parse data."


def parse_company_url(html) -> list:
    """Parse Html Return Name and Link"""
    try:
        soup = BeautifulSoup(html,'lxml')
        result = soup.find(name='div',attrs={'class':'npanel'}).find_all(name='div',class_="title")
    except AttributeError as e:
        print(f"We can't get this page... | Error:{e}")
    else:
        for i in result:
            link = i.a.attrs['href']
            name = i.get_text()
            yield name,link


def get_random_proxy():
    """
    get random proxy from proxypool
    :return: proxy
    """
    proxypool_url = 'http://192.168.153.128:5555/random'
    proxy = requests.get(proxypool_url).text.strip()
    proxies = {'http': 'http://' + proxy}
    return proxies


def main(total,begin,end=1000000):
    """Main Program"""
    times = 1
    print('\033[1;33m状态：正在从目录中读取条目\033[0m')
    _index = begin #设置索引
    for url in DB.select(select_cursor,total,begin,end):
        """从数据库中取出url"""
        if times%10 == 0:
            print('\033[1;31m   -----进程阻塞中-----   \033[0m')
            print('—' * 100)
            time.sleep(20)            
        try:
            # proxies = get_random_proxy()   #获取代理
            html = get_detail_html(url)     #请求
            dirt_data = parse_detail_html(html)     #获取脏数据  
            data = parse_data(dirt_data)    #清洗数据
            print('\033[4;35m公司信息:\033[0m')
            pprint(data)
            insert_detail_multiple_tb(insert_cursor,db,data) #写入 Data
        except:
            print('\033[1;31mALL operation failed\033[0m')
            pass
        else:
            print('—' * 100)
            print(f'\033[1;33m计次：{times}\033[0m') ; times += 1
            print('—' * 100)

            # delay = [1.3,1.4,1.5,1.6,1.7,1.8,1.9]
            # time.sleep(choice(delay))
            # time.sleep(2.5)

            print('\033[4;35m目录存储状况:\033[0m')
            for i in parse_company_url(html):
                """分析页面中可能存在的公司URL"""
                # print(i[0],i[1])
                insert_to_msg_tb(insert_cursor,db,i[0],i[1])
            print('—' * 100)

            _index += 1
            cf.set('crawler','begin',str(_index))
            cf.write(open(path, 'w')) #写入配置文件
    database.close()


if __name__ == '__main__':
    main(total,begin,end) #运行