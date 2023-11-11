from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


def calculate_histogram(image):
    # 计算图像的灰度直方图
    image_array = np.array(image)
    histogram, bins = np.histogram(image_array.flatten(), 256, [0, 256])
    return histogram, bins


def plot_histogram(histogram, bins, title):
    # 可视化直方图
    plt.figure()
    plt.title(title)
    plt.bar(bins[:-1], histogram, width=1)
    plt.show()


def histogram_equalization(image):
    # 图像直方图均衡化
    image_array = np.array(image)
    hist, _ = np.histogram(image_array.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * float(hist.max()) / cdf.max()
    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')

    return cdf[image_array]


def main():
    # 接收用户输入的图片文件名
    file_name = input("请输入图片文件名: ")

    # 打开图像文件
    image = Image.open(file_name).convert('L')  # 转换为灰度图

    # 计算原始图像的直方图
    original_histogram, bins = calculate_histogram(image)
    plot_histogram(original_histogram, bins, "Original Histogram")

    # 直方图均衡化
    equalized_image = Image.fromarray(histogram_equalization(image))
    equalized_histogram, _ = calculate_histogram(equalized_image)
    plot_histogram(equalized_histogram, bins, "Equalized Histogram")

    # 可视化对比图
    plt.figure()

    # 原始图片和均衡化后的图片对比
    plt.subplot(2, 2, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.imshow(equalized_image, cmap='gray')
    plt.title('Equalized Image')
    plt.axis('off')

    # 原始图片和均衡化后的直方图对比
    plt.subplot(2, 2, 3)
    plt.bar(bins[:-1], original_histogram, width=1)
    plt.title('Original Histogram')

    plt.subplot(2, 2, 4)
    plt.bar(bins[:-1], equalized_histogram, width=1)
    plt.title('Equalized Histogram')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
