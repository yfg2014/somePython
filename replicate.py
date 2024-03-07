import os
import shutil
import requests
from replicate import Client

# 要处理的资源路径
path = "/Users/wql/Dropbox/Z0_replicate_will/"
# 处理后移动路径
path2 = "/Users/wql/Dropbox/Z0-模糊图片/"
# 下载保存路径
downlaod_path = "/Users/wql/Pictures/PicWish/"
# api_token配置
api_token = "r8_xxxxxxxxx"
# rep客户端初始化
replicate = Client(api_token)


# 下载文件
def download_image(url, file_path):
    response = requests.get(url)
    with open(file_path, "wb") as file:
        file.write(response.content)

# 运行模型
def run(file):
    # 拼接图片路径
    source_path = path + file
    move_path = path2 + file
    # 获取本地图片的资源句柄
    image_source = open(source_path, "rb")
    # print(image)
    # exit(0)
    output = replicate.run(
        "sczhou/codeformer:7de2ea26c616d5bf2245ad0d5e24f0ff9a6204578a5c876db53142edd9d2cd56",
        input={
            # "image": "https://replicate.delivery/pbxt/IngEkQmZiZ3whtbkNAiOIdCsYAWVMkmoIBJnw7t2TPgvJn5S/photo.jpg",
            "image": image_source,
            "upscale": 3,
            "face_upsample": True,
            "background_enhance": True,
            "codeformer_fidelity": 0.7
        }
    )
    print(output)
    # 处理成功后移动文件到指定文件夹, 并下载图片
    if output:
        # 移动文件
        move_file(source_path, move_path)
        # 图片保存的文件路径
        file_path = downlaod_path + output.split("/")[-2] + ".jpg"
        # 下载图片
        download_image(output, file_path)



# 移动文件
def move_file(source_path, destination_path):
    shutil.move(source_path, destination_path)


# 调用函数
if __name__ == "__main__":
    # 循环读取文件
    for file in os.listdir(path):
        if file != ".DS_Store":
            # 运行模型处理图片
            run(file)


