from __future__ import print_function, absolute_import
import torch.utils.data as data
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

class _OWN(data.Dataset):
    def __init__(self, config, is_train=True):

        self.root = config.DATASET.ROOT
        self.is_train = is_train
        self.inp_h = config.MODEL.IMAGE_SIZE.H
        self.inp_w = config.MODEL.IMAGE_SIZE.W

        with open(config.DATASET.FORMULAS_DIR) as file:
            self.formulas = file.read().splitlines()

        self.dataset_name = config.DATASET.DATASET

        self.mean = np.array(config.DATASET.MEAN, dtype=np.float32)
        self.std = np.array(config.DATASET.STD, dtype=np.float32)

        txt_file = config.DATASET.JSON_FILE['train'] if is_train else config.DATASET.JSON_FILE['val']

        # convert name:indices to name:string
        with open(txt_file, 'r', encoding='utf-8') as file:
            # self.labels = [{c.split(' ')[0]: c.split(' ')[-1][:-1]} for c in file.readlines()]
            self.labels = [{c.split(' ')[0]: self.get_formula(c.split(' ')[1]).split(' ')} for c in file.readlines()]

        print("load {} images!".format(self.__len__()))

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):

        img_name = list(self.labels[idx].keys())[0]
        img = cv2.imread(os.path.join(self.root, img_name))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # plt.imshow(img)
        # plt.show()

        img_h, img_w = img.shape

        img = cv2.resize(img, (0,0), fx=self.inp_w / img_w, fy=self.inp_h / img_h, interpolation=cv2.INTER_CUBIC)
        img = np.reshape(img, (self.inp_h, self.inp_w, 1))

        # plt.imshow(img)
        # plt.show()

        img = img.astype(np.float32)
        img = (img/255. - self.mean) / self.std
        img = img.transpose([2, 0, 1])

        return img, idx


    def get_formula(self, label):
        # function which returns the formula
        return self.formulas[int(label)]





