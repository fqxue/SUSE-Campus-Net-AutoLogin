import re
import time
from urllib.parse import quote

import requests


def auto_login(account, password, interval=60, service='宜宾移动', base_url='http://10.23.2.4/'):
    while True:
        try:
            r = requests.post(base_url)
            if 'success' in r.url:
                print('success')
            else:
                # 若未成功，则进行GET请求
                r = requests.get(r.url)
                text = r.text

                # 正则查找重定向链接
                match = re.search(r"top\.self\.location\.href='([^']+)'", text)
                if match:
                    # 提取重定向URL和参数
                    redirect_url = match.group(1)
                    query_string = redirect_url.split('?')[1]

                    # 登录接口URL
                    login_url = f'{base_url}eportal/InterFace.do?method=login'

                    # 构造POST数据
                    data = {
                        'userId': account,
                        'password': password,
                        'service': quote(service),
                        'queryString': query_string,
                        'passwordEncrypt': 'false'
                    }

                    # 发起登录请求
                    response = requests.post(login_url, data=data)
                    response.encoding = 'utf-8'

                    # 打印返回的JSON结果
                    result = response.json()
                    if result['result'] == 'success':
                        print('登录成功')
                    else:
                        print(f"登录失败: {result['message']}")
                else:
                    print("未找到重定向URL，无法继续登录流程。")
        except Exception as e:
            print(f"程序执行出错: {e}")

        time.sleep(interval)


#
if __name__ == '__main__':
    account = ''  # 账号
    password = ''  # 密码
    interval = 60  # 间隔时间（秒）
    service = '宜宾移动'  # 服务名
    auto_login(account, password, interval, service)
