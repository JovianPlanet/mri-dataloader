template = '''import os
import nibabel as nib
import numpy as np
import pandas as pd
import cv2
import torch
from torchvision import transforms
from torch.utils.data import Dataset

class MRI_DS(Dataset):

    def __init__(self):

        self.path = './data/train'
        self.mri_name = 'T1.nii'
        self.labels_name = None
        self.transform = transforms.Compose([transforms.Grayscale(), transforms.ToTensor()])
        #self.target_transform = target_transform
        self.dims = False
        self.remove_bgnd = False
        self.crop = False

        self.subjects = next(os.walk(self.path))[1]

        self.L = []

        for i, subject in enumerate(self.subjects[:]):
            mri_path = os.path.join(self.path, subject, self.mri_name)
            img = nib.load(mri_path).get_fdata()
            if self.labels_name != None:
                label_path = os.path.join(self.path, subject, self.labels_name)
                lbl = nib.load(label_path).get_fdata()

            if self.remove_bgnd:
                for slice_ in range(img.shape[-1]):
                    if np.any(lbl[:, :, slice_]):
                        self.L.append([subject, slice_, mri_path, label_path])

            elif self.crop:
                for slice_ in range(self.crop[0], self.crop[1]):
                    if self.labels_name != None:
                        self.L.append([subject, slice_, mri_path, label_path])
                    else:
                        self.L.append([subject, slice_, mri_path])

            else:
                for slice_ in range(img.shape[-1]):
                    if self.labels_name != None:
                        self.L.append([subject, slice_, mri_path, label_path])
                    else:
                        self.L.append([subject, slice_, mri_path])

        if self.labels_name != None:
            self.df = pd.DataFrame(self.L, columns=['Subject', 'Slice', 'Path MRI', 'Path Label'])
        else:
            self.df = pd.DataFrame(self.L, columns=['Subject', 'Slice', 'Path MRI'])

        self.df = self.df.assign(id=self.df.index.values)

    def __len__(self):

        return self.df.shape[0]

    def __getitem__(self, index):

        load_path  = self.df.at[index, 'Path MRI']
        load_slice = self.df.at[index, 'Slice']

        mri = np.int16(nib.load(load_path).get_fdata())
        if self.labels_name != None:
            label = np.int16(nib.load(self.df.at[index, 'Path Label']).get_fdata())

        if self.dims:
            mri_ = cv2.resize(mri[:, :, load_slice], self.dims, interpolation=cv2.INTER_CUBIC)
            if self.labels_name != None:
                lbl  = cv2.resize(label[:, :, load_slice], self.dims, interpolation=cv2.INTER_CUBIC)
                return mri_, lbl
            return mri_

        # if self.transform:
        #     image = self.transform(image)
        # if self.target_transform:
        #     label = self.target_transform(label)

        if self.labels_name != None:
            return mri[:, :, load_slice], label[:, :, load_slice]
        return mri[:, :, load_slice]
'''