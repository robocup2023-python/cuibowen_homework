import numpy as np
from PIL import Image
import matplotlib.pyplot as plt


def create_gaussian_kernel(kernel_size, sigma):
    center = kernel_size // 2
    kernel = np.zeros((kernel_size, kernel_size))
    for i in range(kernel_size):
        for j in range(kernel_size):
            x, y = i - center, j - center
            kernel[i, j] = np.exp(-(x ** 2 + y ** 2) / (2.0 * sigma ** 2))
            kernel[i, j] /= 2 * np.pi * sigma ** 2
    kernel /= kernel.sum()
    return kernel


try:
    image_file = input("请输入图像文件名：")
    image = Image.open(image_file)
    gray_image = image.convert('L')
    width, height = gray_image.size
    kernel_size = 5  # 高斯滤波核的大小
    sigma = 1  # 高斯方差

    # 进行复制边缘填充
    padding_size = kernel_size // 2
    padded_image = Image.new('L', (width + 2 * padding_size, height + 2 * padding_size))
    padded_image.paste(gray_image, (padding_size, padding_size))

    # 创建高斯核
    gaussian_kernel = create_gaussian_kernel(kernel_size, sigma)

    filtered_image = Image.new('L', (width, height))

    for x in range(width):
        for y in range(height):
            sum = 0
            for i in range(kernel_size):
                for j in range(kernel_size):
                    pixel_x = x + i
                    pixel_y = y + j
                    pixel = padded_image.getpixel((pixel_x, pixel_y))
                    sum += pixel * gaussian_kernel[i][j]
            filtered_image.putpixel((x, y), int(sum))

    # 显示原始图像、填充图像和过滤图像
    plt.figure(figsize=(12, 6))
    plt.subplot(131)
    plt.imshow(gray_image, cmap='gray')
    plt.title('原始图像')

    plt.subplot(132)
    plt.imshow(padded_image, cmap='gray')
    plt.title('填充后的图像')

    plt.subplot(133)
    plt.imshow(filtered_image, cmap='gray')
    plt.title('高斯滤波后的图像')

    plt.show()

except Exception as e:
    print("出现错误:", str(e))
