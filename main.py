from bs4 import BeautifulSoup
import requests
import pymysql
import os
import time


db_host = 'localhost'
db_user = 'root'
db_passwd = '123456'
db_name = 'vip.mhealthu.com'
tb_name = 'data'


#数据库连接信息
db = pymysql.connect(db_host, db_user, db_passwd, db_name, charset='utf8')
cursor = db.cursor()
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Cookie': 'hy_session=2d4ee5ee307cbdeb168824782585e0e253cd5f69'
}
domain = 'http://vip.mhealthu.com'
info = []
for n in range(280, -8, -8):#按照更新时间正序排列
    # print(n)
    url = 'http://vip.mhealthu.com/Index/index/0/0/0/{}'.format(n)
    # print(n)
    # print(url)
    wb_data = requests.get(url, headers=headers)
    r = wb_data.content
    # print(wb_data.status_code)
    # print(wb_data.content)
    soup = BeautifulSoup(r, 'lxml')
    # print(soup)
    #视频标题
    titles = soup.select('body > div.container.pad_mar_0.wid.home_con > div.col-xs-8.col-sm-8.col-md-8.pad_mar_0.pull-right.curriculum > ul > li > div.pro_img > a > img ')
    #视频播放链接
    vod_links = soup.select('body > div.container.pad_mar_0.wid.home_con > div.col-xs-8.col-sm-8.col-md-8.pad_mar_0.pull-right.curriculum > ul > li > div.pro_img > a')
    for title, vod_link in zip(titles[::-1], vod_links[::-1]): #按照更新时间正序排列
        url = domain + vod_link.get('href').replace('show_v', 'show_vv')
        wb_data = requests.get(url, headers=headers)
        r = wb_data.content
        soup = BeautifulSoup(r, 'html.parser')
        s = soup.select('body > div.container.pad_mar_0.pro_video > div.col-xs-7.col-sm-7.col-md-7.pad_mar_0 > div')
        t = s[0].get_text()
        file_id = t[345:364]
        # print(file_id)
        url = 'http://play.video.qcloud.com/index.php?file_id={}&refer=vip%2Emhealthu%2Ecom&interface=Vod_Api_GetPlayInfo&app_id=1252762320'.format(file_id)
        response = requests.get(url, headers=headers)
        json = response.json()
        file_link = json['data']['file_info']['image_video']['videoUrls'][0]['url']
        image_link = json['data']['file_info']['image_url']
        create_time = json['data']['file_info']['create_time']
        #获取视频标题，并去除左边空格
        title = title.get('alt').lstrip()
        print(title)
        vod_link = domain + vod_link.get('href').replace('show_v', 'show_vv')
        # print(file_id, title, image_link, vod_link, file_link, create_time)
        # print(file_link, image_link)
        # data = {
        #     'file_id': file_id,
        #     'title': title.get('alt'),
        #     'vod_link': domain + vod_link.get('href').replace('show_v', 'show_vv'),
        #     'image_link': image_link,
        #     'file_link': file_link,
        #     'create_time': create_time
        # }
        # info.append(data)
        # print(info)
        # http://1252762320.vod2.myqcloud.com/e82ea7fdvodgzp1252762320/792e66149031868222977077359/f0.mp4
        # _,_,_, d1, d2, file_name = file_link.split('/')
        # work_dir = os.getcwd()
        # directory = d1 + '/' + d2 + 'snapshot'
        # try:
        #     os.makedirs(directory)
        # except FileExistsError:
        #     pass
        # finally:
        #     print('创建{}成功'.format(directory))
        #     os.chdir(work_dir)
        #视频文件绝对路径
        file_path = 'videos/'+title+'.mp4'
        # print(file_path)
        if os.path.exists(file_path):
            continue
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        print('{} 开始下载 {}'.format(now, title))
        print(file_link)
        # print('wget  -q -N -O {} {}'.format(file_path, file_link))
        os.system('wget  -q -N -O {} {}'.format(file_path, file_link))
        sql = '''
        insert into {}
        (file_id,title,image_link,vod_link,file_link,create_time)
        values ('{}','{}','{}','{}','{}','{}')
        '''\
        .format(tb_name, file_id, title, image_link, vod_link, file_link, create_time)
        # print(sql)
        cursor.execute(sql)
        # end = time.strftime("%Y-%m-%d %H:%M:%S")
        # print('{}下载完成'.format(file_link))
        # print(end)
        # now = time.strftime("%Y-%m-%d %H:%M:%S")
        # print('{} 开始下载 {}'.format(now, image_link))
        # os.system('wget -r -q -N -O {}.jpg {}'.format(title, image_link))
        # end = time.strftime("%Y-%m-%d %H:%M:%S")
        # print('{}下载完成'.format(image_link))
        # print(end)


cursor.close()
db.commit()
db.close()


