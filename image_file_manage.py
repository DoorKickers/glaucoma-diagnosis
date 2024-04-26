import os
import numpy as np
import re

class ImageFileManage():
    @staticmethod
    def check_file_prefix_is_given_value(filename: str, given_value: str) -> bool:
        match = re.match(r'^(\d+)', filename)
        if match:
            id_value = match.group(1)
            return id_value == given_value
        else:
            return False
    @staticmethod
    def is_image_file(filename: str) -> bool:
        image_extensions = ('.jpg', '.jpeg', '.png')
        lower_filename = filename.lower()
        return any(lower_filename.endswith(ext) for ext in image_extensions)
    
    @staticmethod
    def get_all_image_file(tar_dir: str) -> list:
        result_list = []
        for filename in os.listdir(tar_dir):
            full_dir = os.path.join(tar_dir, filename)
            if os.path.isfile(full_dir) and ImageFileManage.is_image_file(filename):
                result_list.append(full_dir)
        return result_list
    
    @staticmethod
    def get_image_path_list_by_patient_id(image_dir: str, patient_id: int) -> list:
        result_list = []
        for dir_name in os.listdir(image_dir):
            patient_img_dir = os.path.join(image_dir, dir_name)
            if os.path.isfile(patient_img_dir) == False \
                and ImageFileManage.check_file_prefix_is_given_value(dir_name, str(patient_id)) == True:
                result_list = ImageFileManage.get_all_image_file(patient_img_dir)
                break
        return result_list



