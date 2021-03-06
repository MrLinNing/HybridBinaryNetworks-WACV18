import torch.nn as nn
import torch.nn.functional as F
from newlayers.BinActiveZ import Active

class Net(nn.Module):
    def __init__(self,nClasses):
        super(Net, self).__init__()

        self.relu = nn.ReLU(True)
        self.drop = nn.Dropout2d(0.2)

        self.conv1 = nn.Conv2d(1, 64, kernel_size = 15, stride = 3, padding = 0)
        self.bn1 = nn.BatchNorm2d(64)
        self.maxpool1 = nn.MaxPool2d(kernel_size = 3, stride = 2)

        self.conv2 = nn.Conv2d(64, 128, kernel_size = 5, stride = 1, padding = 0, bias=False)
        self.bn2 = nn.BatchNorm2d(64)
        self.activ2 = Active()
        self.maxpool2 = nn.MaxPool2d(kernel_size = 3, stride = 2)


        self.conv3 = nn.Conv2d(128, 256, kernel_size = 3, stride = 1, padding= 1, bias=False)
        self.bn3 = nn.BatchNorm2d(128)
        self.activ3 = Active()

        # self.conv4 = nn.Conv2d(96, 192, 1, 1)
        self.conv4 = nn.Conv2d(256, 256, kernel_size = 3, stride = 1, padding = 1, bias=False)
        self.bn4 = nn.BatchNorm2d(256)
        self.activ4 = Active()

        self.conv5 = nn.Conv2d(256, 256, kernel_size = 3, stride = 1, padding = 1, bias=False)
        self.bn5 = nn.BatchNorm2d(256)
        self.activ5 = Active()

        self.maxpool3 = nn.MaxPool2d(kernel_size = 3, stride = 2)

        self.conv6 = nn.Conv2d(256, 512, kernel_size = 7, stride = 1, padding = 0, bias=False)
        self.activ6 = Active()
        self.bn6 = nn.BatchNorm2d(256)

        self.conv7 = nn.Conv2d(512, 512, kernel_size = 1, stride = 1, padding = 0, bias=False)
        self.bn7 = nn.BatchNorm2d(512)

        self.conv8 = nn.Conv2d(512, nClasses, kernel_size = 1, stride = 1,  padding = 0)

        self.nClasses = nClasses

    def forward(self, x):

        #print(x.size())
        x = self.relu(self.bn1(self.conv1(x)))
        x = self.maxpool1(x)
        #print(x.size())
        x = self.relu(self.conv2(self.activ2(self.bn2(x))))
        x = self.maxpool2(x)
        #print(x.size())
        x = self.relu(self.conv3(self.activ3(self.bn3(x))))
        x = self.relu(self.conv4(self.activ4(self.bn4(x))))
        #print(x.size())
        x = self.relu(self.conv5(self.activ5(self.bn5(x))))
        x = self.maxpool3(x)
        x = self.relu(self.conv6(self.activ6(self.bn6(x))))
        x = self.drop(x)
        #print(x.size())
        x = self.relu(self.bn7(self.conv7(x)))
        x = self.drop(x)
        #print(x.size())
        x = self.conv8(x)
        #print(x.size())
        x = x.view(-1, self.nClasses)
        #print(x.size())
        return F.log_softmax(x)
