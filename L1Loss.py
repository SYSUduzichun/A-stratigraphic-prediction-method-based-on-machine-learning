from torch.autograd import Variable
import torch
import torch.nn as nn
from depthLabel import depthLabel

class L1Loss(nn.Module):
    def __init__(self,ignore_index = 0):
        super(L1Loss, self).__init__()
        self.ignore_index = ignore_index

    def forward(self, input, target):

        ind = (target != self.ignore_index).float()
        num_all = torch.sum(ind).data[0]


        #loss = torch.mul(torch.abs(input - target),ind)
        loss = torch.mul(torch.pow(input - target,2),ind)
        loss  = torch.sum(loss).div_(num_all)

        return loss,num_all
