""" 这是Chen自己写的可以爬取哔哩哔哩音频、视频的类
这个类中包括：
    1. 可用的哔哩哔哩搜索模式，并能够用表格显示。
    2. 可供显示的音频、视频名称。
    3. 可供选择的单一、多个视频单进程、多进程下载。
    """

import random
import json
import multiprocessing
import re
import time
from os import makedirs
from os.path import exists
import requests
from lxml import etree
import prettytable as pt
from moviepy import VideoFileClip, AudioFileClip


class ChenSpiderBasicInfo:
    """ 这是一个获取头部信息和代理信息的父类"""

    def __init__(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        }
        proxies = {
            "http": ["47.99.112.148", "8.137.38.48", "114.231.46.160", "180.122.147.205", "117.69.232.248",
                     "112.244.230.117", "114.232.110.33", "114.232.110.141", "182.34.37.218", "117.69.237.103",
                     '36.6.144.235'],
            "https": ['114.106.137.169', '117.69.233.179', '113.223.213.80', '117.71.154.81']
        }
        self.headers = headers
        self.proxies = proxies
        self.random_proxy = {
            "http": random.choice(self.proxies["http"]),
            # 'https':random.choice(proxies["https"])
        }

    def get_headers(self):
        """ 获取头部信息"""

        return self.headers

    def get_random_proxy(self):
        """这是一个获取随机代理proxy（怕会封所以每次都用随机代理）的函数"""

        self.random_proxy = {
            "http": random.choice(self.proxies["http"]),
            # 'https':random.choice(proxies["https"])
        }
        return self.random_proxy


