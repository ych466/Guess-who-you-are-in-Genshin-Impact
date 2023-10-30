# 工具类
import os
import random
from shutil import copy2

def data_set_split(src_data_folder, target_data_folder, test_scale=0.1):
    '''
    读取源数据文件夹，生成划分好的文件夹，分为train、val两个文件夹进行
    :param src_data_folder: 源文件夹
    :param target_data_folder: 目标文件夹
    :param test_scale: 测试集比例
    :return:
    '''
    print("开始数据集划分")
    class_names = os.listdir(src_data_folder)
    # 在目标目录下创建文件夹
    split_names = ['train', 'val', 'test']
    for split_name in split_names:
        split_path = os.path.join(target_data_folder, split_name)
        if os.path.isdir(split_path):
            pass
        else:
            os.makedirs(split_path)
        # 然后在split_path的目录下创建类别文件夹
        if split_name != 'test':
            for class_name in class_names:
                class_split_path = os.path.join(split_path, class_name)
                if os.path.isdir(class_split_path):
                    pass
                else:
                    os.makedirs(class_split_path)

    # 按照比例划分数据集，并进行数据图片的复制
    # 首先进行分类遍历
    for class_name in class_names:
        current_class_data_path = os.path.join(src_data_folder, class_name)
        current_all_data = os.listdir(current_class_data_path)
        current_data_length = len(current_all_data)
        current_data_index_list = list(range(current_data_length))
        random.shuffle(current_data_index_list)

        test_folder = os.path.join(target_data_folder, 'test')
        train_folder = os.path.join(os.path.join(target_data_folder, 'train'), class_name)
        val_folder = os.path.join(os.path.join(target_data_folder, 'val'), class_name)

        test_stop_flag = current_data_length * test_scale
        train_stop_flag = current_data_length * (1 - test_scale)

        current_idx = 0
        test_num = 0
        train_num = 0
        val_num = 0

        for i in current_data_index_list:
            src_img_path = os.path.join(current_class_data_path, current_all_data[i])
            if current_idx <= test_stop_flag:
                # Copy to test folder
                dst_img_path = os.path.join(test_folder, f'{class_name}_{test_num}.jpg')
                copy2(src_img_path, dst_img_path)
                test_num += 1
            elif current_idx <= train_stop_flag:
                # Copy to train folder
                dst_img_path = os.path.join(train_folder, f'{class_name}_{train_num}.jpg')
                copy2(src_img_path, dst_img_path)
                train_num += 1
            else:
                # Copy to val folder
                dst_img_path = os.path.join(val_folder, f'{class_name}_{val_num}.jpg')
                copy2(src_img_path, dst_img_path)
                val_num += 1

            current_idx = current_idx + 1

        print("*********************************{}*************************************".format(class_name))
        print("{}类按照{}：{}：{}的比例划分完成，一共{}张图片".format(class_name, test_scale, 1 - test_scale, 1 - test_scale, current_data_length))
        print("测试集{}：{}张".format(test_folder, test_num))
        print("训练集{}：{}张".format(train_folder, train_num))
        print("验证集{}：{}张".format(val_folder, val_num))


if __name__ == '__main__':
    src_data_folder = "datasets"
    target_data_folder = "dataset/"
    data_set_split(src_data_folder, target_data_folder, test_scale=0.1)
