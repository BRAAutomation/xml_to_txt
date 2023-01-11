from xml.etree import ElementTree
import glob
import os

SAVE_DIR = "flowchart_train/flowchart_txt/"
READ_DIR = "flowchart_train/flowchart_xml/*"

#make dict
cl = {}
with open("./flowchart_train/data/classes.txt") as f:
    for line in f:
        (k, v) = line.split()
        cl[v] = int(k)

for xml in glob.glob(READ_DIR):

    #read xml
    content = ""
    tree = ElementTree.parse(xml)
    root = tree.getroot()

    H = int( root.find('height').text )
    W = int( root.find('width').text )
    objects = root.iterfind('object')
    for object in objects:
        name = object.find("name").text
        xmin = object.find("bndbox/xmin").text
        xmax = object.find("bndbox/xmax").text
        ymin = object.find("bndbox/ymin").text
        ymax = object.find("bndbox/ymax").text

        #transform
        class_num = cl[name]
        xmin = int(xmin); xmax = int(xmax); ymin = int(ymin); ymax = int(ymax)
        x_center = (xmin + xmax)/2
        y_center = (ymin + ymax)/2
        width = xmax - xmin
        height = ymax - ymin

        #Standerlize
        x_center /= W ; width /= W
        y_center /= H ; height /= H

        content += '{} {:.6f} {:.6f} {:.6f} {:.6f}\n'.format(class_num, x_center, y_center, width, height)

    #save to .text
    FILE_NAME = os.path.splitext(os.path.basename(xml))[0]
    with open(SAVE_DIR + FILE_NAME + ".txt", mode='w') as f:
        f.write(content)
