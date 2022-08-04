'''
Author：Yiqing Liu, Hufei Duan
Date：20220202
Version：v5.4
【快捷键使用说明】
a：左翻页
d：右翻页
ctrl+z：撤销（在标注过程中使用，应避免撤销第一个框）
↑：随机生成10个阳性框，且同步csv文件
↓：随机生成10个阴性框，且同步csv文件
鼠标左键：阳性标注 及 标注反转（点击未表框的位置，进行阳性标注；点击已标框的位置，进行标注反转）
鼠标右键：阴性标注
鼠标中键：修改标注
         (1) 点击标注框内部，去除该标注框及其csv标注
         (2) 执行(1)后，随即点击非标注框（作为修改后的标注框）；在非标注框中线左侧点击，为阳性；在非标注框中线右侧点击，为阴性
【关于程序中的宏定义】
NUM：设置每张图能标注最多NUM个框
img_num：设置打开软件时，从文件列表中第img_num张图开始显示（文件列表非文件夹，对文件夹进行了随机化处理，random.seed(0)）
grid_or_not：是否设置框线（1为画框线，0为不画框线）
【控件】
标注框列表：选中列表某一行，点击按钮‘确定’，
'''

import tkinter as tk
from PIL import Image, ImageTk
import glob
import os
import tkinter.messagebox
import numpy as np
import random
import csv
import pandas as pd
import time

global NUM
NUM = 10
grid_or_not = 1  # 1为画框线，0为不画框线
root = tk.Tk()

root.wm_geometry("1000x1000+500+5")

imgs = glob.glob(os.path.join(r'D:\PSeger-LabelMe\img','*.png'))
csv_path='label_selfpoints.csv'
random.seed(0)
random.shuffle(imgs)

# imgs = glob.glob(os.path.join(r'H:\lyq_11-19\1901483-HE-IHC', '*.png'))
# csv_path = r'..\csv_files\label_1901483-HE-IHC.csv'
# TODO listbox字体-布局调整-审核函数-四个按钮及排序功能
'''设置listbox控件'''
lbVal=tkinter.StringVar()
global ord_status    # 设置哪一种列表框排序方式
ord_status=4
global ord_imgs      # 排序专用的ord_imgs，以区分原始固定随机种子的imgs
ord_imgs=imgs.copy()
# def show_listbox(status=4):
def get_index_of_filename(filename):
    # filename样例：N61184-1H-HEIHC#11_25_11.png中的11
    index_of_filename=int(filename.split('_')[-1].split('.')[0])
    return index_of_filename

def show_listbox(status):
    global lb
    global str_name
    str_name = []
    global df_list
    df_list = pd.read_csv(csv_path, encoding="utf-8")
    global ord_imgs
    if status==1:
        ord_imgs.sort(key=lambda x:get_index_of_filename(x))
        print('1ok')
    elif status==2:
        global _str_name_1
        _str_name_1 = []
        global _str_name_2
        _str_name_2 = []
        print('2ok')
    elif status==3:
        random.seed()
        random.shuffle(ord_imgs)
        print('3ok')
    elif status==4:
        ord_imgs=imgs.copy()
        print('4ok')

    for i in ord_imgs:

        if i.split('\\')[-1] in list(df_list.img_path):
            # if len(df_list[df_list.img_path==i.split('\\')[-1]]['labels_info'].values[0].split(',')) != 10*3:    # 增加异常行显示
            if len(eval(df_list[df_list.img_path==i.split('\\')[-1]]['labels_info'].values[0])) != 10:    # 增加异常行显示
                str_name.append('? ' + i.split('\\')[-1])
                if status==2:_str_name_1.append('? ' + i.split('\\')[-1])

            else:
                str_name.append('√ ' + i.split('\\')[-1])
                if status==2:_str_name_1.append('√ ' + i.split('\\')[-1])
        else:
            str_name.append(i.split('\\')[-1])
            if status == 2: _str_name_2.append(i.split('\\')[-1])
        # str_name.append(i.split('\\')[-1])


    if status==2:
        _str_name_1.sort(key=lambda x:get_index_of_filename(x))
        _str_name_2.sort(key=lambda x:get_index_of_filename(x))
        str_name=_str_name_1+_str_name_2
        ord_imgs=[os.path.join(r'D:\PSeger\img',_str_name_1[i][2:]) for i in range(len(_str_name_1))]
        ord_imgs+=[os.path.join(r'D:\PSeger\img',_str_name_2[i]) for i in range(len(_str_name_2))]
        # ord_imgs=[os.path.join(r'D:\PSeger\img',str_name[i]) for i in range(len(str_name))]
        print('ok')

    for i_str_name in range(len(str_name)):
        if str_name[i_str_name][0]!='√' and str_name[i_str_name][0]!='?':
            str_name[i_str_name]=' '*2+str_name[i_str_name]
    lbVal.set(str_name)
    # lb = tkinter.Listbox(root, listvariable=lbVal)
    lb = tkinter.Listbox(root, listvariable=lbVal,font=("Helvetica",15),height=20,width=30)
    # lb.place(x=256 * 3 + 80, y=16)
    lb.place(x=256 * 3-50, y=16*3)

