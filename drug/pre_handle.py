# !/usr/bin/python
# -*- coding:utf-8 -*-


import sys
import getopt
import os
import codecs

input_dir = ""  # /Users/lijianwei/Downloads/competition/train
output_dir = ""
ANN_PATH_SUFFIX = ".ann"
OUTPUT_PATH_SUFFIX = ".txt"

try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "ifile=", "ofile="])
except getopt.GetoptError:
    print("python pre_handle.py -i <inputdir> -o <outputdir>")
    sys.exit(1)
for opt, arg in opts:
    if opt == "-h":
        print("python pre_handle.py -i <inputdir> -o <outputdir>")
        sys.exit(2)
    elif opt in ("-i", "--inputfile"):
        input_dir = arg
    elif opt in ("-o", "--outputfile"):
        output_dir = arg

if input_dir == "" or output_dir == "":
    print("python pre_handle.py -i <inputdir> -o <outputdir>")
    sys.exit(3)

print("inputdir is " + input_dir)
print("outputdir is " + output_dir)
# 输出文件夹不存在则创建
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print("outputdir has been created")

# 遍历输入文件夹
input_dir_files = os.listdir(input_dir)

for input_dir_file_name in input_dir_files:

    input_dir_file_path = os.path.join(input_dir, input_dir_file_name)
    input_dir_file_name_arr = os.path.splitext(input_dir_file_name)
    input_dir_file_name_prefix = input_dir_file_name_arr[0]
    input_dir_file_name_suffix = input_dir_file_name_arr[1]

    if input_dir_file_name_suffix == ".txt":
        # ann文件路径
        input_dir_ann_file_path = os.path.join(input_dir, (input_dir_file_name_prefix + ANN_PATH_SUFFIX))
        # 输出文件路径
        output_dir_result_file_path = os.path.join(output_dir, (input_dir_file_name_prefix + OUTPUT_PATH_SUFFIX))

        ann_file = codecs.open(input_dir_ann_file_path, "r", encoding="utf-8")
        txt_file = codecs.open(input_dir_file_path, "r", encoding="utf-8")
        result_file = codecs.open(output_dir_result_file_path, "w+", encoding="utf-8")

        # txt文本
        file_content = txt_file.readline()
        file_content_dict = []
        # 将txt文件每个字写入到文件中
        for per_text in file_content:
            file_content_dict.append((per_text, "0"))

        ann_per_line = ann_file.readline()
        while ann_per_line != "":
            ann_per_line_arr = ann_per_line.split("\t")
            biaozhu_arr = ann_per_line_arr[1].split(" ")
            class_name = biaozhu_arr[0]
            start_index = int(biaozhu_arr[1])
            end_index = int(biaozhu_arr[2])

            result_index = start_index
            # 将标注放入新的文件中
            while result_index < end_index:
                if end_index - start_index == 1:
                    file_content_dict[result_index] = (file_content_dict[result_index][0], "S-" + class_name)
                    result_index += 1
                    continue
                if result_index == start_index:
                    file_content_dict[result_index] = (file_content_dict[result_index][0], "B-" + class_name)
                elif result_index == end_index - 1:
                    file_content_dict[result_index] = (file_content_dict[result_index][0], "E-" + class_name)
                elif result_index > start_index and result_index < end_index - 1:
                    file_content_dict[result_index] = (file_content_dict[result_index][0], "M-" + class_name)
                result_index += 1
            ann_per_line = ann_file.readline()
        for per_dict in file_content_dict:
            if per_dict[0] == " ":
                continue
            result_file.write(per_dict[0] + " " + per_dict[1] + "\n")
