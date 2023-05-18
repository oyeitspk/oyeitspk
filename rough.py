def longest_subsequence(arr):
    sseq = []
    for n in arr:
        if len(sseq) == 0:
            sseq.append(n)
        else:
            if sseq[-1] + 1 == n:
                sseq.append(n)
            else:
                sseq = [n]
    if len(sseq) == 1:
        sseq = []
    print(sseq)
    return sseq

longest_subsequence([1,2,3,4,5])
longest_subsequence([3,1,2,7,3,4,5])
longest_subsequence([1,1,0,0])
longest_subsequence([3,4,5,1,8,0])
longest_subsequence([1,2,3,4,5,9])
