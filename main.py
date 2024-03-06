import cv2
import os
from functions import generate_xml, get_data_from_photo

folder_name = "images"
folder_path = folder_name + '/'
for image_file in os.listdir(folder_path):
    image_height, image_width, image_depth, x_min, y_min, x_max, y_max = get_data_from_photo(folder_name + "/" + image_file)
    objects_data = [
        {
            'name': 'licence',
            'xmin': x_min,
            'ymin': y_min,
            'xmax': x_max,
            'ymax': y_max
        }
    ]
    generate_xml(folder_name, image_file, image_width, image_height, image_depth, objects_data)