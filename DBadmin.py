import pymysql

class DBadmin():
    """
    :user:数据库用户名
    :password:数据库密码
    :dbname:数据库名
    :host:数据库地址 默认localhost
    :port:端口 默认3306
    """

    def __init__(self,user:str,password:str,dbname:str,host="192.168.0.105",port=3306) -> None:
        self.user = user
        self.password = password
        self.dbname = dbname
        self.host = host
        self.port = port


    def connect(self) -> object:
        """
        Connect to database
        无需传入直接调用方法即可
        """
        try:
            db = pymysql.connect(host=self.host,user=self.user,password=self.password,port=self.port,db=self.dbname)
        except:
            raise UserWarning
        return db

    
    def select(self,cursor,times,begin=1,end=100000000) -> str:
        """
        Query Message input curor and times
        :cursor: 传入数据库游标
        :times: 传入查询条数
        :begin: 传入x,从第x条开始查询（可选）
        :end: 传入y,到第y条结束（可选）
        """
        self.cursor = cursor
        SQL = "SELECT company_url FROM company_msg LIMIT %s,%s"
        try:
            self.cursor.execute(SQL,(begin,end))
        except:
            print('\033[1;31mGet Data from Database Error\033[0m')
            pass
        else:
            for i in range(1,int(int(times)+1)):
                try:
                    for col in self.cursor.fetchone():
                        yield 'https://www.qcc.com' + col
                except TypeError:
                    break
                # return None
            

    def insert_to_msg_tb(self,cursor,dbobj,name,url) -> str:
        """
        Insert Message to company_msg table
        :cursor: 传入游标
        :dbobj: 传入实例化的数据库对象
        :name: 传入公司名字段
        :url: 传入公司url字段
        """
        self.cursor = cursor
        self.dbobj = dbobj
        self.company_name = name
        self.company_url = url
        SQL = "INSERT INTO company_msg(company_name,company_url) VALUES(%s,%s)"
        try:
            self.cursor.execute(SQL,(self.company_name,self.company_url))
            self.dbobj.commit()
        except:
            print("保存至数据库失败")
            self.dbobj.rollback()
            # return None
        # self.dbobj.close()
        # return None


def insert_to_msg_tb(cursor,dbobj,name,url) -> str:
    """
    Insert Message to company_msg table
    :cursor: 传入游标
    :dbobj: 传入实例化的数据库对象
    :name: 传入公司名字段
    :url: 传入公司url字段
    """
    cursor = cursor
    dbobj = dbobj
    company_name = name
    company_url = url
    SQL = "INSERT INTO company_msg(company_name,company_url) VALUES(%s,%s)"
    try:
        cursor.execute(SQL,(company_name,company_url))   #存入数据库
        dbobj.commit()
        print('\033[1;32mSave Success.\033[0m')
    except:
        print('\033[1;31mFail to Save Message into Content\033[0m')
        dbobj.rollback()
        # return None
    # self.dbobj.close()
    # return None


def insert_detail_multiple_tb(cursor,dbobj,data:dict) -> str:
    """
    Insert Detail to company_detail table
    Insert Code to company_code table
    Insert Introduction to company_intro table
    :cursor: 传入游标
    :dbobj: 传入实例化数据库对象
    :data: 传入数据字典
    """

    """定义语句"""
    SQL_to_detail = ('INSERT INTO company_detail VALUE(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
    SQL_to_code = ('INSERT INTO company_code VALUE(%s,%s,%s,%s,%s)')
    SQL_to_intro = ('INSERT INTO company_intro VALUE(%s,%s)')
    SQL_update_detail = ("""UPDATE company_detail SET company_name=%s,
    credit_code=%s,law_agent=%s,company_status=%s,start_date=%s,
    operate_period=%s,company_type=%s,reg_capital=%s,contribute_capital=%s,
    staff_size=%s,related_field=%s,address=%s WHERE company_name=%s""")
    SQL_update_code = ("""UPDATE company_code SET company_name=%s,credit_code=%s,
    org_code=%s,ie_org_code=%s,reg_num=%s WHERE company_name=%s""")
    SQL_update_intro = ("""UPDATE company_intro SET company_name=%s,company_intro=%s WHERE company_name=%s""")
    SQL_check_key_close = ("""SET foreign_key_checks = 0""")
    SQL_check_key_open = ("""SET foreign_key_checks = 1""") 
    
    try:
        """赋值模块"""
        company_name = data['company_name']
        if list(data.keys())[0] == '法定代表人':
            law_agent = data['法定代表人']
        elif list(data.keys())[0] == '投资人':
            law_agent = data['投资人']
        elif list(data.keys())[0] == '负责人':
            law_agent = data['负责人']
        else:
            law_agent = data[list(data.keys())[0]]
        company_status = data['经营状态'] if data['经营状态'] != '-' else None
        start_date = data['成立日期'] if data['成立日期'] != '-' else None
        operate_period = data['营业期限'] if data['营业期限'] != '-' else None
        company_type = data['企业类型'] if data['企业类型'] != '-' else None
        reg_capital = data['注册资本'] if data['注册资本'] != '-' else None
        contribute_capital = data['实缴资本'] if data['实缴资本'] != '-' else None
        staff_size = data['人员规模'] if data['人员规模'] != '-' else None
        related_field = data['所属行业'] if data['所属行业'] != '-' else None
        address = data['企业地址'] if data['企业地址'] != '-' else None
        business_scope = data['经营范围'] if data['经营范围'] != '-' else None
        org_code = data['组织机构代码'] if data['组织机构代码'] != '-' else None
        credit_code = data['统一社会信用代码'] if data['统一社会信用代码'] != '-' else None
        ie_org_code = data['进出口企业代码'] if data['进出口企业代码'] != '-' else None
        reg_num = data['工商注册号'] if data['工商注册号'] != '-' else None
    except:
        pass
    try:
        """插入语句模块"""
        cursor.execute(SQL_to_detail,(company_name,credit_code,law_agent,
        company_status,start_date,operate_period,company_type,reg_capital,
        contribute_capital,staff_size,related_field,address))
        dbobj.commit()
        cursor.execute(SQL_to_code,(company_name,credit_code,org_code,
        ie_org_code,reg_num))
        dbobj.commit()
        cursor.execute(SQL_to_intro,(company_name,business_scope))
        dbobj.commit()
        print('—' * 100)
        print('\033[1;32m状态：Save to Database Success\033[0m')
    except:
        try:
            """更新语句模块"""
            cursor.execute(SQL_check_key_close)
            cursor.execute(SQL_update_detail,(company_name,credit_code,law_agent,
            company_status,start_date,operate_period,company_type,reg_capital,
            contribute_capital,staff_size,related_field,address,company_name))
            dbobj.commit()
            cursor.execute(SQL_update_code,(company_name,credit_code,org_code,
            ie_org_code,reg_num,company_name))
            dbobj.commit()
            cursor.execute(SQL_update_intro,(company_name,business_scope,company_name))
            dbobj.commit()
            cursor.execute(SQL_check_key_open)
            print('—' * 100)
            print('\033[1;34m状态：Update Success\033[0m')
        except:
            print('—' * 100)
            print('\033[1;31m状态：Error fail to store to database\033[0m')
            dbobj.rollback()
            
        