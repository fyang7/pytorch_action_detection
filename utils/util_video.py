# **********************************************************
#  Author        : Fan Yang
#  Email         : yangfan43@baidu.com
#  Last modified : 2018-06-25 15:51
#  Filename      : util_video.py
#  Description   : 
#  *********************************************************

from utils import *
from util_func import *

class THUMOS:
    """
        thumos 14 dataset
    """
    def __init__():
        pass
    def get_key():
        pass

class ActivityNet:
    """
        activitynet1.3 dataset generator
    """
    def __init__(self, gt_file, use_default=True, new_train_list="", new_val_list=""):
        self.gt_annos = read_json(gt_file)["database"]
        self.vid_list = {"testing":[], "training":[], "validation":[]}
        self.duration = {}
        # default
        for key in self.gt_annos:
            self.vid_list[self.gt_annos[key]["subset"]].append(key)
            self.duration[key] = self.gt_annos[key]["duration"]
        # new divide dataset
        if use_default == False:
            assert new_train_list != "" 
            assert new_val_list != ""
            self.vid_list["training"] = read_list(new_train_list)
            self.vid_list["validation"] = read_list(new_val_list)

    def get_key_list(self, mode):
        """
            input: example/ training
            output: [key1, key2, ... keyN]
        """
        if mode == "all":
            return self.vid_list["training"] + self.vid_list["testing"] + self.vid_list["validation"]
        return self.vid_list[mode]

    def get_cls_label(self, mode, convert=False, convert_file=""): 
        """
            input: example/ training, true, labels_convert.txt
            output:  key: [label1, label2, ...]
        """
        result = {}
        for key in self.vid_list[mode]:
            anno = self.gt_annos[key]["annotations"]
            labels = [item["label"] for item in anno]
            result[key] = labels
        return result
    
    def get_det_label(self, mode, convert=False, convert_file=""):
        """
            input: example/ training, true, labels_convert.txt
            output: key: [{"label":label, "segment":[start, end]}, {}, ....]
        """
        result = {}
        for key in self.vid_list[mode]:
            anno = self.gt_annos[key]["annotations"]
        return result
    
    def get_proposal(self, pr_file=""):
        """
            input: example/ train_pr.json, hth=high_thresh, lth=low_thresh, 
            output: key: {"pos":[[s1, e1], [s2, e2], ...], "neg":[]}
        """
        result = {}
        import json 
        proposals = json.loads(open(pr_file).read())["results"]
        for key in proposals:
            result[key] = []
            for item in proposals[key]:
                seg = item["segment"]
                result[key].append([1.0*seg[0]/self.duration[key], 1.0*seg[1]/self.duration[key]])
        return result

    def get_proposal_label(self, pr_file="", hth=0.7, lth=0.3, drop_zero=False, with_label=False, with_reg=False, convert_pool=False):
        """
            input: example/ train_pr.json, hth=high_thresh, lth=low_thresh, 
            output: key: {"pos":[[s1, e1], [s2, e2], ...], "neg":[]}
        """
        result = {}
        import json 
        proposals = json.loads(open(pr_file).read())["results"]
        for key in proposals:
            result[key] = {"pos":[], "neg":[]}
            all_segs = proposals[key]
            gt_segs = [item["segment"] for item in self.gt_annos[key]["annotations"]]
            for item in all_segs:
                seg = item["segment"]
                max_iou = calc_max_iou(seg, gt_segs)
                if drop_zero and max_iou == 0:
                    continue
                if max_iou <= lth:
                    result[key]["neg"].append([1.0*seg[0]/self.duration[key], 1.0*seg[1]/self.duration[key]])
                elif max_iou >= hth:
                    result[key]["pos"].append([1.0*seg[0]/self.duration[key], 1.0*seg[1]/self.duration[key]])
                else:
                    continue
        # convert to pos and neg pool
        if not convert_pool:
            print "lth:{} hth:{}\n  PR INFO: total pos {}  total neg {}".format(lth, hth, sum([len(result[key]["pos"]) for key in result]), sum([len(result[key]["neg"]) for key in result]))
            return result
        pool_result = {"pos":[], "neg":[]}
        for key in result:
            for item in result[key]["pos"]:
                pool_result["pos"].append((key, item))
            for item in result[key]["neg"]:
                pool_result["neg"].append((key, item))
        import random
        random.shuffle(pool_result["pos"])
        random.shuffle(pool_result["neg"])
        print "lth:{} hth:{}\n  PR INFO: total pos {}  total neg {}".format(lth, hth, len(pool_result["pos"]), len(pool_result["neg"]))
        return pool_result

    def get_proposal_iou(self, pr_file=""):
        """
            input: example/ train_pr.json, hth=high_thresh, lth=low_thresh,
            output: key: {"pos":[[s1, e1], [s2, e2], ...], "neg":[]}
        """
        result = {}
        import json
        proposals = json.loads(open(pr_file).read())["results"]
        for key in proposals:
            result[key] = []
            all_segs = proposals[key]
            gt_segs = [item["segment"] for item in self.gt_annos[key]["annotations"]]
            for item in all_segs:
                seg = item["segment"]
                max_iou = calc_max_iou(seg, gt_segs)
                result[key].append(([1.0*seg[0]/self.duration[key], 1.0*seg[1]/self.duration[key]], max_iou))
        return result

if __name__ == "__main__":
    dataset = ActivityNet("activity_net.v1-3.min.json")
