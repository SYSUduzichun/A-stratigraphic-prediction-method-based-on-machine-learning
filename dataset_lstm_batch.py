import torch.utils.data as data
from os.path import join
from PIL import Image
import numpy as np
import pickle

EOS_token=16 #for end and padding

class HoleDataset(data.Dataset):
    def __init__(self,phase,num = 0):
        super(HoleDataset, self).__init__()
        coordinate_list = []
        hole_depth_list = []
        layer_num_list = []
        X = []
        Y = []
        # load the adjacent nodes 
        data_file = open('data/sample_merge.txt','r')
        lines = data_file.readlines()
        data_file.close()
	
        type_gt = np.ones((len(lines),10,1)) * EOS_token#28+1 多一位放EOS
        depth_gt = np.ones((len(lines),10,1)) *0
        end_gt = np.ones((len(lines),10,1)) * EOS_token

        for i,line in enumerate(lines):
            sep_line = line.strip().split(' ')
            x = float(sep_line[1])
            y = float(sep_line[2])
            
            start_depth = float(sep_line[3])
            hole_depth = float(sep_line[4])
                        
            layer_num = int(sep_line[5])
    
            coordinate_list.append([x,y,start_depth])
            hole_depth_list.append(hole_depth)
            layer_num_list.append(layer_num)
            X.append(x)
            Y.append(y) 
	    # get the layer depth and layer type info
            j = 6
            count = 0
            while(j < (len(sep_line) - 1)):
                layer_type = int(sep_line[j])
                type_gt[i,count,0] = layer_type
                j+=1
                layer_depth = float(sep_line[j])
                depth_gt[i,count,0] = layer_depth
                j+=1
                end_gt[i,count,0] = 0
                count+=1
            end_gt[i,count-1,0] = 1
                # layer_type = int(sep_line[j])
                # one-hot vector
                # input[i,count,layer_type] = 1
                # j+=1
                # layer_depth = float(sep_line[j])
                # input[i,count,-1] = layer_depth
                # j+=1
                # count+=1
        dis_file = 'data/sample_merge_dis.txt'
        dis = np.loadtxt(dis_file).astype(np.int64)


        self.num = num
        self.train_coordinate_list = coordinate_list[:2848]
        self.train_hole_depth_list = hole_depth_list[:2848]
        self.train_layer_num_list = layer_num_list[:2848]
        self.train_X = X[:2848]
        self.train_Y = Y[:2848]
        self.train_dis = dis[:2848]
        

        if phase == "train":
            self.type_gt = type_gt[:2848,:,:]
            self.depth_gt = depth_gt[:2848,:,:]
            self.end_gt = end_gt[:2848,:,:]
            self.coordinate_list = coordinate_list[:2848]
            self.hole_depth_list = hole_depth_list[:2848]
            self.layer_num_list = layer_num_list[:2848]
            self.X = X[:2848]
            self.Y = Y[:2848]
            self.dis = dis[:2848]
        else:
            self.type_gt = type_gt[2848:,:,:]
            self.depth_gt = depth_gt[2848:,:,:]
            self.end_gt = end_gt[2848:,:,:]
            self.coordinate_list = coordinate_list[2848:]
            self.hole_depth_list = hole_depth_list[2848:]
            self.layer_num_list = layer_num_list[2848:]
            self.X = X[2848:]
            self.Y = Y[2848:]
            self.dis = dis[2848:]




    def __getitem__(self, index):
        coordinate = []
        coordinate.extend(self.coordinate_list[index])
        for i in range(self.num):
            ind = self.dis[index,i]
            coordinate.extend(self.train_coordinate_list[ind])
            coordinate.append(self.train_layer_num_list[ind] - 1)
            coordinate.append(self.train_hole_depth_list[ind])

        hole_depth = self.hole_depth_list[index]
        layer_num = self.layer_num_list[index] - 1
	

	#coordinate.append(hole_depth)
	#coordinate.append(layer_num)
        coordinate = np.array(coordinate)        

        type_gt = self.type_gt[index,:,:]
        depth_gt = self.depth_gt[index,:,:]
        end_gt = self.end_gt[index,:,:]

        a=layer_num+1
    
        return coordinate,type_gt,depth_gt,end_gt,a

    def __len__(self):
        return len(self.coordinate_list)
