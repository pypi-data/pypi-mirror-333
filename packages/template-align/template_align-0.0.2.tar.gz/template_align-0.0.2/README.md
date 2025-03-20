# template-align
Align images based on a template

## Installation
Create and select your environment using your favorite environmant management tool, e.g.
```
python -m venv template-environment
source template-environment/bin/activate
``` 
and install via 
```
pip install template-align
```

for a editable installation, clone this project and pipinstall it in development mode
```
clone git@github.com:mathiaszinnen/template-align.git
cd template-align
pip install -e .
```

## Usage
### Command Line
To align a folder of images according to a template image run the alignment tool as follows:
```
template-align PATH/TO/TEMPLATE.jpg PATH/TO/IMAGEDIR 
```
Note that the path arguments have to be adapted. 

By default the aligned images will be saved to `./output/aligned` relative to the current working directory. The output dir can be changed using the `--output-dir` flag. 
```
template-align PATH/TO/TEMPLATE.jpg PATH/TO/IMAGEDIR --output_dir PATH/TO/OUTPUTDIR
```

Visualizations of the mappings can be enabled via the `--visualize` flag. They will be saved to a `matches` subdirectory below the specified output directory. 
```
template-align PATH/TO/TEMPLATE.jpg PATH/TO/IMAGEDIR --visualize 
```

### Python
To align images within python, simply import template-align and invoke the align function:
```python
import os
import cv2
from glob import glob
from template-align import align

image_dir_path = os.path.join('path','to','images')
template_path = os.path.join('path','to','template.jpg')
image_paths = glob.glob(os.path.join(image_dir_path,'*.jpg'))
image_names = [fn for fn in os.listdir(image_dir_path) if os.path.splitext(fn)[-1] == '.jpg']
images = [cv2.imread(p) for p in image_paths]
template = cv2.imread(template_path)

aligned_images = align(images, template, visualization_path=None, image_names=image_names)
``` 

## Acknowledgements
Thank you to Jeta Sopa whose work on template alignment this project is based on.
