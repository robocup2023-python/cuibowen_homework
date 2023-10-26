import numpy as np  # 导入numpy库，用于数学运算
import cv2         # 导入opencv库，用于图像处理
import matplotlib.pyplot as plt  # 导入matplotlib库，用于可视化


def create_gaussian_kernel(kernel_size, sigma):
    center = kernel_size // 2  # 确定滤波核中心点
    kernel = np.zeros((kernel_size, kernel_size))  # 创建全为零的数组，用来存储高斯滤波核
    for i in range(kernel_size):
        for j in range(kernel_size):
            x, y = i - center, j - center
            kernel[i, j] = np.exp(-(x**2 + y**2) / (2.0 * sigma**2))
            kernel[i, j] /= 2 * np.pi * sigma**2  # 根据高斯函数，为每一个核元素赋值

    #  确保滤波核的所有元素和为1
    kernel /= kernel.sum()

    return kernel


kernel_size = int(input("请输入高斯滤波核大小"))
sigma = float(input("请输入高斯方差sigma大小"))


# 创建自定义高斯滤波核
custom_kernel = create_gaussian_kernel(kernel_size, sigma)

# 创建opencv高斯滤波核
opencv_kernel = cv2.getGaussianKernel(kernel_size, sigma)

# 可视化
plt.figure(figsize=(8, 4))
plt.subplot(121)
plt.imshow(custom_kernel, cmap='gray')
plt.title('Custom Gaussian Kernel')

plt.subplot(122)
plt.imshow(opencv_kernel, cmap='gray')
plt.title('OpenCV Gaussian Kernel')

plt.show()