class ChenBilibiliVideo(ChenSpiderBasicInfo):
    """
    这是获取哔哩哔哩音频的类
    1. 可进行搜索
    2. 可显性显示
    3. 可自动判断是否为特殊模式（多个单独，多个和为一个单独）
    4. 可单个下载
    5. 可多个下载（单进程、多进程）
    """

    def __init__(self):
        super().__init__()
        self.headers['Referer'] = 'https://www.bilibili.com/'
        self.search_info_dict = None
        self.search_video_url = None
        self.search_video_title = None
        self.bilibili_play_tree = None
        self.bilibili_play_info = None
        self.bilibili_play_single_name = None
        self.bilibili_play_name = None
        self.judge_if_multiply_video_index = None
        self.down_model = None
        self.info_url = None
        self.video_url = None
        self.audio_url = None
        self.last_name = None
        self.dir_file_name = None
        self.video_module = None

    def search_system(self):
        """ 搜索函数，输入要搜索的字符串，输出列表显示，输入想要的视频，返回想要的视频ULR和TITLE"""
        keyword = input('输入想要查询的:')
        info_dict = []
        url = fr'https://search.bilibili.com/video?keyword={keyword}'
        request = requests.get(url=url, headers=self.headers, proxies=self.random_proxy).text
        tree = etree.HTML(request)
        div_list = tree.xpath('//div[@class = "video-list row"]')[0]
        href_url = div_list.xpath('//div[@class = "bili-video-card__info--right"]/a/@href')
        title = div_list.xpath('//div[@class = "bili-video-card__info--right"]/a/h3/@title')
        play_volume = div_list.xpath('//span[@class = "bili-video-card__stats--item"][1]/span/text()')
        # print(href_url)
        # print(title)
        # print(play_volume)
        table = pt.PrettyTable()
        table.title = '搜索列表'
        table.field_names = ['标号', '标题名称', '播放量']
        for i in range(len(href_url)):
            value_dict = {
                "Title": title[i],
                'href': 'https:' + str(href_url[i]),
                'play_volume': play_volume[i]
            }
            info_dict.append(value_dict)
            table.add_row([i + 1, title[i], play_volume[i]])
        print(table)

        search_idex = int(input('输入想要获取的编号:'))
        self.search_video_url = info_dict[search_idex - 1]['href']
        self.search_video_title = info_dict[search_idex - 1]['Title']
        return self.search_video_url, self.search_video_title

    def change_standard_filename(self, filename):
        """ 这是一个将文件名称标准化的函数 """
        # 去除前后空格
        filename = filename.strip()

        # 替换操作系统不允许的字符（Windows的例子）
        invalid_chars = r'[<>:"/\\|?*]'
        filename = re.sub(invalid_chars, "_", filename)

        # 确保文件名没有过长
        max_length = 200  # Windows文件名最大长度限制
        if len(filename) > max_length:
            filename = filename[:max_length]
        return filename

    def judge_if_multiply_video(self, module=0):
        """ 这是一个判断是否是下载当前音乐还是当前全部音乐的函数 """
        if module == 0:
            self.info_url = 'https://www.bilibili.com/video/' + input("输入视频代码：如（BV1aumjYZEcG）：")
        if module == 1:
            self.info_url = self.search_video_url
        request = requests.get(url=self.info_url, headers=self.headers,
                               proxies=self.get_random_proxy()).text
        tree = etree.HTML(request)
        # 检测是否为单独视频合并的
        if tree.xpath('/html/body/div[2]/div[2]/div[2]/div/div[7]/div[1]/div[2]/div[@class="video-pod__list section"]'):
            self.video_module = "String"
            multiply_video_info = tree.xpath(
                '/html/body/div[2]/div[2]/div[2]/div/div[7]/div[1]/div[2]/div[@class="video-pod__list section"]')
            main_video_list = [sole_video_name.xpath("./div/div/div[1]/@title")[0] for sole_video_name in
                               multiply_video_info[0].xpath('./div')]
            table = pt.PrettyTable()
            table.title = '视频列表'
            table.field_names = ['标号', '标题名称']
            for i in range(len(main_video_list)):
                table.add_row([i + 1, main_video_list[i]])
            print(f'【+】一共搜索出{len(main_video_list)}个【+】')
            print(table)
            self.judge_if_multiply_video_index = int(input("检测到有多个视频是否全部下载？|【0】否、【1】是|："))
            if self.judge_if_multiply_video_index == 0:
                return self.info_url
            if self.judge_if_multiply_video_index == 1:
                sole_video_list = ['https://www.bilibili.com/video/' + sole_video.xpath('./@data-key')[0] for sole_video
                                   in multiply_video_info[0].xpath('./div')]
                return sole_video_list
        # 检测是否为合集
        if tree.xpath(
                '/html/body/div[2]/div[2]/div[2]/div/div[7]/div[1]/div[2]/div[@class="video-pod__list multip list"]'):
            self.video_module = "Number"
            multiply_video_info = tree.xpath(
                '/html/body/div[2]/div[2]/div[2]/div/div[7]/div[1]/div[2]/div[@class="video-pod__list multip list"]')
            main_video_list = [sole_video_name.xpath("./div/div/div[1]/@title")[0] for sole_video_name in
                               multiply_video_info[0].xpath('./div')]
            table = pt.PrettyTable()
            table.title = '视频列表'
            table.field_names = ['标号', '标题名称']
            for i in range(len(main_video_list)):
                table.add_row([i + 1, main_video_list[i]])
            print(f'【+】一共搜索出{len(main_video_list)}个【+】')
            print(table)
            self.judge_if_multiply_video_index = int(input("检测到有多个视频是否全部下载？|【0】否、【1】是|："))
            if self.judge_if_multiply_video_index == 0:
                return self.info_url
            if self.judge_if_multiply_video_index == 1:
                sole_video_list = [self.info_url + '?p=' + str(sole_video_page) for sole_video_page
                                   in range(1, len(multiply_video_info[0].xpath('./div')) + 1)]

                return sole_video_list
        else:
            print('没发现其他音乐！正在下载该音乐！')
            return self.info_url

    def get_bilibili_play_info(self, info_url):
        """ 这是一个获得全部播放信息的函数 """
        request = requests.get(url=info_url, headers=self.headers,
                               proxies=self.get_random_proxy()).text
        tree = etree.HTML(request)
        self.bilibili_play_name = self.change_standard_filename(
            tree.xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/h1/@title')[0])
        if self.video_module == "Number":
            self.bilibili_play_single_name = self.change_standard_filename(
                tree.xpath('/html/head/title/text()')[0][:-14])
        info = tree.xpath('/html/head/script[4]')[0].text[20:]
        # 全部播放数据字典
        self.bilibili_play_info = json.loads(info)
        # pprint.pprint(self.bilibili_play_info['data']['dash']['video'])
        # input()
        # 视频数据
        self.video_url = self.bilibili_play_info['data']['dash']['video'][0]['baseUrl']
        # 音频数据
        self.audio_url = self.bilibili_play_info['data']['dash']['audio'][0]['baseUrl']

    def down_bilibili_audio(self):
        """ 下载音频 (或者视频，还没更新视频) """
        dir_file_name = self.dir_file_name
        down_model = self.down_model
        try:
            if down_model == "v":
                self.last_name = ".mp4"
                request = requests.get(url=self.video_url, headers=self.headers, timeout=5).content
            else:
                self.last_name = ".mp3"
                request = requests.get(url=self.audio_url, headers=self.headers, timeout=5).content
            if self.video_module == "String":
                # 如果不存在则创建，如果存在则不执or行后边代码
                exists(dir_file_name) or makedirs(dir_file_name)
                with open(f"{dir_file_name}/{self.change_standard_filename(self.bilibili_play_name)}{self.last_name}",
                          'wb') as fp:
                    fp.write(request)
                # print("下载地址为：", dir_file_name)
                print(f"\t{self.change_standard_filename(self.bilibili_play_name)}下载完毕\n", "\t\t下载地址为：",
                      f"{dir_file_name}/{self.bilibili_play_name}{self.last_name}")
            if self.video_module == "Number":
                # 如果不存在则创建，如果存在则不执or行后边代码
                exists(dir_file_name + "/" + self.change_standard_filename(self.bilibili_play_name)) or makedirs(
                    dir_file_name + "/" + self.change_standard_filename(self.bilibili_play_name))
                with open(
                        f"{dir_file_name}/{self.change_standard_filename(self.bilibili_play_name)}/{self.change_standard_filename(self.bilibili_play_single_name)}{self.last_name}",
                        'wb') as fp:
                    fp.write(request)
                # print("下载地址为：", dir_file_name)
                print(f"\t{self.change_standard_filename(self.bilibili_play_single_name)}下载完毕\n", "\t\t下载地址为：",
                      f"{dir_file_name}/{self.change_standard_filename(self.bilibili_play_name)}/{self.change_standard_filename(self.bilibili_play_single_name)}{self.last_name}")
        except Exception:
            print(self.bilibili_play_name, '下载发生错误')

    def down_bilibili_video(self):
        """ 下载视频 """
        # 指定视频文件和音频文件路径
        video_path = f"{self.dir_file_name}-video.mp4"
        audio_path = f"{self.dir_file_name}-audio.mp3"

        # 加载视频和音频
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        # 将音频添加到视频中
        video = video.with_audio(audio)

        # 输出合并后的视频文件
        output_path = f"{self.dir_file_name}.mp4"
        video.write_videofile(output_path)
        print(output_path, "视频下载完毕")

    def multiply_down_bilibili_video(self, info_url):
        """ 多进程下载 """
        self.get_bilibili_play_info(info_url)
        self.down_bilibili_audio()

    def main(self, down_model="a", dir_file_name="D:/歌曲"):
        """ 这是下载的总函数 """
        # --------------------基本参数----------------- #
        # 下载文件夹名称：(可更改)
        self.down_model = down_model
        self.dir_file_name = fr"{dir_file_name}"
        # ------------------------------------------- #
        # 判断是否用下载器
        judge_if_use_search = 0
        if int(input('是否启用搜索引擎？|【0】否、【1】是|：')) == 1:
            self.search_system()
            judge_if_use_search = 1
        sole_video_list = self.judge_if_multiply_video(judge_if_use_search)
        if type(sole_video_list) == list:
            if_multiply = int(input('是否多进程下载？|【0】否、【1】是|：'))
            now_time = time.time()
            if if_multiply == 0:
                for info_url in sole_video_list:
                    self.get_bilibili_play_info(info_url)
                    self.down_bilibili_audio()
                print(time.time() - now_time)
            if if_multiply == 1:
                pool = multiprocessing.Pool()
                pool.map(self.multiply_down_bilibili_video, sole_video_list)
                pool.close()
                pool.join()
                print(time.time() - now_time)
        else:
            self.get_bilibili_play_info(self.info_url)
            self.down_bilibili_audio()
