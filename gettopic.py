#encoding=utf-8
import urllib,pymysql,requests,re
from db.wb_data import get_flag_by_title

config={
	'host':'127.0.0.1',
	'port':3306,
	'user':'root',
	'password':'WS15871564/56BT',
	'db':'weibo',
	'charset':'utf8',
	}
conn=pymysql.connect(**config)
cursor=conn.cursor()
weiboHotFile=requests.get('http://s.weibo.com/top/summary')
weiboHotHtml=weiboHotFile.text
hotKey=re.compile(r'td class=\\"td_05\\"><a href=\\"\\/weibo\\/(.*?)&Refer=top\\"')
hotKeyListBe=hotKey.findall(weiboHotHtml)
topicid=1
for title in hotKeyListBe:
    #flag=get_flag_by_title(title)
    #if flag:
        #print("%s exist"%(title))
        #continue
    title=title.replace('25','')
    url='http://s.weibo.com/weibo/'+title
    title=urllib.parse.unquote(title)
    sql1='insert into toptopic (daydate,mindate,title,url) values (curdate(),curtime(),%s,%s)'
    sql2='insert into keywords (keyword,enable) values (%s,1)'
    try:
        cursor.execute(sql1,(title,url))
        cursor.execute(sql2,(title))
    #except IntegrityError:
    except Exception:
        print("%s exist2"%(title))
        continue
    print(str(topicid)+''+title+''+url+'\n')
    topicid+=1
    conn.commit()
cursor.execute('alter table keywords drop column id')
cursor.execute('alter table keywords add id int AUTO_INCREMENT UNIQUE')
cursor.close()
conn.close()
