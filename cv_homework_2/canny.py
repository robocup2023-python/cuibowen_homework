import cv2
import numpy as np


def non_max_suppression(gradient_magnitude, gradient_direction):
    rows, cols = gradient_magnitude.shape
    suppressed = np.zeros(gradient_magnitude.shape, dtype=np.uint8)

    q, r = 0, 0

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            direction = gradient_direction[i, j]  # 当前像素的梯度方向
            mag = gradient_magnitude[i, j]  # 当前像素的梯度幅值

            # 根据梯度方向判断相邻像素的坐标
            if (0 <= direction < 22.5) or (157.5 <= direction <= 180):
                q, r = gradient_magnitude[i, j + 1], gradient_magnitude[i, j - 1]
            elif (22.5 <= direction < 67.5):
                q, r = gradient_magnitude[i - 1, j + 1], gradient_magnitude[i + 1, j - 1]
            elif (67.5 <= direction < 112.5):
                q, r = gradient_magnitude[i - 1, j], gradient_magnitude[i + 1, j]
            elif (112.5 <= direction < 157.5):
                q, r = gradient_magnitude[i - 1, j - 1], gradient_magnitude[i + 1, j + 1]

            # 如果当前像素梯度幅值是沿梯度方向上的局部最大值，则保留，否则设为0
            if mag >= q and mag >= r:
                suppressed[i, j] = mag
            else:
                suppressed[i, j] = 0

    return suppressed


def double_threshold(edge_image, low_threshold, high_threshold):
    rows, cols = edge_image.shape
    strong_edge = 175
    weak_edge = 50

    strong_edges = (edge_image > high_threshold)
    no_edges = (edge_image < low_threshold)
    weak_edges = (edge_image >= low_threshold) & (edge_image <= high_threshold)

    edge_image_new = np.zeros((rows, cols), dtype=np.uint8)

    edge_image_new[strong_edges] = strong_edge
    edge_image_new[weak_edges] = weak_edge

    # 连接边缘
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            if edge_image_new[i, j] == weak_edge:
                if (np.any(edge_image_new[i - 1:i + 2, j - 1:j + 2] == strong_edge)):
                    edge_image_new[i, j] = strong_edge
                else:
                    edge_image_new[i, j] = 0

    return edge_image_new


# 接受用户输入的图像文件名
image_path = input("请输入图像文件名：")

# 读取图像
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if image is None:
    print("无法读取图像，请检查文件路径或文件类型")
else:
    # 高斯滤波
    image_blurred = cv2.GaussianBlur(image, (5, 5), 1.4)

    # 一阶差分算子求梯度幅度和方向
    gradient_x = cv2.Sobel(image_blurred, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(image_blurred, cv2.CV_64F, 0, 1, ksize=3)

    gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
    gradient_direction = np.arctan2(gradient_y, gradient_x) * 180 / np.pi

    # 执行NMS
    nms_image = non_max_suppression(gradient_magnitude, gradient_direction)

    # 执行双阈值算法进行边缘连接
    high_threshold = 25
    low_threshold = 10
    edge_image = double_threshold(nms_image, low_threshold, high_threshold)

    # 可视化展示
    top_row = np.hstack((image, gradient_magnitude.astype(np.uint8)))
    bottom_row = np.hstack((nms_image, edge_image))
    images_combined = np.vstack((top_row, bottom_row))

    cv2.imshow('Images', images_combined)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
