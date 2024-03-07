#!/usr/bin/python
# -*- coding:utf8 -*-
import hashlib
import shutil
import os

'''
去除一个目录中的重复图片
已经简化过了，以前写的很长很差
'''


# 获取一个文件的md5
def get_md5(filepath):
    file = open(filepath, "rb")
    md = hashlib.md5()
    md.update(file.read())
    res = md.hexdigest()
    return res


# 优化后去重算法
def deal_pic2(load_path, save_path):
    os.makedirs(save_path, exist_ok=True)

    # 获取图片列表file_map，字典{filename : image_md5}
    file_map = {}
    # 遍历filePath下的文件、文件夹（包括子目录）
    for parent, dirnames, filenames in os.walk(load_path):
        for filename in filenames:
            image_md5 = get_md5(os.path.join(parent, filename))
            file_map.setdefault(os.path.join(parent, filename), image_md5)

    # file_map去除重复值
    func = lambda z: dict([(x, y) for y, x in z.items()])
    file_map = func(func(file_map))

    # 新数据结构移到save_path目录里
    for image in file_map:
        shutil.move(image, save_path)
        print("正在移动去重后照片到save_path：", image)


if __name__ == '__main__':
    # 要去重的文件夹
    load_path = 'D:\Dropbox/test1'
    # 空文件夹，用于存储处理后的图片
    save_path = 'D:\Dropbox/test2'
    deal_pic2(load_path, save_path)
