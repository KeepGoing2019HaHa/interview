import random
import math
from collections import Counter, deque
import matplotlib.pyplot as plt

class Node:
    def __init__(self, val, feat_idx):
        self.val = val
        self.feat_idx = feat_idx
        self.left = None
        self.right = None
        self.pred = None
    def __repr__(self):
        q,qq=deque([self]),deque([])
        all_prints = []
        while q:
            layer_print=[]
            while q:
                s=q.popleft()
                if s.pred is None:
                    layer_print.append("{}_{}".format(s.feat_idx,s.val))
                    qq.append(s.left)
                    qq.append(s.right)
                else:
                    layer_print.append("{}".format(s.pred))
            all_prints.append(' '.join(layer_print))
            q,qq=qq,q
        return '\n'.join(all_prints)

# 一直划分，直到完全分好
# 只有2维feature

def entropy(ys):
    d = Counter(ys)
    ps = [d[k]/len(ys) for k in d]
    return sum(-p*math.log(p) for p in ps)

def gain(points, idx):
    n = len(points)
    xs = [point[idx] for point in points]
    ys = [point[2] for point in points]
    select_val = sum(xs) / n
    ys_left = [y for x,y in zip(xs,ys) if x<=select_val]
    ys_right = [y for x, y in zip(xs, ys) if x > select_val]
    left_prob = len(ys_left) / n
    gain = entropy(ys) - (left_prob*entropy(ys_left)+(1-left_prob)*entropy(ys_right))
    return gain,select_val


def fit(points):
    n = len(points)
    if len(set(points[i][2] for i in range(n))) == 1:
        leaf = Node(None, None)
        leaf.pred = points[0][2]
        return leaf

    # feat2gain
    gain_x, val_x = gain(points, 0)
    gain_y, val_y = gain(points, 1)
    select_idx = 0 if gain_x>gain_y else 1
    select_val = val_x if gain_x>gain_y else val_y
    root = Node(select_val, select_idx)
    root.left = fit([points[i] for i in range(n) if points[i][select_idx] <= select_val])
    root.right = fit([points[i] for i in range(n) if points[i][select_idx] > select_val])
    return root


xys = [list(range(10)) for _ in range(10)]
pos_xys = []
neg_xys = []
for i in range(-5,6):
    if i==0: continue
    for j in range(-5,6):
        if j==0: continue
        if i * j>0:
            pos_xys.append((i, j, 1))
        else:
            neg_xys.append((i, j, 0))
points = pos_xys + neg_xys

tree = fit(points)
print(tree)

# xs_pos = [s[0] for s in pos_xys]
# ys_pos = [s[1] for s in pos_xys]
# xs_neg = [s[0] for s in neg_xys]
# ys_neg = [s[1] for s in neg_xys]
# plt.plot(xs_pos, ys_pos, 'ro')
# plt.plot(xs_neg, ys_neg, 'r+')
# plt.show()