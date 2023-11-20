import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("Lenna.jpg", 0)

img_float = np.float32(img)

# 进行傅立叶变换
dft = cv2.dft(img_float, flags=cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)    # 将零频率移到图像中心

img_magnitude = cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1])    # 计算幅度谱
img_phase = np.angle(dft_shift[:, :, 0] + 1j * dft_shift[:, :, 1])    # 计算相位谱

rows, cols = img_float.shape
crow, ccol = int(rows/2), int(cols/2)    # 找到频域图中点

# 构造掩码
mask = np.zeros((rows, cols, 2), np.uint8)   # 创建全零数组
mask[crow-30:crow+30, ccol-30:ccol+30] = 1    # 将中心60 * 60区域标记为1

# 应用掩码并进行反变换
dft_shift = dft_shift * mask    # 应用掩码
f_shift = np.fft.ifftshift(dft_shift)    # 将零频率移回左上角
img_back = cv2.idft(f_shift)    # 进行傅立叶反变换
img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])    # 对双通道进行处理，还原出可视化幅度图


# 可视化低通滤波
plt.subplot(121), plt.imshow(img, cmap="gray")
plt.title("Input Image")
plt.subplot(122), plt.imshow(img_back, cmap="gray")
plt.title("Output Image")
plt.show(block=False)

# 可视化幅度谱、相位谱
plt.figure()
plt.subplot(131), plt.imshow(img, cmap="gray")
plt.title("Original Image")
plt.subplot(132), plt.imshow(np.log(1 + img_magnitude), cmap="gray")
plt.title("Magnitude Image")
plt.subplot(133), plt.imshow(img_phase, cmap="gray")
plt.title("Phase Image")
plt.show()