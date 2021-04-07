import random
import math
import matplotlib.pyplot as plt


def sigmoid(x):
    y = 1. / (1 + math.exp(-x))
    return y

def fit(points):
    w1 = random.random()
    w2 = random.random()
    b = random.random()
    iteration = 1000
    lr = 0.001

    for _ in range(iteration):
        for x1, x2, y in points:
            pred_y = sigmoid(w1 * x1 + w2 * x2 + b)

            loss = - y * math.log(pred_y) - (1 - y) * math.log(1 - pred_y)
            grad_w1 = (pred_y - y) * x1
            grad_w2 = (pred_y - y) * x2
            grad_b = pred_y - y

            w1 -= lr * grad_w1
            w2 -= lr * grad_w2
            b -= lr * grad_b

    return w1, w2, b


xys = [list(range(10)) for _ in range(10)]
pos_xys = [(i, j, 1) for i in range(1, 10) for j in range(10-i+1, 10)]
neg_xys = [(i, j, 0) for i in range(1, 10) for j in range(0, 10-i-1)]
points = pos_xys + neg_xys

w1, w2, b = fit(points)
print(w1, w2, b)

xs_pos = [s[0] for s in pos_xys]
ys_pos = [s[1] for s in pos_xys]
xs_neg = [s[0] for s in neg_xys]
ys_neg = [s[1] for s in neg_xys]

plt.plot(xs_pos, ys_pos, 'ro')
plt.plot(xs_neg, ys_neg, 'r+')
# draw boundary: w1*x1+w2*x2+b=0 --> x2=(-w1/w2)*x+(-b/w2)
boundary_xs = list(range(10))
boundary_ys = [-w1/w2*x-b/w2 for x in boundary_xs]
plt.plot(boundary_xs, boundary_ys, 'b-')

plt.show()