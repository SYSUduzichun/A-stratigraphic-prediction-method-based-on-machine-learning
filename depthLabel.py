# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 15:54:32 2018

@author: Administrator
"""
max_layer_depth=102.35
min_layer_depth=0.1
def depthLabel0(depth):
    if depth<0.1:#EOS
        return 1;
    elif depth <5:
        return 2+int(depth/0.5)#min 2 max 11 
    elif depth<10:
        return 2+10+int((depth-5)/1)#min 12 max 16 
    elif depth<20:
        return 2+10+5+int((depth-10)/2)#min 17 max 21 
    elif depth<40:
        return 2+10+5+5+int((depth-20)/4)#min 22 max 26
    elif depth<60:
        return  2+10+5+5+5+int((depth-40)/5)#min 27 max 30
    elif depth<80:
        return  2+10+5+5+5+4+int((depth-60)/10)#min 31 max 32
    else:
        return 33
    
def LabelToDepthRange0(label):
    if label==0 or label==1:
        return [0,0]
    elif label <=11:
        return [(label-2)*0.5,(label-1)*0.5]#min 0  max 5
    elif label <=16:
        return [5+(label-12)*1,5+(label-11)*1]#min 5  max 10
    elif label <=21:
        return [10+(label-17)*2,10+(label-16)*2]#min 10  max 20
    elif label <=26:
        return  [20+(label-22)*4,20+(label-21)*4]#min 20  max 40
    elif label <=30:
        return  [40+(label-27)*5,40+(label-26)*5]#min 40  max 60
    elif label <=32:
        return  [60+(label-31)*10,60+(label-30)*10]#min 40  max 60
    else:
        return  [80,100]
def getOriginDepth0(depth):
    if depth==-1:
        return 0
    return (max_layer_depth-min_layer_depth)*depth+min_layer_depth

def depthLabel1(depth):
    if depth<0.1:#EOS
        return 1;
    elif depth <16:
        return 2+int((depth)/2)#min 2 max 9
    elif depth<40:
        return 10+int((depth-16)/4)#min 10 max 15 
    elif depth<60:
        return 16+int((depth-40)/5)#min 16 max 19 
    elif depth<80:
        return 20+int((depth-60)/10)#min 20 max 21
    else:
        return 22
    
def LabelToDepthRange1(label):
    if label==0 or label==1:
        return [0,0]
    elif label <=9:
        return [(label-2)*2,(label-1)*2]#min 0  max 5
    elif label <=15:
        return [16+(label-10)*4,16+(label-9)*4]#min 5  max 10
    elif label <=19:
        return [40+(label-16)*5,40+(label-15)*5]#min 10  max 20
    elif label <=21:
        return [60+(label-20)*10,60+(label-19)*10]#min 20  max 40
    else:
        return  [80,100]
def getOriginDepth1(depth):
    if depth==-1:
        return 0
    return (max_layer_depth-min_layer_depth)*depth+min_layer_depth

def depthLabel2(depth):
    if depth<0.1:#EOS
        return 1;
    elif depth <50:
        return 2+int((depth)/5)#min 2 max 11
    elif depth<80:
        return 12+int((depth-50)/10)#min 12 max 14 
    else:
        return 15
    
def LabelToDepthRange2(label):
    if label==0 or label==1:
        return [0,0]
    elif label <=11:
        return [(label-2)*5,(label-1)*5]#min 0  max 5
    elif label <=14:
        return [50+(label-12)*10,50+(label-11)*10]#min 5  max 10
    else:
        return  [80,102.35]
def getOriginDepth2(depth):
    if depth==-1:
        return 0
    return (max_layer_depth-min_layer_depth)*depth+min_layer_depth

def depthLabel(depth):
    '''
    EOS:7 also serves as padding
    SOS:8
    '''
    if abs(depth-255)<0.5:
        return 7#EOS
    if depth == 0:
        return 0;
    elif depth <0.24657:#1
        return 0
    elif depth<0.47157:#3
        return 1
    elif depth <0.57618:#5
        return 2
    elif depth<0.718144:#10
        return 3
    elif depth <0.860101:#20
        return 4
    elif depth<0.94314:#30
        return 5
    else:
        return 6

'''


'''
def markVariable(Vari):
    Vari=Vari.squeeze()
    batch_size=Vari.size(0)
    seq_len=Vari.size(1)
    
    for i in range(batch_size):
        for j in range(seq_len):
            Vari[i,j]=depthLabel(Vari[i,j])
    return Vari

