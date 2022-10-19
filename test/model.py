from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import torchvision
from torchvision import transforms

import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data as data

import torchvision.datasets as datasets

from sklearn import decomposition
from sklearn import manifold
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay

from tqdm.notebook import tqdm, trange
import matplotlib.pyplot as plt

import copy
import random
import time

from sklearn.metrics import precision_score, recall_score, f1_score

class CNN(nn.Module):
    def __init__(self, out_dim):
        super().__init__()

        #Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0)

        self.features = nn.Sequential(
            nn.Conv2d(1, 6, 5),
            nn.MaxPool2d(2),
            nn.ReLU(inplace=True),
            nn.Conv2d(6, 16, 5),
            nn.MaxPool2d(2),
            nn.ReLU(inplace=True),
         )

        self.classifier = nn.Sequential(
            nn.Linear(16*4*4, 120),
            nn.ReLU(inplace=True),
            nn.Linear(120, 84),
            nn.ReLU(inplace=True),
            nn.Linear(84, out_dim)
         )

    def forward(self, x):
        x = self.features(x)
        h = x.view(x.shape[0], -1)
        x = self.classifier(h)
        return x, h


class CNN_LSTM(nn.Module):
    def __init__(self, out_dim):
        super().__init__()

        #Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0)

        self.features = nn.Sequential(
            nn.Conv2d(1, 6, 5),
            nn.MaxPool2d(2),
            nn.ReLU(inplace=True),
            nn.Conv2d(6, 16, 5),
            nn.MaxPool2d(2),
            nn.ReLU(inplace=True),
         )
        
        self.lstm = nn.LSTM(16*4*4, 128, 2, batch_first=True)
        self.fc = nn.Linear(128, out_dim)
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.shape[0], -1, 16*4*4)
        h0 = torch.zeros(2, x.size(0), 128).to('cuda') 
        c0 = torch.zeros(2, x.size(0), 128).to('cuda')
        out, cell = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        
        return out, cell    

class LSTM(nn.Module):
    def __init__(self, out_dim):
        super().__init__()
        
        self.hidden_size = 128
        self.num_layers = 2
        self.input_size = 28
        self.batch_size = 36
   
        self.lstm = nn.LSTM(self.input_size, self.hidden_size, self.num_layers, batch_first=True)
        self.fc = nn.Linear(self.hidden_size, out_dim)
        
        
    def forward(self, x):
        
        x = x.reshape(-1, 28,28)
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to('cuda') 
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to('cuda')
        out, cell = self.lstm(x, (h0, c0))
        
        out = self.fc(out[:, -1, :])
        return out, cell


class BiLSTM(nn.Module):
    def __init__(self, out_dim):
        super().__init__()
        
        self.hidden_size = 128
        self.num_layers = 2
        self.input_size = 28
        self.batch_size = 36
   
        self.lstm = nn.LSTM(self.input_size, self.hidden_size, self.num_layers, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(self.hidden_size*2, out_dim)
        
        
    def forward(self, x):
        x = x.reshape(-1, 28, 28)
        h0 = torch.zeros(self.num_layers*2, x.size(0), self.hidden_size).to('cuda') 
        c0 = torch.zeros(self.num_layers*2, x.size(0), self.hidden_size).to('cuda')
        out, cell = self.lstm(x, (h0, c0))
        
        out = self.fc(out[:, -1, :])
        return out, cell

class CNN_BiLSTM(nn.Module):
    def __init__(self, out_dim):
        super().__init__()

        #Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0)
        self.hidden_size = 128
        self.num_layers = 2
        self.batch_size = 36
        
        self.features = nn.Sequential(
            nn.Conv2d(1, 6, 5),
            nn.MaxPool2d(2),
            nn.ReLU(inplace=True),
            nn.Conv2d(6, 16, 5),
            nn.MaxPool2d(2),
            nn.ReLU(inplace=True),
         )
        
        self.lstm = nn.LSTM(16*4*4, self.hidden_size, self.num_layers, batch_first=True, bidirectional=True)
        self.fc = nn.Linear(self.hidden_size*2, out_dim)
        
    def forward(self, x):
        x = self.features(x)
        x = x.view(x.shape[0], -1, 16*4*4)
        h0 = torch.zeros(self.num_layers*2, x.size(0), self.hidden_size).to('cuda') 
        c0 = torch.zeros(self.num_layers*2, x.size(0), self.hidden_size).to('cuda')
        out, cell = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        
        return out, cell    


class CNN_256(nn.Module):
    def __init__(self, output_dim):
        super().__init__()

        #Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0)

        self.features = nn.Sequential(
            nn.Conv2d(1, 6, 5),
            nn.MaxPool2d(2),
            nn.ReLU(inplace=True),
            nn.Conv2d(6, 16, 5),
            nn.MaxPool2d(2),
            nn.ReLU(inplace=True),
         )

        self.classifier = nn.Sequential(
            nn.Linear(16*61*61, 120),
            nn.ReLU(inplace=True),
            nn.Linear(120, 84),
            nn.ReLU(inplace=True),
            nn.Linear(84, output_dim)
         )

    def forward(self, x):
        x = self.features(x)
        h = x.view(x.shape[0], -1)
        x = self.classifier(h)
        return x, h
