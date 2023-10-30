from ultralytics import YOLO

model = YOLO("yolo-cls/yolov8x-cls.pt")  #根据需求选择模型,见yolo官网
if __name__ == '__main__':
    model.train(data='dataset', epochs=100, batch=-1, imgsz=150) #根据需要设置参数