# PSeger-LabelMe
[Sensors 2022] This is an efficient annotation tool for image segmentation described in our paper.
<br /> Authors：Yiqing Liu, Hufei Duan
<br /> Date：20220202

# Usage
【Hotkey instructions】
 <br /> a：Last page
 <br /> d：Next page
 <br /> ctrl+z：Unmake
 <br /> ↑：Randomly generate 10 positive boxes，and CSV file is synchronized.
 <br /> ↓：Randomly generate 10 negtive boxes，and CSV file is synchronized.
<br /> Left mouse button：label as positive or reverse the label (When clicking the unlabeled position, "label as positive" is performed. When clicking the labeled position, the positive label will be reversed into negtive label.)
<br /> Right mouse button：label as negtive
<br /> Middle mouse button：change the label
<br />          (1) 点击标注框内部，去除该标注框及其csv标注
 <br />         (2) 执行(1)后，随即点击非标注框（作为修改后的标注框）；在非标注框中线左侧点击，为阳性；在非标注框中线右侧点击，为阴性

【关于程序中的宏定义】
<br /> NUM：设置每张图能标注最多NUM个框
<br /> img_num：设置打开软件时，从文件列表中第img_num张图开始显示（文件列表非文件夹，对文件夹进行了随机化处理，random.seed(0)）
<br /> grid_or_not：是否设置框线（1为画框线，0为不画框线）

【控件】
<br /> 标注框列表：选中列表某一行，点击按钮‘确定’，


# Install
1. Download PSeger-LabelMe program.
```bash
git clone https://github.com/FHDD/PSeger-LabelMe.git
```

2. Put the downloading folder on disk D (or E, F). The folder structure is:
```bash
D:
  \PSeger-LabelMe
      invasegtool_selfpoints.py
      \img
          HEIHC#11_25_10.png
          HEIHC#11_25_11.png
          ...
```

3. Run ```invasegtool_selfpoints.py``` in Python environment. Pycharm is recommended.

   Noted that some python pakages is required, such as tkinter, glob, numpy. You can install them by using the command:
   ```bash
   pip install -r requirements.txt
   ```
   
   or install each package respectively, like:
   ```bash
   pip install numpy
   pip install os
   sudo apt-get install python3-tk
   ...
   ```
   
4. Then, PSeger-LabelMe will be shown.

![image](https://user-images.githubusercontent.com/39789261/182822284-ad0ef778-c6ff-4fec-a606-9e168f13229f.png)





