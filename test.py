# -*- coding: utf-8 -*-
# @Author : lihuiwen
# @file : test
# @Email : huiwennear@163.com
# @Time : 2024/5/24 16:42
import requests

url = "https://www.walmart.com/search"

querystring = {"q":"iPhone","page":"3","affinityOverride":"default"}

payload = ""
headers = {
'dpr':'1',
'downlink':'6.4',
'sec-ch-ua':'"Chromium";v="119", "Not?A_Brand";v="24"',
'sec-ch-ua-mobile':'?0',
'sec-ch-ua-platform':'"Windows"',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'Sec-Fetch-Site':'none',
'Sec-Fetch-Mode':'navigate',
'Sec-Fetch-User':'?1',
'Sec-Fetch-Dest':'document',
'Accept-Language':'zh-CN,zh;q=0.9',
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

print(response.text)
