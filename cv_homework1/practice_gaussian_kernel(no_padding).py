import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


center = None

# 创建高斯滤波核的函数

def create_gaussian_kernel(kernel_size, sigma):
    global center
    center = kernel_size // 2
    kernel = np.zeros((kernel_size, kernel_size))
    for i in range(kernel_size):
        for j in range(kernel_size):
            x, y = i - center, j - center
            kernel[i, j] = np.exp(-(x**2 + y**2) / (2.0 * sigma**2))
            kernel[i, j] /= 2 * np.pi * sigma**2
    kernel /= kernel.sum()
    return kernel


try:
    # 从用户输入获取图像文件名
    image_file = input("请输入图像文件名：")

    # 打开图像
    image = Image.open(image_file)

    # 将图像转换为灰度图
    gray_image = image.convert('L')

    # 获取图像的宽度和高度
    width, height = gray_image.size

    # 从用户输入获取滤波核的大小和高斯方差
    kernel_size = int(input("请输入高斯滤波核的大小："))
    sigma = float(input("请输入高斯方差："))

    # 创建高斯滤波核
    gaussian_kernel = create_gaussian_kernel(kernel_size, sigma)

    # 复制输入图像
    filtered_image = gray_image.copy()

    # 对图像进行高斯滤波
    for x in range(center, width - center):
        for y in range(center, height - center):
            # 以核的中心点为中心应用滤波
            sum = 0
            for i in range(kernel_size):
                for j in range(kernel_size):
                    pixel = gray_image.getpixel((x + i - center, y + j - center))
                    sum += pixel * gaussian_kernel[i][j]
            filtered_image.putpixel((x, y), int(sum))

    # 显示原始图像和滤波后的图像
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plt.imshow(gray_image, cmap='gray')
    plt.title('原始图像')

    plt.subplot(122)
    plt.imshow(filtered_image, cmap='gray')
    plt.title('高斯滤波后的图像')

    plt.show()

except Exception as e:
    print("出现错误:", str(e))
