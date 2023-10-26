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

# "Reflect across edge" 填充方法
def reflect_edge_padding(image, padding_size):
    width, height = image.size
    padded_width = width + 2 * padding_size
    padded_height = height + 2 * padding_size
    padded_image = Image.new('L', (padded_width, padded_height))

    # 复制原图像到中心区域
    padded_image.paste(image, (padding_size, padding_size))

    # 填充左边缘
    for x in range(padding_size):
        for y in range(height):
            mirrored_x = padding_size - x
            pixel = image.getpixel((0, y))
            padded_image.putpixel((x, y + padding_size), pixel)

    # 填充右边缘
    for x in range(padding_size):
        for y in range(height):
            mirrored_x = width - 1 - x
            pixel = image.getpixel((width - 1, y))
            padded_image.putpixel((x + width + padding_size, y + padding_size), pixel)

    # 填充顶部边缘
    for y in range(padding_size):
        for x in range(width):
            mirrored_y = padding_size - y
            pixel = image.getpixel((x, 0))
            padded_image.putpixel((x + padding_size, y), pixel)

    # 填充底部边缘
    for y in range(padding_size):
        for x in range(width):
            mirrored_y = height - 1 - y
            pixel = image.getpixel((x, height - 1))
            padded_image.putpixel((x + padding_size, y + height + padding_size), pixel)

    # 填充四个角
    for x in range(padding_size):
        for y in range(padding_size):
            # 左上角
            pixel = image.getpixel((0, 0))
            padded_image.putpixel((x, y), pixel)
            # 右上角
            pixel = image.getpixel((width - 1, 0))
            padded_image.putpixel((x + width + padding_size, y), pixel)
            # 左下角
            pixel = image.getpixel((0, height - 1))
            padded_image.putpixel((x, y + height + padding_size), pixel)
            # 右下角
            pixel = image.getpixel((width - 1, height - 1))
            padded_image.putpixel((x + width + padding_size, y + height + padding_size), pixel)

    return padded_image

try:
    image_file = input("请输入图像文件名：")
    image = Image.open(image_file)
    gray_image = image.convert('L')
    width, height = gray_image.size
    kernel_size = 5  # 高斯滤波核的大小
    sigma = 1.0  # 高斯方差

    gaussian_kernel = create_gaussian_kernel(kernel_size, sigma)

    # 对图像进行边缘填充
    padding_size = kernel_size // 2
    padded_image = reflect_edge_padding(gray_image, padding_size)

    # 创建一个新的图像用于存储滤波结果
    filtered_image = Image.new('L', (width, height))

    for x in range(padding_size, width + padding_size):
        for y in range(padding_size, height + padding_size):
            sum = 0
            for i in range(kernel_size):
                for j in range(kernel_size):
                    pixel_x = x + i - padding_size
                    pixel_y = y + j - padding_size
                    pixel = padded_image.getpixel((pixel_x, pixel_y))
                    sum += pixel * gaussian_kernel[i][j]
            filtered_image.putpixel((x - padding_size, y - padding_size), int(sum))

    plt.figure(figsize=(12, 6))
    plt.subplot(131)
    plt.imshow(gray_image, cmap='gray')
    plt.title('原始图像')

    plt.subplot(132)
    plt.imshow(padded_image, cmap='gray')
    plt.title('边缘填充后的图像')

    plt.subplot(133)
    plt.imshow(filtered_image, cmap='gray')
    plt.title('高斯滤波后的图像')

    plt.show()

except Exception as e:
    print("出现错误:", str(e))
