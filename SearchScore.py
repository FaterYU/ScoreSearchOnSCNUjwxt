from requests import session
from re import findall
from json import loads,load,dump
# from os import system
class Score:
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36'
    }
    purl = 'https://jwxt.scnu.edu.cn/cjcx/cjcx_cxXsgrcj.html?doType=query&gnmkdm=N305005&su=20213802028'
    pdata = {
        'xnm': 2022,
        'xqm': 3,
        '_search': 'false',
        'nd': 1672812592764,
        'queryModel.showCount': 15,
        'queryModel.currentPage': 1,
        'queryModel.sortName': '',
        'queryModel.sortOrder': 'asc',
        'time': 1
    }
    def postScore(self,xnm=2022,xqm=1):
        self.pdata['xnm']=xnm
        self.pdata['xqm']=3 if xqm==1 else 12
        x = self.session.post(
            url=self.purl,
            headers=self.headers,
            data=self.pdata,
            cookies=self.cookies
        )
        print(str(xnm)+ ' 学年 第 '+str(xqm)+' 学期\n成绩已出 '+str(len(loads(x.text)['items']))+' 门\n')
        title=['课程名称','成绩','绩点','学分','学分绩点']
        print(' | '.join(title))
        for i in loads(x.text)['items']:
            print()
            print(' | '.join([i['kcmc'], i['cj'], i['jd'], i['xf'], i['xfjd']]))

    def saveCookies(self):
        self.session = session()
        gurl='https://jwxt.scnu.edu.cn/xtgl/login_slogin.html'
        a = self.session.get(url=gurl, headers=self.headers)
        logurl=findall('https://sso.scnu.edu.cn/AccountService.*https://jwxt.scnu.edu.cn/sso/oauthLogin',a.text)[0]
        self.session.get(url=logurl, headers=self.headers)
        self.session.post(
            url='https://sso.scnu.edu.cn/AccountService/user/login.html',
            headers=self.headers
        )
        self.cookies = self.session.cookies.get_dict()
        self.session.post(
            url='https://sso.scnu.edu.cn/AccountService/user/login.html',
            headers=self.headers,
            data=self.user)
        self.session.get(
            url='https://sso.scnu.edu.cn/AccountService/openapi/onekeyapp.html?app_id=96',
            headers=self.headers,
            cookies=self.cookies)

    def __init__(self,user):
        self.user = {
            'account': user['account'],
            'password': user['password'],
            'rancode': ''
        }
        self.saveCookies()

if __name__ == '__main__':
    try:
        with open('./user.json','r') as file:
            user=load(file)
        score = Score(user)
        score.postScore(xnm=user['year'],xqm=user['term'])
    except:
        print('请配置用户信息')
        account=int(input('学号：'))
        password=input('密码：')
        year=int(input('学年(2022)：'))
        term=int(input('学期(1)：'))
        user={
            "account": account,
            "password": password,
            "year":year,
            "term":term
        }
        with open('./user.json','w') as file:
            dump(user,file)
        score = Score(user)
        score.postScore(xnm=user['year'], xqm=user['term'])
    # system('pause') # windows -> .exe
