# -*- coding: utf-8 -*-
# @Author : lihuiwen
# @file : goods_spider
# @Email : huiwennear@163.com
# @Time : 2024/5/23 14:00
import json
from urllib.parse import urljoin

import scrapy
from scrapy import Request


class GoodsSpider(scrapy.Spider):
    name = "goods_spider"

    def __init__(self):
        self.list_headers = {
            'dpr': '1',
            'downlink': '6.4',
            'sec-ch-ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }

        self.detail_headers = {
            'Cache-Control': 'max-age=0',
            'dpr': '1',
            'downlink': '10',
            'sec-ch-ua': '"Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.6045.160 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }
        self.proxy = ""

    def start_requests(self):
        keyword = "iphone"
        page = 1
        req_url = f'https://www.walmart.com/search?q={keyword}&page={page}&affinityOverride=default'
        req_meta = {"keyword": keyword, "page": page,
                    # "proxy":self.proxy
                    }
        yield Request(url=req_url, method='GET', headers=self.list_headers,
                      callback=self.detail_page_parse, meta=req_meta,
                      dont_filter=True)

    def detail_page_parse(self, response):
        keyword = response.meta.get('keyword')
        page = response.meta.get('page')
        div_list = response.xpath('//div[@class="h-100 pb1-xl pr4-xl pv1 ph1"]')
        if (div_list):
            for div_index in range(len(div_list)):
                div_item = div_list[div_index]
                goods_item = {}
                goods_item["name"] = div_item.xpath(
                    './/a[string-length(@link-identifier) > 0]/span[@class="w_iUH7"]/text()').extract_first().strip()
                goods_item["detail_url"] = urljoin("https://www.walmart.com/", div_item.xpath(
                    './/a[string-length(@link-identifier) > 0]/@href').extract_first().strip())
                req_meta = {"keyword": keyword, "goods_item": goods_item,
                            # "proxy":self.proxy
                            }
                yield Request(url=goods_item["detail_url"], method='GET', headers=self.detail_headers,
                              callback=self.detail_parse, meta=req_meta,
                              dont_filter=True)
            page += 1
            req_url = f'https://www.walmart.com/search?q={keyword}&page={page}&affinityOverride=default'
            req_meta = {"keyword": keyword, "page": page,
                        # "proxy":self.proxy
                        }
            yield Request(url=req_url, method='GET', headers=self.list_headers,
                          callback=self.detail_page_parse, meta=req_meta,
                          dont_filter=True)
        else:
            print("没有下一页")

    def detail_parse(self, response):
        keyword = response.meta.get('keyword')
        goods_item = response.meta.get('goods_item')
        goods_item["goods_detail"] = json.loads(
            response.xpath('//script[@id="__NEXT_DATA__"]/text()').extract_first().strip(), strict=False)
        print(goods_item)
