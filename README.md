# PSeger-LabelMe
[Sensors 2022] This is an efficient annotation tool for image segmentation described in our paper.

# Usage
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
