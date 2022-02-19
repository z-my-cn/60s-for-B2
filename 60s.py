import json
import os
import time
from datetime import datetime

import requests


def loadConfig():
    '''
    加载配置文件，异常返回空字典。
    '''
    config_file = '60s.json'
    config = {}
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
            print('读取配置文件成功！')
    else:
        print('未找到配置文件！')

    return config


def apiList(url):
    '''
    返回使用过程中所需要的api列表
    '''
    api_list = {}
    api_list['get_news'] = 'https://v2.alapi.cn/api/zaobao'
    api_list['get_lunar'] = 'https://v2.alapi.cn/api/lunar'
    api_list['get_token'] = url + '/wp-json/jwt-auth/v1/token'
    api_list['check_token'] = url + '/wp-json/jwt-auth/v1/token/validate'
    api_list['upload'] = url + '/wp-json/b2/v1/fileUpload'
    api_list['submit'] = url + '/wp-json/b2/v1/submitNewsflashes'

    return api_list


def getData(api, token):
    '''
    请求ALAPI接口，获取相关数据，异常返回空字典。
    '''
    data = {}
    params = {"token": token, "format": "json"}
    r = requests.get(api, params=params)
    result = r.json()
    if r.status_code == 200:
        if result['code'] == 200 and result['msg'] == 'success':
            print('API请求成功！')
            data = result['data']
        else:
            print('API请求失败！\n 错误信息：{}'.format(result['msg']))
    else:
        print('API接口失效！')

    return data


def getImg(url, path):
    '''
    下载远程图片到本地，如图片已存在将会覆盖写。
    '''
    img = requests.get(url)
    with open(path, 'wb') as f:
        f.write(img.content)


def wpToken(api, user):
    '''
    获取jwt-auth的Token，异常返回空字符串。
    '''
    r = requests.post(api, data=user)
    token = ''
    if 'token' in r.json():
        token = r.json()['token']
        print('获取jwt的Token成功！')
    else:
        print('获取jwt的Token失败！请检查配置是否正确！')

    return token


def wpTokenValid(api, token):
    '''
    验证jwt-auth的Token是否有效， 异常返回False
    '''
    headers = {'authorization': 'Bearer ' + token}
    r = requests.post(api, headers=headers)
    if r.json()['code'] == 'jwt_auth_valid_token':
        return True
    else:
        return False


def wpUpload(api, token, path):
    '''
    上传类型为newsflashes的图片附件，异常返回空字典
    '''
    headers = {'authorization': 'Bearer ' + token}
    data = {'post_id': 1, 'type': 'newsflashes'}
    files = {'file': open(path, 'rb')}
    r = requests.post(api, headers=headers, data=data, files=files)
    inform = {}
    if ('id' and 'url') in r.json():
        inform['img[url]'] = r.json()['url']
        inform['img[id]'] = r.json()['id']
        print('图片上传成功！')
    else:
        inform = {}
        print('图片上传失败！请检查用户是否有上传权限！')

    return inform


def wpSubmit(api, token, data):
    headers = {'authorization': 'Bearer ' + token}
    r = requests.post(api, headers=headers, data=data)
    result = r.json()
    if type(result) is str:
        print('发布成功！')
    elif type(result) is dict:
        print('发布失败！错误原因：{}!'.format(result['message']))
    else:
        print('发布失败！未知原因，请检查配置！')


def main():
    config = loadConfig()
    if config != {}:
        api_list = apiList(config['url'])
        news = getData(api_list['get_news'], config['api_token'])

        while news['date'] != datetime.strftime(datetime.today(), "%Y-%m-%d"):
            print('今日数据尚未更新！')
            time.sleep(1800)
            news = getData(api_list['get_news'], config['api_token'])
        else:
            print('获取今日数据成功！')

        token = wpToken(api_list['get_token'], config['user'])

        dt = datetime.strptime(news['date'], '%Y-%m-%d')
        submit = {}
        submit['title'] = '{}月{}日，{}，每天60秒读懂世界！'.format(dt.month, dt.day,
                                                        dt.strftime('%A'))
        submit['tag'] = config['news_tag']

        if config['all_image']:
            path = 'image.png'
            getImg(news['image'].replace('!/format/webp', ''), path)
            submit['content'] = '来源:澎湃、人民日报、腾讯新闻、网易新闻、新华网、中国新闻网'
        else:
            path = 'head_image.png'
            getImg(news['head_image'].replace('!/format/webp', ''), path)
            content = news['news'][:]
            content.append(news['weiyu'])
            content.append('来源:澎湃、人民日报、腾讯新闻、网易新闻、新华网、中国新闻网')
            submit['content'] = '\n\n'.join(content)

        img = wpUpload(api_list['upload'], token, path)
        if img != {}:
            submit.update(img)
            wpSubmit(api_list['submit'], token, submit)


if __name__ == "__main__":
    main()