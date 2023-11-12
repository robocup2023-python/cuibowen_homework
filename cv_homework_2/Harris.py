import cv2
import numpy as np


# Harris 角点检测
def harris_corner_detection(Ix2, Iy2, IxIy, k):

    # 计算 M 矩阵
    det_M = Ix2 * Iy2 - IxIy**2
    trace_M = Ix2 + Iy2

    # 计算角点响应函数 R
    R = det_M - k * (trace_M**2)

    # 定义正阈值 T
    threshold = 0.01 * R.max()

    # 标记候选角点
    candidate_points = np.zeros_like(gray, dtype=np.uint8)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if R[i, j] < threshold:
                candidate_points[i, j] = 255

    # 创建一个彩色图像用于显示
    colored_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    colored_img[candidate_points == 255] = [0, 0, 255]

    return colored_img

ksize = 3
k = 0.04

img = cv2.imread('testpic_Harris.png')

# 灰度化
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 对灰度图进行高斯滤波
blurred = cv2.GaussianBlur(gray, (5, 5), 0.5, None, 0.5)

# 计算梯度
Ix = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=ksize)
Iy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=ksize)

gradient_magnitude = np.sqrt(Ix ** 2 + Iy ** 2)
gradient_direction = np.arctan2(Iy, Ix) * 180 / np.pi

Ix2 = Ix * Ix
Iy2 = Iy * Iy
IxIy = Ix * Iy

# 归一化
Ix2 = cv2.normalize(Ix2, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
Iy2 = cv2.normalize(Iy2, None, 0, 255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
IxIy = cv2.normalize(IxIy, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

# 对梯度图像进行高斯模糊
Ix2 = cv2.GaussianBlur(Ix2, (5, 5), 0.5, None, 0.5)
Iy2 = cv2.GaussianBlur(Iy2, (5, 5), 0.5, None, 0.5)
IxIy = cv2.GaussianBlur(IxIy, (5, 5), 0.5, None, 0.5)

# 可视化展示
colored_img = harris_corner_detection(Ix2, Iy2, IxIy, k)

cv2.imshow('Harris with Candidate Points', colored_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

