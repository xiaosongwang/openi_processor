import os
import os.path as osp
import xml.etree.ElementTree as ET
import csv

report_dir = '/home/xiaosongw/datasets/openi/report_xml'
# image_dir = '/home/xiaosongw/datasets/openi/NLMCXR_png'
output_dir = '/home/xiaosongw/datasets/openi'

xml_file_list = os.listdir(report_dir)

report_text = ''
mesh_words = ''
for i, xml_file in enumerate(xml_file_list):
    print i, xml_file
    tree_tmp = ET.parse(osp.join(report_dir, xml_file))
    if len(tree_tmp.getroot()) <= 18: continue
    report_text = report_text + 'image_id : ' \
                  + (tree_tmp.getroot()[18].attrib['id'][:-5] if len(tree_tmp.getroot()) >= 19 else ' ') + ' & ' \
                  + tree_tmp.getroot()[16][0][2][0].attrib['Label'] + ' : ' \
                  + (tree_tmp.getroot()[16][0][2][0].text if tree_tmp.getroot()[16][0][2][0].text is not None else ' ') + ' & ' \
                  + tree_tmp.getroot()[16][0][2][1].attrib['Label'] + ' : ' \
                  + (tree_tmp.getroot()[16][0][2][1].text if tree_tmp.getroot()[16][0][2][1].text is not None else ' ') + ' & ' \
                  + tree_tmp.getroot()[16][0][2][2].attrib['Label'] + ' : ' \
                  + (tree_tmp.getroot()[16][0][2][2].text if tree_tmp.getroot()[16][0][2][2].text is not None else ' ') + ' & ' \
                  + tree_tmp.getroot()[16][0][2][3].attrib['Label'] + ' : ' \
                  + (tree_tmp.getroot()[16][0][2][3].text if tree_tmp.getroot()[16][0][2][3].text is not None else ' ') \

    report_text = report_text + ' & ' + tree_tmp.getroot()[17].tag + ' : '
    for child_i in range(len(tree_tmp.getroot()[17])):
        if tree_tmp.getroot()[17][child_i].tag == 'major':
            if child_i > 0:
                report_text = report_text + ' // '
            report_text = report_text + tree_tmp.getroot()[17][child_i].text


    if len(tree_tmp.getroot()) >= 19:
        report_text = report_text + ' & ' + tree_tmp.getroot()[18].tag + ' : ' \
                      + tree_tmp.getroot()[18].attrib['id']

    if len(tree_tmp.getroot()) >= 20:
        report_text = report_text + ' & ' + tree_tmp.getroot()[19].tag + ' : ' \
                      + tree_tmp.getroot()[19].attrib['id']

    report_text = report_text + '\n'

    for child_i in range(len(tree_tmp.getroot()[17])):
        if tree_tmp.getroot()[17][child_i].tag == 'major':
            mesh_words = mesh_words + tree_tmp.getroot()[17][child_i].text + '/'

file = open(osp.join(output_dir, 'all_report.csv'), 'w')
file.write(report_text)
file.close()

mesh_words = mesh_words.lower().replace(', ', '-').replace(' ', '-').replace('/',' ')
mesh_words = " ".join(mesh_words.split(' '))
mesh_words_list = mesh_words.split(' ')

unique_mesh_words = set(mesh_words_list)

# count the frequency of each word
import collections
mesh_words_counter = collections.Counter(mesh_words_list)
print mesh_words_counter

dict = mesh_words_counter
w = csv.writer(open(osp.join(output_dir, 'mesh_word_freq.csv'), "w"))
for key, val in dict.items():
    w.writerow([key, val])



# for i, caption in enumerate(caption_data['caption']):
#     caption = caption.replace('.', '').replace(',', '').replace("'", "").replace('"', '')
#     caption = caption.replace('&', 'and').replace('(', '').replace(")", "").replace('-', ' ')
#     caption = " ".join(caption.split())  # replace multiple spaces
#
#     caption_data.set_value(i, 'caption', caption.lower())