'''设置listbox对应的button'''
def getListBoxValue():
    global img_num
    global _path
    global lb
    num_list=lb.curselection()
    # val_list=lb.get(lb.curselection())

    tile_list.clear()
    # re_load_img(num_list[0], imgs[num_list[0]])
    re_load_img(num_list[0], ord_imgs[num_list[0]])
    df = pd.read_csv(csv_path, encoding="utf-8")
    try:
        content_now_str = df[df.img_path == _path.split('\\')[-1]]['labels_info'].values[0]
        content_now = eval(content_now_str)
    except (IndexError,):
        return
    tile_list.load_from_list(content_now)
    print('ok')
'''设置button所在的label的函数——原因：tkinter的button的字体变大，形状也变大'''
def label_out_btn(w,h,co_x,co_y):
    label_btn = tkinter.LabelFrame(root, width=w, height=h)
    label_btn.place(x=co_x, y=co_y)
    label_btn.grid_rowconfigure(0, weight=1)
    label_btn.grid_columnconfigure(0, weight=1)
    label_btn.grid_propagate(False)
    return label_btn
label_confirm=label_out_btn(100,50,256*3+60-50,16*3+560)
clickBtn=tkinter.Button(label_confirm,text='确 认',command=getListBoxValue,font=('microsoft yahei', 14),relief='flat',cursor='hand2')
clickBtn.grid(row=0, column=0, sticky='nesw')

'''设计列表框排序功能的button'''
def forwa_ord():
    global ord_status
    ord_status=1
    show_listbox(ord_status)
    print('ok')
label_forwa_ord=label_out_btn(50,25,256*3-50, 48-24)
clickBtn_forwa_ord=tkinter.Button(label_forwa_ord,text='name',command=forwa_ord,font=('microsoft yahei', 10),relief='flat')
clickBtn_forwa_ord.grid(row=0, column=0, sticky='nesw')

def has_anno_ord():
    global ord_status
    ord_status=2
    show_listbox(ord_status)
    print('ok')
label_has_anno=label_out_btn(50,25,256*3, 48-24)
clickBtn_has_anno=tkinter.Button(label_has_anno,text='annotated',command=has_anno_ord,font=('microsoft yahei', 10),relief='flat')
clickBtn_has_anno.grid(row=0, column=0, sticky='nesw')

def random_ord():
    global ord_status
    ord_status=3
    show_listbox(ord_status)
    print('ok')
label_random=label_out_btn(50,25,256*3+50, 48-24)
clickBtn_random=tkinter.Button(label_random,text='random',command=random_ord,font=('microsoft yahei', 10),relief='flat')
clickBtn_random.grid(row=0, column=0, sticky='nesw')

def origin_ord():
    global ord_status
    ord_status=4
    show_listbox(ord_status)
    print('ok')
label_origin=label_out_btn(50,25,256*3+50*2, 48-24)
clickBtn_origin=tkinter.Button(label_origin,text='initial',command=origin_ord,font=('microsoft yahei', 10),relief='flat')
clickBtn_origin.grid(row=0, column=0, sticky='nesw')

