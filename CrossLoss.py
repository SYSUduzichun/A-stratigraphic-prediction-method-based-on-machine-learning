from torch.autograd import Variable
import torch
import torch.nn as nn
from depthLabel import depthLabel

class CrossLoss(nn.Module):
    def __init__(self,ignore_index = 0):
        super(CrossLoss, self).__init__()
        self.ignore_index = ignore_index
        self.criterion=nn.CrossEntropyLoss(ignore_index=0)

    def forward(self, input, target):

        ind = (target != self.ignore_index).float()
        num_all = torch.sum(ind).data[0]

        #print(target)
        size0=target.size(0)
        size1=target.size(1)
        temp=target.cpu().data
        for i in range(size0):
            for j in range(size1):
                temp[i,j]=depthLabel(temp[i,j])
                
        
        pred= torch.mul(input,ind).long()
        temp=temp.long()
        
        loss=self.criterion(pred,temp)
        return loss,num_all
