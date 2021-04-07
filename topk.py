import random

def top_k_heap(arr, k=10):
    def heapy(arr, s, end):
        while s < end:
            l,r = 2*s+1,2*s+2
            if l<end and arr[l]>arr[s] and (r>=end or arr[l]>arr[r]):
                arr[l],arr[s] = arr[s],arr[l]
                s = l
            elif r<end and arr[r]>arr[s] and arr[r]>arr[l]:
                arr[r],arr[s] = arr[s],arr[r]
                s = r
            else:
                break

    pq = arr[:k]
    for i in range(k//2, -1, -1):
        heapy(pq, i, k)
    for i in range(k, len(arr)):
        if arr[i] < pq[0]:
            pq[0] = arr[i]
            heapy(pq, 0, k)
    return pq


def top_k_sort(arr, k=10):
    def partion(arr, lo, hi):
        pivot = lo
        while lo<=hi:
            while lo<=hi and arr[lo]<=arr[pivot]: lo+=1
            while lo<=hi and arr[hi]>=arr[pivot]: hi-=1
            if lo<=hi: arr[lo],arr[hi] = arr[hi],arr[lo]
        a[hi],a[pivot] = a[pivot],a[hi]
        return hi

    lo,hi = 0,len(arr)-1
    while 1:
        index = partion(arr, lo, hi)
        if index == k-1:
            break
        elif index < k-1:
            lo = index+1
        else:
            hi = index
    return arr[:k]

for test_id in range(100):
    # k = 10
    k = random.randint(1, 100)
    # print(test_id, k)
    a = list(range(1000))
    random.shuffle(a)
    assert tuple(sorted(a)[:k]) == tuple(sorted(top_k_heap(a, k)))
    assert tuple(sorted(a)[:k]) == tuple(sorted(top_k_sort(a, k)))