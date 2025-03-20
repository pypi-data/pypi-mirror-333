import argparse
import cv2
from glob import glob
from tqdm import tqdm
import os
import numpy as np

def align(images, template, visualization_path=None, image_names=None):
    if image_names is None: 
        image_names = [""] * len(images)

    sift = cv2.SIFT_create()

    kps_tmpl, desc_tmpl = sift.detectAndCompute(template,None)

    aligned_images = []
    for image, name in tqdm(zip(images,image_names), total=len(images)):
        kps_img, desc_img = sift.detectAndCompute(image,None)
        matches = _find_matches(desc_img, desc_tmpl)
        matches = _filter_matches(matches)

        if visualization_path is not None:
            matched_image = cv2.drawMatches(image,kps_img,template,kps_tmpl,matches,None)
            cv2.imwrite(os.path.join(visualization_path,name),matched_image)

        matching_pts_img = np.array([kps_img[m.queryIdx].pt for m in matches])
        matching_pts_tmpl = np.array([kps_tmpl[m.trainIdx].pt for m in matches])
    
        H,_ = cv2.findHomography(matching_pts_img, matching_pts_tmpl, cv2.RANSAC)
        w,h = template.shape[:2]
        image_aligned = cv2.warpPerspective(image, H, (h,w))

        aligned_images.append(image_aligned)

    return aligned_images

def _find_matches(descs_a, descs_b):
    matcher = cv2.BFMatcher(cv2.NORM_L2,crossCheck=False)
    matches = matcher.knnMatch(descs_a, descs_b,k=2)
    return matches

def _filter_matches(matches, thresh = 0.8, n_matches=50):
    matches = [m for m,n in matches if m.distance < thresh * n.distance]
    matches.sort(key=lambda x: x.distance)
    return matches[:n_matches]


def _read_images(input_dir):
    im_exts = ["jpg","jpeg","tiff","bmp"]
    image_paths = []
    for ext in im_exts: 
        image_paths.extend(glob(os.path.join(input_dir,f'*.{ext}')))
    images = [cv2.imread(impath) for impath in image_paths]
    image_names = [os.path.basename(image_path) for image_path in image_paths]
    return images, image_names

def _save_images(images, names, path):
    for image,name in tqdm(zip(images,names),total=len(images)):
        cv2.imwrite(os.path.join(path,name),image)

def main():
    parser = argparse.ArgumentParser(description="Aligns images based on a template.")
    parser.add_argument('template', help='Path to the template image file')
    parser.add_argument('input_dir', help='Path to a folder containing the images to be aligned.')
    parser.add_argument('--output_dir', help='Directory to save aligned images and visualizations', 
                        default=os.path.join('output','aligned'),
                        required=False)
    parser.add_argument('--visualize', help='Visualize matches', action='store_true') 
    args = parser.parse_args()

    os.makedirs(os.path.join(args.output_dir,'aligned'), exist_ok=True)
    if args.visualize:
        visualization_path = os.path.join(args.output_dir,'matches')
        os.makedirs(visualization_path, exist_ok=True)
    else: visualization_path = None

    images, image_names = _read_images(args.input_dir)
    print(f'Aligning {len(images)} images.')
    template = cv2.imread(args.template)
    aligned_images = align(images, template, visualization_path=visualization_path, image_names=image_names)
    print(f'Saving {len(images)} aligned images to {args.output_dir}.')
    _save_images(aligned_images,image_names,args.output_dir)


if __name__ == '__main__':
    input_dir = 'test_data/input/'
    template_path = 'test_data/template.jpeg'
    images, image_names = _read_images(input_dir)
    template = cv2.imread(template_path)
    aligned_images = align(images, template,visualization_path='output/matches',image_names=image_names)
    _save_images(aligned_images,image_names,'output/aligned')
