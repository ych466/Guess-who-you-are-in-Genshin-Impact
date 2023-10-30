import cv2
import os
from ultralytics import YOLO
from tqdm import tqdm

def read_path(file_pathname, model, name_dict, save_folder):
    file_dir = os.listdir(file_pathname)
    for k,v in name_dict.items():
        name_foler = os.path.join(save_folder, v)
        os.makedirs(name_foler)
    #遍历该目录下的所有图片文件
    for filename in tqdm(file_dir):
        print(filename)
        img = cv2.imread(file_pathname+'/'+filename)
        results = model.predict(source=img)

        for result in results:
            # print(result.names)
            name_dict = result.names
            print(name_dict)
            probs = result.probs.cpu().numpy()
            top1_index = result.probs.top1
            class_name = name_dict[top1_index]
            print(class_name)
            save_img_path = os.path.join(save_folder, class_name, filename)
            cv2.imwrite(save_img_path, img)
        print('---------------------------')



if __name__ == '__main__':
    name_dict = {0: 'NG', 1: 'OK'}
    save_folder = 'classify_infer_folder'
    load_img_folder = '/home/lzj/Downloads/pb'
    model = YOLO('runs/classify/train46/weights/best.pt')
    read_path(load_img_folder, model, name_dict, save_folder)


