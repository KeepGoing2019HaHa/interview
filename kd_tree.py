class Node(object):
    def __init__(self):
        self.father = None
        self.left = None
        self.right = None
        self.feature = None
        self.split = None


class KDTree(object):
    def __init__(self):
        self.root = Node()

    def _get_median_idx(self, X, idxs, feature):
        n = len(idxs)
        k = n // 2
        col = map(lambda i: (i, X[i][feature]), idxs)
        sorted_idxs = map(lambda x: x[0], sorted(col, key=lambda x: x[1]))
        median_idx = list(sorted_idxs)[k]
        return median_idx

    def _get_variance(self, X, idxs, feature):
        n = len(idxs)
        col_sum = col_sum_sqr = 0
        for idx in idxs:
            xi = X[idx][feature]
            col_sum += xi
            col_sum_sqr += xi ** 2
        return col_sum_sqr / n - (col_sum / n) ** 2

    def _choose_feature(self, X, idxs):
        m = len(X[0])
        variances = map(lambda j: (
            j, self._get_variance(X, idxs, j)), range(m))
        return max(variances, key=lambda x: x[1])[0]

    def _split_feature(self, X, idxs, feature, median_idx):
        idxs_split = [[], []]
        split_val = X[median_idx][feature]
        for idx in idxs:
            if idx == median_idx:
                continue
            xi = X[idx][feature]
            if xi < split_val:
                idxs_split[0].append(idx)
            else:
                idxs_split[1].append(idx)
        return idxs_split

    def build_tree(self, X, y):
        # X_scale = self.min_max_scale(X)
        X_scale = X
        nd = self.root
        idxs = range(len(X))
        que = [(nd, idxs)]
        while que:
            nd, idxs = que.pop(0)
            n = len(idxs)
            if n == 1:
                nd.split = (X[idxs[0]], y[idxs[0]])
                continue
            feature = self._choose_feature(X_scale, idxs)
            median_idx = self._get_median_idx(X, idxs, feature)
            idxs_left, idxs_right = self._split_feature(X, idxs, feature, median_idx)
            nd.feature = feature
            nd.split = (X[median_idx], y[median_idx])
            if idxs_left != []:
                nd.left = Node()
                nd.left.father = nd
                que.append((nd.left, idxs_left))
            if idxs_right != []:
                nd.right = Node()
                nd.right.father = nd
                que.append((nd.right, idxs_right))

    def get_euclidean_distance(self, arr1, arr2):
        # return ((arr1 - arr2) ** 2).sum() ** 0.5
        return sum([(a-b)**2 for a,b in zip(arr1,arr2)]) ** 0.5

    def _get_eu_dist(self, Xi, nd):
        X0 = nd.split[0]
        return self.get_euclidean_distance(Xi, X0)

    def _get_hyper_plane_dist(self, Xi, nd):
        j = nd.feature
        X0 = nd.split[0]
        return (Xi[j] - X0[j]) ** 2

    # 按照自己的理解写的
    # 核心是：如果Xi到超平面的垂直距离D都大于当前遍历到的最小值，那超平面另外一段完全不用遍历了。复杂度介于logN和N之间
    # 如果是topK的话，就维护一个优先队列保存已经遍历的topk小值，如果D大于max(topk小值)，那超平面另外一段完全不用遍历了
    def nearest_neighbour_search(self, Xi):
        q = [self.root]
        dist_min, nearest = self._get_eu_dist(Xi, self.root), self.root
        while q:
            cur = q.pop()
            if cur.feature is None:
                continue

            # hyper_dist = self._get_hyper_plane_dist(Xi, cur)
            hyper_dist = abs(Xi[cur.feature] - cur.split[0][cur.feature])

            if cur.left:
                # if True:
                if Xi[cur.feature] <= cur.split[0][cur.feature] or hyper_dist <= dist_min:
                    q.append(cur.left)

                    dist_left = self._get_eu_dist(Xi, cur.left)
                    if dist_left < dist_min:
                        dist_min = dist_left
                        nearest = cur.left

            if cur.right:
                # if True:
                if Xi[cur.feature] >= cur.split[0][cur.feature] or hyper_dist <= dist_min:
                    q.append(cur.right)

                    dist_right = self._get_eu_dist(Xi, cur.right)
                    if dist_right < dist_min:
                        dist_min = dist_right
                        nearest = cur.right

        return nearest


    def exhausted_search(self, X, Xi):
        dist_best = float('inf')
        row_best = None
        for row in X:
            dist = self.get_euclidean_distance(Xi, row)
            if dist < dist_best:
                dist_best = dist
                row_best = row
        return row_best


def gen_data(low, high, n_rows, n_cols=None):
    from random import randint
    if n_cols is None:
        ret = [randint(low, high) for _ in range(n_rows)]
    else:
        ret = [[randint(low, high) for _ in range(n_cols)]
               for _ in range(n_rows)]
    return ret

def main():
    from time import time
    print("Testing KD Tree...")
    test_times = 100
    run_time_1 = run_time_2 = 0
    for _ in range(test_times):
        low = 0
        high = 100
        n_rows = 1000
        n_cols = 2
        X = gen_data(low, high, n_rows, n_cols)
        y = gen_data(low, high, n_rows)
        Xi = gen_data(low, high, n_cols)

        tree = KDTree()
        tree.build_tree(X, y)

        start = time()
        nd = tree.nearest_neighbour_search(Xi)
        run_time_1 += time() - start
        ret1 = tree.get_euclidean_distance(Xi, nd.split[0])

        start = time()
        row = tree.exhausted_search(X, Xi)
        run_time_2 += time() - start
        ret2 = tree.get_euclidean_distance(Xi, row)

        assert ret1 == ret2, str(ret1) + '#' + str(ret2)
    print("%d tests passed!" % test_times)
    print("KD Tree Search %.2f s" % run_time_1)
    print("Exhausted search %.2f s" % run_time_2)


main()