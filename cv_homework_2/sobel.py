import numpy as np
import matplotlib.pyplot as plt
from PIL import Image  # 用于图像读取和显示

# Sobel 算子
def sobel_operator(image):
    # Sobel 算子的 x 和 y 方向上的卷积核
    kernel_x = np.array([[-1, 0, 1],
                         [-2, 0, 2],
                         [-1, 0, 1]])

    kernel_y = np.array([[-1, -2, -1],
                         [0, 0, 0],
                         [1, 2, 1]])

    # 图像灰度化
    gray = np.array(image.convert("L"))

    # 初始化输出的图像数组
    gradient_magnitude = np.zeros_like(gray)

    # 对图像进行sobel滤波
    for i in range(1, gray.shape[0] - 1):
        for j in range(1, gray.shape[1] - 1):
            gx = np.sum(np.multiply(kernel_x, gray[i - 1:i + 2, j - 1:j + 2]))
            gy = np.sum(np.multiply(kernel_y, gray[i - 1:i + 2, j - 1:j + 2]))
            gradient_magnitude[i, j] = np.sqrt(gx**2 + gy**2)

    return gradient_magnitude

# 可视化图像
def visualize_image(image):
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.title('Sobel Filtered Image')
    plt.show()

# 用户输入图像文件名
image_path = input("请输入图像文件名：")

# 读取图像
img = Image.open(image_path)

if img is not None:
    # 执行Sobel算子
    sobel_image = sobel_operator(img)

    # 可视化滤波结果
    visualize_image(sobel_image)
else:
    print("无法读取图像，请检查文件路径或文件是否存在。")
