import pandas as pd
import os
import os.path
import numpy as np

data_folder = '/home/xiaosongw/datasets/openi'

##################### generate the image label list for Chexpert and Negbio #################3
meta_data_file = os.path.join(data_folder, 'all_report.csv')
# vocab_fname = '/home/xiaosongw/DTC/mimic_vocab_f3_6301.pkl'
# with open(vocab_fname, 'rb') as f:
#     vocab = pickle.load(f)

dataset_name = 'mimic' # 'mimic'

cxr14_disease_list = ['atelectasis', 'cardiomegaly', 'effusion', 'infiltration', 'mass', 'nodule',
                'pneumonia', 'pneumothorax', 'consolidation', 'edema', 'emphysema',
                'fibrosis', 'pleural-thickening', 'hernia', 'no-finding']
cxr14_disease_word_list = [['atelect'], ['cardiomegaly', 'shadow-enlarged'], ['effusion'], ['infiltrat'], ['mass'],
                           ['nodule'], ['pneumonia'], ['pneumothorax'], ['consolidation'], ['edema'], ['emphysema'],
                           ['fibrosis'], ['thickening-pleura'], ['hernia'], ['no-finding']]
mimic_disease_list = ['atelectasis', 'cardiomegaly', 'consolidation', 'edema', 'enlarged-cardiomediastinum',
                      'fracture', 'lung-lesion', 'lung-opacity', 'no-finding', 'pleural-effusion', 'pleural-other',
                      'pneumonia', 'pneumothorax', 'support-devices']
mimic_disease_word_list = [['atelect'], ['cardiomegaly'], ['consolidation', 'pneumonia'], ['pulmonaryedema'],
                           ['shadow-enlarged', 'cardiomegaly'], ['fracture'], ['mass', 'nodule'],
                           ['opacity-lung', 'density-lung', 'pulmonaryedema', 'consolidation', 'pneumonia',
                            'mass', 'nodule', 'atelect'],
                           ['no-finding'], ['effusion'], ['pleural-other', 'thickening-pleura', 'cicatrix-pleura'],
                           ['pneumonia'], ['pneumothorax'], ['device', 'catheters']]
plco_disease_list = ['nodule', 'mass', 'distortion_pulmonary_architecture', 'pleural_based_mass', 'granuloma',
                     'fluid_in_pleural_space', 'right_hilar_abnormality', 'left_hilar_abnormality',
                     'major_atelectasis', 'infiltrate', 'scarring', 'pleural_fibrosis', 'bone_soft_tissue_lesion',
                     'cardiac_abnormality', 'copd']

front_image_list = os.listdir(os.path.join(data_folder, 'front'))

# build data list for mimic style
meta_data_df = pd.read_csv(meta_data_file, delimiter='&')

data_list = []
for entry in meta_data_df.values.tolist():
    data_list_entry = []
    image_file_name = entry[0][13:-2]
    try:
        image_fname_full = [fn for fn in front_image_list if image_file_name in fn][0]
    except:
        print(image_file_name)
        continue
    data_list_entry.append(image_fname_full)
    # processing report
    report = entry[3][2:-1] + entry[4][2:-1]
    data_list_entry.append(report.replace('::', ':').replace('..', '.').replace('"', ' '))
    # processing labels
    mesh_words = entry[5][10:-2].lower().replace(' ', '').replace(',', '-').replace('//', ' // ').replace('/', '-')
    data_list_entry.append(entry[5][10:-2])
    nofinding_sign = 0
    if dataset_name == 'mimic':
        disease_list_org = mimic_disease_list
        disease_word_list_org = mimic_disease_word_list
    elif dataset_name == 'cxr14':
        disease_list_org = cxr14_disease_list
        disease_word_list_org = cxr14_disease_word_list
    for disease_idx, disease in enumerate(disease_list_org):
    # for disease_idx, disease in enumerate(cxr14_disease_list):
        disease_sign = 0
        # for disease_word in cxr14_disease_word_list[disease_idx]:
        for disease_word in disease_word_list_org[disease_idx]:
            if mesh_words.find(disease_word.lower()) >= 0:
                disease_sign = 1
                nofinding_sign = 1
        if disease_sign:
            data_list_entry.append(1)
        else:
            data_list_entry.append(0)

    # set the "no finding" label
    if nofinding_sign == 0:
        if dataset_name == 'mimic':
            data_list_entry[2 + 9] = 1
        elif dataset_name == 'cxr14':
            data_list_entry[2 + 15] = 1

    data_list.append(data_list_entry)

if dataset_name == 'mimic':
    column_names = ['file_name', 'report', 'mesh_word'] + mimic_disease_list
elif dataset_name == 'cxr14':
    column_names = ['file_name', 'report', 'mesh_word'] + cxr14_disease_list
annotation_df = pd.DataFrame(data_list, columns=column_names)
annotation_df.to_csv(os.path.join(data_folder, 'front_label_list_'+dataset_name+'.csv'), doublequote=True, index=False, sep='&')
# annotation_df.to_csv(os.path.join(data_folder, 'front_label_list_cxr14.csv'), doublequote=True, index=False)