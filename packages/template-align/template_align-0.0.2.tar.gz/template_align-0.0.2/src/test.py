import os
import cv2
from glob import glob
from template_align import align

image_dir_path = os.path.join('test_data','input')
template_path = os.path.join('test_data','template.jpeg')
image_paths = glob(os.path.join(image_dir_path,'*.jpeg'))
image_names = [fn for fn in os.listdir(image_dir_path) if os.path.splitext(fn)[-1] == '.jpeg']
images = [cv2.imread(p) for p in image_paths]
template = cv2.imread(template_path)

aligned_images = align(images, template, visualization_path=None, image_names=image_names)
print(len(aligned_images))