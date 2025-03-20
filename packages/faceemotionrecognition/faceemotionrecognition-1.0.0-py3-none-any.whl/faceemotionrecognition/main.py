import tkinter as tk
import cv2
from tkinter import filedialog
from ultralytics import YOLO
import numpy as np
import sys
import os


class YOLOObjectDetectionGUI:
    def __init__(self):
        # 检查是否是打包后的环境
        if getattr(sys, 'frozen', False):
            # 如果是打包后的环境，使用 sys._MEIPASS 获取临时目录
            self.base_path = sys._MEIPASS
        else:
            # 如果是开发环境，使用当前目录
            self.base_path = os.path.dirname(os.path.abspath(__file__))

        # 加载模型
        model_path = os.path.join(self.base_path, 'trained_model.pt')
        try:
            self.model = YOLO(model_path)
        except Exception as e:
            print(f"模型加载失败: {e}")
            sys.exit(1)

        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("YOLO Object Detection")
        self.root.geometry("320x320")

        # 创建一个外层框架用于垂直居中
        self.outer_frame = tk.Frame(self.root)
        self.outer_frame.pack(expand=True)

        # 创建一个内层框架用于放置按钮
        self.button_frame = tk.Frame(self.outer_frame)
        self.button_frame.pack()

        # 创建按钮
        self.create_buttons()

    # 图像缩放函数
    def resize_image(self, image, target_width=640):
        height, width = image.shape[:2]
        aspect_ratio = height / width
        target_height = int(target_width * aspect_ratio)
        dim = (target_width, target_height)
        return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    def process_image(self, file_path):
        try:
            img = cv2.imread(file_path)
            if img is None:
                raise ValueError("无法读取图片文件")
            results = self.model(img)
            annotated_image = results[0].plot()
            resized_image = self.resize_image(annotated_image)
            cv2.imshow('YOLO Object Detection', resized_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return results
        except Exception as e:
            print(f"处理图片时出错: {e}")
            return []

    def process_video(self, cap):
        all_results = []
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                results = self.model(frame)
                all_results.extend(results)
                result = results[0]
                result_frame = result.plot()
                result_frame = np.squeeze(result_frame)
                resized_frame = self.resize_image(result_frame)
                cv2.imshow('YOLO Object Detection', resized_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except Exception as e:
            print(f"处理视频时出错: {e}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
        return all_results

    def detect_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.process_image(file_path)

    def detect_video(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
        if file_path:
            cap = cv2.VideoCapture(file_path)
            self.process_video(cap)

    def detect_camera(self):
        cap = cv2.VideoCapture(0)
        self.process_video(cap)

    def create_buttons(self):
        image_button = tk.Button(self.button_frame, text="Select Image", command=self.detect_image, width=20, height=2)
        image_button.pack(pady=10)

        video_button = tk.Button(self.button_frame, text="Select Video", command=self.detect_video, width=20, height=2)
        video_button.pack(pady=10)

        camera_button = tk.Button(self.button_frame, text="Start Camera", command=self.detect_camera, width=20, height=2)
        camera_button.pack(pady=10)

    def run(self):
        self.root.mainloop()

    def process_file(self, file_path):
        """
        处理本地图片或视频文件，返回检测结果
        :param file_path: 本地图片或视频的路径
        :return: 检测结果列表
        """
        if file_path.lower().endswith(('.jpg', '.png', '.jpeg')):
            return self.process_image(file_path)
        elif file_path.lower().endswith(('.mp4', '.avi')):
            cap = cv2.VideoCapture(file_path)
            return self.process_video(cap)
        else:
            print("不支持的文件类型，请提供图片（.jpg, .png, .jpeg）或视频（.mp4, .avi）文件。")
            return []

    def process_camera(self):
        """
        调用摄像头进行实时目标检测，并返回每帧的检测结果列表
        """
        cap = cv2.VideoCapture(0)
        return self.process_video(cap)


if __name__ == "__main__":
    app = YOLOObjectDetectionGUI()
    app.run()