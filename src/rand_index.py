from sklearn.metrics.cluster import adjusted_rand_score

def rand_index(ans, alg, a, b, N):
    L = b - a + 1
    comb = L * (L - 1) / 2
    ans_ele_num = [0] * N
    alg_ele_num = [0] * N
    for i in range(a, b + 1):
        ans_ele_num[ans[i]] += 1
        alg_ele_num[alg[i]] += 1
    for i in range(N):
        ans_ele_num[i] /= L
        alg_ele_num[i] /= L
        
    RI = 0
    for i in range(a, b + 1):
        for j in range(i + 1, b + 1):
            if (ans[i] == ans[j] and alg[i] == alg[j]) or (ans[i] != ans[j] and alg[i] != alg[j]):
                RI += 1
    
    penalty = 0
    for i in range(N):
        penalty += ans_ele_num[i] * alg_ele_num[i]
    penalty *= comb
    
    ARI = (RI - penalty) / (comb - penalty) # normalized
    return ARI
    