if not os.path.exists(csv_path):
    with open(csv_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(['img_path', 'labels_info'])  # 【】
        print('文件不存在')


class Tile:
    def __init__(self, idx, coord, label):
        self.idx = idx
        self.coord = coord
        self.label = label
        self.color = ['green', 'red']
        self.patch_size = 16
        self.mag_factor = 3

    def change_box_label(self, removal=False):
        if removal:
            canvas.itemconfig(self.rect, outline='black')
            return
        self.label = 1 - self.label
        canvas.itemconfig(self.rect, outline=self.color[self.label])

    def del_box(self):
        canvas.delete(self.rect)
        canvas.delete(self.text)

    def create_rectangle_color(self):  # a=0, b=1
        a = self.coord[0] * self.mag_factor
        b = self.coord[1] * self.mag_factor
        c = self.patch_size * self.mag_factor
        self.rect = canvas.create_rectangle(a, b, a + c, b + c, outline=self.color[self.label], width=3)
        self.text = canvas.create_text(a + 5, b, text=str(self.idx), fill='yellow', font=('purisa', 20))


class TileList:
    def __init__(self):
        self.max_length = 10
        self.list = []
        self.idx_to_del = -1

    def append(self, tile):
        self.list.append(tile)

    def insert(self, m, tile):
        self.list.insert(m, tile)

    def clear(self):
        while self.list:
            tile = self.list.pop()
            tile.del_box()
        self.idx_to_del = -1

    def remove_box(self, idx):
        tile = self.list.pop(idx)
        tile.del_box()

    def load_from_list(self, source_list):
        for i_load_img, (coord, point_label) in enumerate(source_list):
            tile = Tile(i_load_img, coord, point_label)
            tile.create_rectangle_color()
            self.append(tile)

    def if_point_in_any_box(self, x, y):
        coord_x = (int(x / 48)) * 16
        coord_y = (int(y / 48)) * 16
        for i_mouse, tile_i in enumerate(self.list):
            if (coord_x, coord_y) == tile_i.coord:
                return i_mouse
        return -1

    def gen_random_tiles(self, key):
        color = {'w': 'red', 's': 'green'}[key]
        label = {'w': 1, 's': 0}[key]

        random_list = random.sample(range(1, 196), 10)  # 生成10个1~196的不重复的随机数
        annotations = []
        for i, tile_i in enumerate(random_list):
            tile_row = tile_i // 14  # 1
            tile_column = tile_i % 14  # 13
            coord = (tile_column * 16, tile_row * 16)
            tile = Tile(i, coord, label)
            tile.create_rectangle_color()
            self.append(tile)
            annotations.append((coord, label))
        return annotations

    def __len__(self):
        return len(self.list)

tile_list = TileList()


def create_rectangle_color(tile_n, a, b, color="green"):  # a=0, b=1
    c = 16 * 3
    # canvas.create_rectangle(b, a, b + c, a + c, outline=color, dash=(3, 5), width=3)
    canvas.create_rectangle(b, a, b + c, a + c, outline=color, width=3)
    canvas.create_text(b + 5, a, text=str(tile_n), fill='yellow', font=('purisa', 20))


def create_grid(status, color='white'):
    image_size = 224 * 3
    tile_size = 16 * 3
    if status:
        for i in range(int(image_size / tile_size)):  # 画横线
            canvas.create_line(0, i * tile_size, image_size, i * tile_size, fill=color, width=1)
        for i in range(int(image_size / tile_size)):
            canvas.create_line(i * tile_size, 0, i * tile_size, image_size, fill=color, width=1)


def load_img(index, path):
    global img
    global canvas
    global _path
    _path = path

    global imgs  # 进度条获取图像总数量
    global canvas_text  # 为了清除现有的进度条文字
    global canvas_path

    # canvas = tk.Canvas(root, width=770, height=800, bg='pink')
    canvas = tk.Canvas(root, width=224*3, height=800, bg='pink')
    # canvas.pack()
    canvas.place(x=0,y=0)
    # img = tk.PhotoImage(file=path)
    _img = Image.open(path)
    # _img = _img.resize((768, 768), Image.ANTIALIAS)
    _img = _img.resize((672, 672), Image.ANTIALIAS)  # 标注224×224的图像
    img = ImageTk.PhotoImage(_img)
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    create_grid(grid_or_not)  # 【add】【画grid0221】

    out_rec = canvas.create_rectangle(0, 256 * 3 + 5, 256 * 2, 256 * 3 + 15, outline="blue", width=1)
    fill_rec = canvas.create_rectangle(0, 256 * 3 + 5, 0, 256 * 3 + 15, outline="", width=0, fill="blue")
    all_schedule = len(imgs)
    now_schedule = len(pd.read_csv(csv_path, encoding="utf-8"))
    # now_schedule=0      # 设计获取csv图像个数的函数-reload也写进度条设计程序-加入16/17
    canvas.coords(fill_rec, (0, 256 * 3 + 5, 1 + (now_schedule / all_schedule) * 256 * 2, 256 * 3 + 15))
    # 加入进度条文字
    canvas_path = canvas.create_text(350, 730, text=path.split('\\')[-1],
                                     font=("Purisa", 25))  # canvas.create_text(256*2+100,777,text='进度条')
    canvas_text = canvas.create_text(256 * 2 + 100, 777, text=str(now_schedule) + '/' + str(all_schedule),
                                     font=("Purisa", 15))
    root.update()

    df = pd.read_csv(csv_path, encoding="utf-8")
    try:
        content = df[df.img_path == _path.split('\\')[-1]]['labels_info'].values[0]
    except (IndexError,):
        return
    label_list = eval(content)
    tile_list.load_from_list(label_list)

    show_listbox(ord_status)


def re_load_img(index, path):
    global img
    global canvas
    global _path
    _path = path
    global canvas_text
    global canvas_path
    _img = Image.open(path)
    _img = _img.resize((672, 672), Image.ANTIALIAS)  # 标注224×224的图像
    img = ImageTk.PhotoImage(_img)
    canvas.create_image(0, 0, anchor=tk.NW, image=img)
    create_grid(grid_or_not)  # 【add】【画grid0221】

    # 进度条设计——加入进度条文字
    # out_rec = canvas.create_rectangle(0, 256*3+5, 256*3, 256*3+15, outline="blue", width=1)
    out_rec = canvas.create_rectangle(0, 256 * 3 + 5, 256 * 2, 256 * 3 + 15, outline="blue", width=1)
    fill_rec = canvas.create_rectangle(0, 256 * 3 + 5, 0, 256 * 3 + 15, outline="", width=0, fill="blue")
    all_schedule = len(imgs)
    now_schedule = len(pd.read_csv(csv_path, encoding="utf-8"))
    # now_schedule=0      # 设计获取csv图像个数的函数-reload也写进度条设计程序-加入16/17
    canvas.coords(fill_rec, (0, 256 * 3 + 5, 1 + (now_schedule / all_schedule) * 256 * 2, 256 * 3 + 15))
    # 加入进度条文字
    # canvas.create_text(256*2+100,777,text='进度条')
    # canvas.create_text(100 * 2 + 0, 777, text='进度条', font=("Purisa", 25))
    canvas.delete(canvas_path)
    canvas_path = canvas.create_text(350, 730, text=path.split('\\')[-1], font=("Purisa", 25))
    # canvas.create_text(100, 700, text='进度条', font=("Purisa", 15))

    canvas.delete(canvas_text)
    canvas_text = canvas.create_text(256 * 2 + 100, 777, text=str(now_schedule) + '/' + str(all_schedule),
                                     font=("Purisa", 15))
    root.update()
    show_listbox(ord_status)


def change_img(event):
    global img_num
    global _path
    delta = {'a': -1, 'd': 1}[event.char]
    img_num = img_num + delta
    if img_num < 0:
        img_num = img_num - delta
        tk.messagebox.showerror('', '这已经是第一张图片了')
    elif img_num > len(imgs) - 1:
        img_num = img_num - delta
        tk.messagebox.showerror('', '这已经是最后一张图片了')
    else:
        tile_list.clear()
        re_load_img(img_num, imgs[img_num])
        df = pd.read_csv(csv_path, encoding="utf-8")
        try:
            content_now_str = df[df.img_path == _path.split('\\')[-1]]['labels_info'].values[0]
            content_now = eval(content_now_str)
        except (IndexError,):
            return
        tile_list.load_from_list(content_now)


# root.bind('<Left>',key_last_img)
root.bind('a', change_img)  # 【revise_0208_改为a键翻页】
# root.bind('<Right>',key_next_img)
root.bind('d', change_img)  # 【revise_0208_改为d键翻页】

global img_num
# img_num=5
img_num = 0
# global NUM
# NUM=3
load_img(img_num, imgs[img_num])


# TODO: 按照新的Tile的数据格式来定义
def generate_box_selfpoints(box_num, loca_x, loca_y, color):  # 【0122】
    # loca_x_leftup=(int((loca_x-8*3)/48))*48
    # loca_y_leftup=(int((loca_y-8*3)/48))*48
    # 直接将鼠标点击点，视为方框左上角的点（不再是中心点）；寻找该点最近的16倍数的点
    loca_x_leftup = (int((loca_x) / 48)) * 48
    loca_y_leftup = (int((loca_y) / 48)) * 48

    create_rectangle_color(box_num, loca_x_leftup, loca_y_leftup, color=color)  # 【0122】


def mouse_right_double_selfpoints(x_from_event, y_from_event, event_num):  # 【0122】整个函数新增
    # 设置224×224的画框标注范围              # 【20220203——224×224】
    # if event.x<=672 and event.y<=672:       # 【20220203——224×224】

    if x_from_event > 672 or y_from_event > 672:  # 【20220203——224×224】
        return

    label = {1: 1, 3: 0}[event_num]
    # TODO: 根据Tile对象的参数来确定倍率
    coord_x = (int(x_from_event / 48)) * 16
    coord_y = (int(y_from_event / 48)) * 16
    coord = (coord_x, coord_y)
    content_append = ((coord_x, coord_y), label)

    df = pd.read_csv(csv_path, encoding="utf-8")
    try:
        content_now_str = df[df.img_path == _path.split('\\')[-1]]['labels_info'].values[0]
        content_now = eval(content_now_str)
    except (IndexError,):
        tile = Tile(0, coord, label)
        tile.create_rectangle_color()
        tile_list.append(tile)
        with open(csv_path, "a") as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')
            writer.writerow([_path.split('\\')[-1],
                             [content_append]])  # 5.【0122】
        return

    # 获取要添加的字符之后，先判断已有点的个数，小于10(NUM)-则添加；大于10-则前向添加
    if len(tile_list) < NUM:
        content_now.append(content_append)
        tile = Tile(len(tile_list), coord, label)
        tile_list.append(tile)
    else:
        tk.messagebox.showerror('', '提醒：已超过指定个数\n覆盖第一个')
        q = len(tile_list) % NUM
        content_now[q] = content_append
        tile = Tile(q, coord, label)
        tile_list.list[q].del_box()
        tile_list.list[q] = tile

    tile.create_rectangle_color()
    df.loc[df.img_path == _path.split('\\')[-1], 'labels_info'] = str(content_now)
    df.to_csv(csv_path, encoding='utf-8-sig', index=False)

    print(content_now)


# 进度条
# 画进度条位置-确定进度条填充颜色-进度条更新函数（读取文件夹所有图像数目，➗csv文件已有图像数）
def according_key_label(m):
    global _path
    tile_list.list[m].change_box_label()
    df = pd.read_csv(csv_path, encoding="utf-8")
    try:
        content_now_str = df[df.img_path == _path.split('\\')[-1]]['labels_info'].values[0]
        content_now = eval(content_now_str)
    except (IndexError,):
        raise IndexError("No according csv found!")
    content_now[m] = (content_now[m][0], 1 - content_now[m][1])
    df.loc[df.img_path == _path.split('\\')[-1], 'labels_info'] = str(content_now)
    df.to_csv(csv_path, encoding='utf-8-sig', index=False)


def mouse_center(x_from_event, y_from_event):
    i_mouse = tile_list.if_point_in_any_box(x_from_event, y_from_event)
    if i_mouse == -1:
        return
    according_key_label(i_mouse)


# TODO: 按照新的Tile的数据格式来定义（待验收）
def key_ctrl_z(event):
    print('revoke')
    # 在规定次数NUM之内使用（如在点击10次之内使用）

    global _path
    # 找到方框位置，去除方框，pop标签
    # 判断是该行标签否为空，空则返回
    if tile_list.list==None:
        return

    # tile_list.list[-1].change_box_label(removal=True)
    tile_list.remove_box(tile_list.idx_to_del)

    df = pd.read_csv(csv_path, encoding="utf-8")
    try:
        content_now_str = df[df.img_path == _path.split('\\')[-1]]['labels_info'].values[0]
        content_now = eval(content_now_str)
    except (IndexError,):
        raise IndexError("No according csv found!")
    content_now.pop()
    df.loc[df.img_path == _path.split('\\')[-1], 'labels_info'] = str(content_now)
    df.to_csv(csv_path, encoding='utf-8-sig', index=False)
    print('ok')

root.bind("<Control-z>", key_ctrl_z)


# 这个rewrite_according_key_label，含鼠标中键位置靠左为阳_靠右为阴的功能
def rewrite_according_key_label(loca_x, loca_y, m):
    # 鼠标点击的点是随意的(方框的中心点)，可能是小数；但放缩小后，需要是整数坐标，因此用下面的一行语句处理；
    # 其中的8是，16×16边长的一半，也就是中心点坐标到左上角的差值
    # global tile_list
    loca_x_leftup = (int(loca_x / 48)) * 48
    loca_y_leftup = (int(loca_y / 48)) * 48
    # 记录鼠标点击位置的横坐标中线，靠左则为红色，靠右则为绿色
    delta_x = abs(loca_x - loca_x_leftup)
    delta_csv = int(delta_x <= int(48 / 2))

    global _path
    df = pd.read_csv(csv_path, encoding="utf-8")
    try:
        content_now_str = df[df.img_path == _path.split('\\')[-1]]['labels_info'].values[0]
        content_now = eval(content_now_str)
    except (IndexError,):
        raise IndexError("No according csv found!")
    new_coord = (loca_x_leftup // 3, loca_y_leftup // 3)
    new_item = (new_coord, delta_csv)
    content_now[m] = new_item
    df.loc[df.img_path == _path.split('\\')[-1], 'labels_info'] = str(content_now)
    df.to_csv(csv_path, encoding='utf-8-sig', index=False)
    tile = Tile(m, new_coord, delta_csv)
    tile.create_rectangle_color()
    tile_list.insert(m, tile)


def mouse_left_double_selfpoints_revise(event):
    i_mouse = tile_list.if_point_in_any_box(event.x, event.y)
    if i_mouse == -1:
        if tile_list.idx_to_del == -1:
            return
        tile_list.remove_box(tile_list.idx_to_del)
        rewrite_according_key_label(event.x, event.y, tile_list.idx_to_del)
        tile_list.idx_to_del = -1
        return

    if tile_list.idx_to_del == -1:
        tile_list.list[i_mouse].change_box_label(removal=True)
        tile_list.idx_to_del = i_mouse
    else:
        for _ in range(2):
            tile_list.list[tile_list.idx_to_del].change_box_label()
        tile_list.idx_to_del = -1

root.bind("<Button-2>", mouse_left_double_selfpoints_revise)


# 按住up，触发随机生成10个红框，同时csv标注全阳性
# 按住down，触发随机生成10个绿框，同时csv标注全阴性
def random_labeling(event):
    global _path
    df = pd.read_csv(csv_path, encoding="utf-8")
    if (df.img_path == _path.split('\\')[-1]).any():
        return
    # global tile_list
    annotations = tile_list.gen_random_tiles(event.char)

    with open(csv_path, "a") as csvfile:
        writer = csv.writer(csvfile, lineterminator='\n')
        writer.writerow(
            [_path.split('\\')[-1], str(annotations)])

root.bind('w', random_labeling)
root.bind('s', random_labeling)


# 将mouse_center和mouse_right_double_selfpoints合并，形成不带(event)的普通函数
# 新建<Button-1>对应的鼠标响应函数，如果点的点在标注框内，则启动mouse_center函数；
# 如果在标注框外，则启动mouse_right_double_selfpoints函数
def mouse_center_or_mouse_right_double_selfpoints(event):
    i_mouse = tile_list.if_point_in_any_box(event.x, event.y)
    if i_mouse == -1:
        mouse_right_double_selfpoints(event.x, event.y, event.num)
    else:
        according_key_label(i_mouse)

# root.bind('<Button-1>', mouse_center_or_mouse_right_double_selfpoints)
# root.bind('<Button-3>', mouse_center_or_mouse_right_double_selfpoints)
canvas.bind('<Button-1>', mouse_center_or_mouse_right_double_selfpoints)
canvas.bind('<Button-3>', mouse_center_or_mouse_right_double_selfpoints)

root.mainloop()
