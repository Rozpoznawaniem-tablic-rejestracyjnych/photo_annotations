import os
import xml.etree.cElementTree as ET
import cv2
def generate_xml(folder, filename, width, height, depth, objects):
    annotation = ET.Element("annotation")

    folder_elem = ET.SubElement(annotation, "folder")
    folder_elem.text = folder

    filename_elem = ET.SubElement(annotation, "filename")
    filename_elem.text = filename

    size_elem = ET.SubElement(annotation, "size")
    width_elem = ET.SubElement(size_elem, "width")
    width_elem.text = str(width)
    height_elem = ET.SubElement(size_elem, "height")
    height_elem.text = str(height)
    depth_elem = ET.SubElement(size_elem, "depth")
    depth_elem.text = str(depth)

    segmented_elem = ET.SubElement(annotation, "segmented")
    segmented_elem.text = "0"

    for obj in objects:
        object_elem = ET.SubElement(annotation, "object")

        name_elem = ET.SubElement(object_elem, "name")
        name_elem.text = obj['name']

        pose_elem = ET.SubElement(object_elem, "pose")
        pose_elem.text = "Unspecified"

        truncated_elem = ET.SubElement(object_elem, "truncated")
        truncated_elem.text = "0"

        occluded_elem = ET.SubElement(object_elem, "occluded")
        occluded_elem.text = "0"

        difficult_elem = ET.SubElement(object_elem, "difficult")
        difficult_elem.text = "0"

        bndbox_elem = ET.SubElement(object_elem, "bndbox")
        xmin_elem = ET.SubElement(bndbox_elem, "xmin")
        xmin_elem.text = str(obj['xmin'])
        ymin_elem = ET.SubElement(bndbox_elem, "ymin")
        ymin_elem.text = str(obj['ymin'])
        xmax_elem = ET.SubElement(bndbox_elem, "xmax")
        xmax_elem.text = str(obj['xmax'])
        ymax_elem = ET.SubElement(bndbox_elem, "ymax")
        ymax_elem.text = str(obj['ymax'])
    name = filename.split(".")
    tree = ET.ElementTree(annotation)
    tree.write(os.path.join('annotation/', name[0] + '.xml'))


coordinates = []
scale = 0

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(param, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow('image', param)
        coordinates.append((x, y))


def get_data_from_photo(image_path, resized_width, resized_height):
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    depth = img.shape[2] if len(img.shape) == 3 else 1
    scale_width = resized_width / width
    scale_height = resized_height / height
    resized_img = cv2.resize(img, (resized_width, resized_height), interpolation=cv2.INTER_AREA)
    cv2.imshow('image', resized_img)
    cv2.setMouseCallback('image', click_event, resized_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    x_min = int(min(coordinates[0][0], coordinates[1][0]) / scale_height)
    y_min = int(min(coordinates[0][1], coordinates[1][1]) / scale_width)
    x_max = int(max(coordinates[0][0], coordinates[1][0]) / scale_height)
    y_max = int(max(coordinates[0][1], coordinates[1][1]) / scale_width)
    coordinates.clear()
    return height, width, depth, x_min, y_min, x_max, y_max

