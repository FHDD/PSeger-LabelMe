# PSeger-LabelMe
[Sensors 2022] This is an efficient annotation tool for image segmentation described in our paper.
<br /> Authors：Yiqing Liu, Hufei Duan
<br /> Date：20220202

# Video presentation
Click [here](https://cloud.tsinghua.edu.cn/f/64c8544971f4413e8d17/) for the video presentation.

# Install
1. Download PSeger-LabelMe program.
```bash
git clone https://github.com/FHDD/PSeger-LabelMe.git
```

2. Put the downloading folder on disk D (or E, F). The folder structure is:
```bash
D:\
└── PSeger-LabelMe\
    └── invasegtool_selfpoints.py
    └── img/
        ├── HEIHC#11_25_10.png
        ├── HEIHC#11_25_11.png
        └── ...
```

3. Run ```invasegtool_selfpoints.py``` in Python environment. Pycharm is recommended.

   Noted that some python pakages is required, such as glob, numpy. You can install them by using the command:
   ```bash
   pip install -r requirements.txt
   ```
   
   or install each package respectively, like:
   ```bash
   pip install numpy
   pip install os
   ...
   ```
   Besides, Python 3.X it self has Tkinter module, so we do not need to install it any more.
   
4. Then, PSeger-LabelMe will be shown.

![image](https://user-images.githubusercontent.com/39789261/182822284-ad0ef778-c6ff-4fec-a606-9e168f13229f.png)



# Usage
## Hotkey instructions
<br /> &emsp;**a**：&emsp;&emsp;&emsp;&emsp;Last page
<br /> &emsp;**d**：&emsp;&emsp;&emsp;&emsp;Next page
<br /> &emsp;**ctrl+z**：&emsp;&emsp;Unmake
<br /> &emsp;**↑**：&emsp;&emsp;&emsp;&emsp;Randomly generate 10 positive boxes，and CSV file is synchronized.
<br /> &emsp;**↓**：&emsp;&emsp;&emsp;&emsp;Randomly generate 10 negtive boxes，and CSV file is synchronized.
<br /> &emsp;**Left mouse button**：&emsp;&emsp;Label as positive or reverse the label. <br /> &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;While clicking the unlabeled position, "label as positive" is performed. <br /> &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;While clicking the labeled position, the positive label will be reversed into a negtive label.
<br /> &emsp;**Right mouse button**：&emsp;&nbsp;Label as negtive or reverse the label. The details are the same as "Left mouse button".
<br /> &emsp;**Middle mouse button**：&ensp;Change the label.
<br />          &emsp;&emsp;(1) Click inside the labeled box. This labeled box and its corresponding annotation in CSV file will be removed.
 <br />         &emsp;&emsp;(2) After executing step (1)，click an unlabeled box (target box). Click on the left side of the center line of the non marking box, the label will be positive. Click on the right side of the center line of the non marking box, it will be negtive.

## Macro definitions in the program
<br /> &emsp;**NUM**：Set the maximum number of boxes that can be marked on each image.
<br /> &emsp;**img_num**：The No. img_num image will be shown first while opening the software.
<br /> &emsp;**grid_or_not**：set grids or not（1 means set，0 means unset.）

## Components
<br /> &emsp;**Image list**：Select one image and click "Confirm". That image will be shown for your annotating.


# Citation
Updating.
