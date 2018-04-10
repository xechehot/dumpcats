# coding=utf-8
import sys
import time
import telepot
import telepot.namedtuple
from telepot.loop import MessageLoop
from tempfile import TemporaryFile
import os

from fastai.imports import *
from fastai.transforms import *
from fastai.conv_learner import *
from fastai.model import *
from fastai.dataset import *
from fastai.sgdr import *
from fastai.plots import *

import cv2

import io
import numpy as np

def open_image(file_object):
    # flags = cv2.IMREAD_UNCHANGED + cv2.IMREAD_ANYDEPTH + cv2.IMREAD_ANYCOLO
    flags = 5
    file_object.seek(0)
    img_array = np.asarray(bytearray(file_object.read()), dtype=np.uint8)
    im = cv2.imdecode(img_array, flags).astype(np.float32) / 255
    return cv2.cvtColor(im, cv2.COLOR_BGR2RGB)

class CatDogPredictor():
    def __init__(self, model_path):
        self.model = torch.load(model_path, map_location=lambda storage, loc: storage)
        self.model.train(False)
        _, val_tfms = tfms_from_model(resnet34, 224)
        self.tfms = val_tfms

    def transform_image(self, source_img):
        return self.tfms(source_img)

    def predict(self, file_object):
        source_img = open_image(file_object)
        image = self.transform_image(source_img)        
        x = Variable(torch.from_numpy(np.array([image])), requires_grad=False)
        output = self.model(x.cpu())
        return np.exp(output.cpu().data.numpy())[0]