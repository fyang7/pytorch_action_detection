# **********************************************************
#  Author        : Fan Yang
#  Email         : yangfan43@baidu.com
#  Last modified : 2018-06-25 15:51
#  Filename      : util_torch.py
#  Description   : 
#  *********************************************************

import torch 
from util_func import *

###############################################
def save_checkpoint(state, filename='output/checkpoint.pth.tar'):
    torch.save(state, filename)

@file_check
def load_checkpoint(file, model):
    print "==> loading checkpoint '{}'".format(file)
    checkpoint = torch.load(file)
    model_dict = model.state_dict()
    checkpoint = {k: v for k, v in checkpoint['state_dict'].items() if k in model_dict}
    model_dict.update(checkpoint)
    model.load_state_dict(model_dict)
    print "==> finish load checkpoint {}".format(file)
 
###############################################
class AverageMeter(object):
    """Computes and stores the average and current value"""
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

###############################################
def adjust_learning_rate(optimizer, epoch):
    if epoch < 4:
        lr = 0.0001
    else:
        lr = 0.0001
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr
    return lr

##############################################
def accuracy(output, target, topk=(1,)):
    """Computes the precision@k for the specified values of k"""
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].view(-1).float().sum(0)
        res.append(correct_k.mul_(100.0 / batch_size))
    return res
