import os
import cv2
import insightface
import mediapipe as mp
import numpy as np
from sklearn import preprocessing


class FaceRecognition:
    # 初始化人脸识别模型
    def __init__(self, gpu_id=0, face_db='face_db', threshold=1.24, det_thresh=0.50, det_size=(640, 640)):
        """
        人脸识别工具类
        :param gpu_id: 正数为GPU的ID，负数为使用CPU
        :param face_db: 人脸库文件夹
        :param threshold: 人脸识别阈值
        :param det_thresh: 检测阈值
        :param det_size: 检测模型图片大小
        """
        self.gpu_id = gpu_id
        self.face_db = face_db
        self.threshold = threshold
        self.det_thresh = det_thresh
        self.det_size = det_size

        # 加载人脸识别模型，当allowed_modules=['detection', 'recognition']时，只单纯检测和识别
        self.model = insightface.app.FaceAnalysis(root='./',
                                                  allowed_modules=None,
                                                  providers=['CUDAExecutionProvider'])
        self.model.prepare(ctx_id=self.gpu_id, det_thresh=self.det_thresh, det_size=self.det_size)
        # 人脸库的人脸特征
        self.faces_embedding = list()
        # 加载人脸库中的人脸
        self.load_faces(self.face_db)

    # 加载人脸库中的人脸
    def load_faces(self, face_db_path):
        if not os.path.exists(face_db_path):
            os.makedirs(face_db_path)
        for root, dirs, files in os.walk(face_db_path):
            for file in files:
                input_image = cv2.imdecode(np.fromfile(os.path.join(root, file), dtype=np.uint8), 1)
                user_name = file.split(".")[0]
                face = self.model.get(input_image)[0]
                embedding = np.array(face.embedding).reshape((1, -1))
                embedding = preprocessing.normalize(embedding)
                self.faces_embedding.append({
                    "user_name": user_name,
                    "feature": embedding
                })

    # 欧式距离计算函数
    @staticmethod
    def feature_compare(feature1, feature2, threshold):
        diff = np.subtract(feature1, feature2)
        dist = np.linalg.norm(diff)
        return dist < threshold

    # 人脸识别函数
    def recognition(self, embedding):
        user_name = "unknown"
        for com_face in self.faces_embedding:
            r = self.feature_compare(embedding, com_face['feature'], self.threshold)
            if r:
                user_name = com_face["user_name"]

        return user_name

    # 添加没有在库中的人脸
    def register(self, image, user_name):
        faces = self.model.get(image)
        if len(faces) != 1:
            return '图片检测不到人脸或人脸多于1'
        # 判断人脸是否存在
        embedding = np.array(faces[0].embedding).reshape((1, -1))
        embedding = preprocessing.normalize(embedding)
        is_exits = False
        for com_face in self.faces_embedding:
            r = self.feature_compare(embedding, com_face["feature"], self.threshold)
            if r:
                is_exits = True
        if is_exits:
            return '该用户已存在'
        # 符合注册条件保存图片，同时把特征添加到人脸特征库中
        cv2.imencode('.png', image)[1].tofile(os.path.join(self.face_db, '%s.png' % user_name))
        self.faces_embedding.append({
            "user_name": user_name,
            "feature": embedding
        })
        return "success"

    # 通用人脸检测函数
    def detect(self, image_detect):
        faces = self.model.get(image_detect)
        results = list()
        for face in faces:
            result = dict()
            # 获取人脸属性
            result["bbox"] = np.array(face.bbox).astype(np.int32).tolist()
            result["kps"] = np.array(face.kps).astype(np.int32).tolist()
            # 开始人脸识别
            embedding = np.array(face.embedding).reshape((1, -1))
            embedding = preprocessing.normalize(embedding)
            result["embedding"] = embedding
            results.append(result)
        return results

    # 绘制人脸框和信息
    def draw_faces(self, img_draw):
        """
        在图像上绘制人脸框、标注姓名和关键点
        :param img_draw: 输入图像
        """
        faces_info = self.detect(img_draw)
        # 获取人脸信息列表中各项数据
        for face_info in faces_info:
            bbox = face_info['bbox']
            x, y, w, h = bbox
            embedding = face_info['embedding']
            user_name = self.recognition(embedding)

            # 进行手势检测
            gesture = detect_gestures(img_draw, (x, y), (x+w, y+h))

            # 绘制人脸框
            cv2.rectangle(img_draw, (x, y), (w, h), (0, 255, 0), 2)
            # 标注姓名
            cv2.putText(img_draw, f'User: {user_name}, Gesture: {gesture}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)

        return img_draw


# 对摄像头前人脸进行识别
def cap_recognize():
    cap = cv2.VideoCapture(0)
    face_recognition = FaceRecognition()  # 对人脸识别模型进行类实例化
    while True:
        ret, img_cap = cap.read()
        # 调用绘制人脸框和姓名的函数
        img_with_faces = face_recognition.draw_faces(img_cap)

        # 显示结果
        cv2.imshow('Face Recognition', img_with_faces)

        # 按q退出循环
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # 释放摄像头，关闭窗口
    cap.release()
    cv2.destroyAllWindows()


# 手势检测函数
def detect_gestures(image_numpy, top_left, bottom_right):
    gesture = 'no_gesture'
    # 初始化MediaPipe手部模块
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # 读取输入图像
    height, width, _ = image_numpy.shape

    # 转换为RGB格式
    image_rgb = cv2.cvtColor(image_numpy, cv2.COLOR_BGR2RGB)

    # 执行手势检测
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        # 遍历每一只检测到的手
        for hand_landmarks in results.multi_hand_landmarks:
            # 获取的指尖坐标
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            ring_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]
            pinky_tip = hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP]

            # 将关键点坐标转换为图像坐标
            thumb_tip_x, thumb_tip_y = int(thumb_tip.x * width), int(thumb_tip.y * height)
            index_finger_tip_x, index_finger_tip_y = int(index_finger_tip.x * width), int(index_finger_tip.y * height)

            # 检查手的关键点是否在指定的坐标范围内
            region_x1, region_y1 = top_left
            region_x2, region_y2 = bottom_right
            if region_x1 <= thumb_tip_x <= region_x2 and region_y1 <= thumb_tip_y <= region_y2 and \
                    region_x1 <= index_finger_tip_x <= region_x2 and region_y1 <= index_finger_tip_y <= region_y2:
                # 计算大拇指和食指之间的距离
                distance = ((thumb_tip.x - index_finger_tip.x) ** 2 + (thumb_tip.y - index_finger_tip.y) ** 2) ** 0.5

                # 判断是否形成"OK"手势
                if distance < 0.00005 * width:  # 调整这个阈值以适应实际情况
                    gesture = 'ok'
                # 计算其他指尖距离
                dist_thumb_index = ((thumb_tip.x - index_finger_tip.x) ** 2 + (
                            thumb_tip.y - index_finger_tip.y) ** 2) ** 0.5
                dist_thumb_ring = ((thumb_tip.x - ring_finger_tip.x) ** 2 + (thumb_tip.y - ring_finger_tip.y) ** 2) ** 0.5
                dist_thumb_pinky = ((thumb_tip.x - pinky_tip.x) ** 2 + (thumb_tip.y - pinky_tip.y) ** 2) ** 0.5

                # 定义经验值
                threshold_large_distance = 0.12
                threshold_small_distance = 0.12

                # 判断是否形成"Yes"手势
                if (
                        dist_thumb_index > threshold_large_distance and
                        dist_thumb_ring < threshold_small_distance and
                        dist_thumb_pinky < threshold_small_distance

                ):
                    gesture = 'yes'

    # 关闭MediaPipe手部模块
    hands.close()
    return gesture


cap_recognize()
