import sys,os,datetime
import numpy as np
import cv2
import torch
import torch.nn as nn
import torchvision
import argparse

from django.conf import settings
from .BreakHisDataset import *
from .SqueezeNet import get_model


def forward_single_img(img_path):
    num_classes = 8

    dir_weights = os.path.join(settings.BASE_DIR, "main", "CNN_src", "weights_50.pt")
    img_size = 256
    model = get_model(num_classes, dir_weights)

    test_dataset = BreakHisWork(img_path, img_size)
    test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=1, shuffle=False)

    for batch_id, (data) in enumerate(test_loader):
        data = data
        output = model(data)
        _, predict = torch.max(output, dim=1)
        result = predict.cpu().tolist()
        return result[0], output
