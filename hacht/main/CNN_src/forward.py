import sys,os,datetime
import numpy as np
import cv2
import torch
import torch.nn as nn
import torchvision
import models
import argparse

from torch.autograd import Variable
from torch.optim import Adam
from models import get_model
from BreakHisDataset import *
from Performance import Performance


PATH = "C:/Users/Martin/Desktop/Red_CNN/"

def forward_single_img(img_path):
        num_classes = 8
        dir_weights = "/home/Martinvc96/hacht/hacht/main/CNN_src/weights_50.pt"
        #dir_weights = "C:/Users/gmc_2/source/repos/HACHT/hacht/hacht/main/CNN_src/weights_50.pt"
        architecture = "squeezenet"
        (model, img_size) = get_model(num_classes, dir_weights, architecture)
        model = model
        test_dataset = BreakHis2(img_path, img_size, training=True, preprocessing="RGB")
        test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=1, shuffle=False)

        for batch_id, (data) in enumerate(test_loader):
                data = data	
                output = model(data)
                _, predict = torch.max(output, dim=1)
                result = predict.cpu().tolist()
                return result[0]
                	

def forward_single_img2(img_path):
        num_classes = 8
        dir_weights = "weights_50.pt"
        architecture = "squeezenet"
        (model, img_size) = get_model(num_classes, dir_weights, architecture)
        model = model
        test_dataset = BreakHis3(img_path, img_size, training=False, preprocessing="RGB")
        test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=1, shuffle=False)

        for batch_id, (data, patient_id) in enumerate(test_loader):
                data, patient_id = data, patient_id	
                output = model(data)
                _, predict = torch.max(output, dim=1)
                print("Result: ", predict.cpu().tolist())
                print(" --------------------------------- \n ")

def forward_n_img(img_folder_path):
        return 1

def forward_n_img_with_labels(img_folder_path, csv_file_path):
        num_classes = 8
        dir_weights = PATH + "weights.pt"
        architecture = "squeezenet"

        #"C:/Users/Martin/Desktop/Red_CNN/breakhis_subset"
        #"C:/Users/Martin/Desktop/Red_CNN/test_100_multi_kfold_0.csv"
        
        (model, img_size) = get_model(num_classes, dir_weights, architecture)
        model = model
        test_dataset = BreakHis(img_folder_path, csv_file_path, img_size, training=False, preprocessing="RGB")
        test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=1, shuffle=False)

        for batch_id, (data, target, patient_id) in enumerate(test_loader):
                data, target = data, target
                output = model(data)
                _, predict = torch.max(output, dim=1)
                print("Id paciente: ", patient_id.tolist())
                print("Target: ",target.cpu().tolist())
                print("Result: ", predict.cpu().tolist())
                print("\n --------------------------------- \n ")

