import os

import cv2
from PIL import Image, ImageChops


# 视盘白化
def inner(mask_path, save_path):
    img = Image.open(mask_path)
    # 模式L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
    Img = img.convert('L')
    # 自定义灰度界限，大于这个值为白色，小于这个值为黑色
    threshold = 30
    table = []
    for i in range(256):
        if i < threshold:
            table.append(1)
        else:
            table.append(0)
    # 图片二值化
    photo = Img.point(table, '1')
    # return photo
    photo.save(save_path)


# 视盘黑化
def outer(mask_path, save_path):
    img = Image.open(mask_path)
    # 模式L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
    Img = img.convert('L')
    # 自定义灰度界限，大于这个值为白色，小于这个值为黑色
    threshold = 240
    table = []
    for i in range(256):
        if i < threshold:
            table.append(1)
        else:
            table.append(0)
    # 图片二值化
    photo = Img.point(table, '1')
    # return photo
    photo.save(save_path)


# 最小外接圆
def minimum_external_circle(mask_path):
    image = cv2.imread(mask_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for cont in contours:
        # 外接圆
        (x, y), radius = cv2.minEnclosingCircle(cont)
        cv2.circle(image, (int(x), int(y)), int(radius), (0, 0, 255), 2)
    # cv2.imshow('ret', image)
    # cv2.waitKey(0)
    return radius

def cd_ratio(path):

    photo1 = 'test1.jpg'
    photo2 = 'test2.jpg'
    inner(path,photo1)
    outer(path,photo2)
    # 视杯半径
    a = minimum_external_circle(photo1)
    # 视盘半径
    b = minimum_external_circle(photo2)

    # 杯盘比
    rat= a / b
    print(rat)
    return rat

# if __name__ == '__main__':
#
#     print(cd_ratio('../media/img/V0008_division.png'))
