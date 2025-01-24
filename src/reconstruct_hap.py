import random
import matplotlib.pyplot as plt

def edit_distance(hap1, hap2, s):
    distance = 0
    for i in range(s):
        if hap1[i] != hap2[i]:
            distance += 1
    return distance

def recostruct_haplotype(r, s, N, M, color, ans):
    hap = [[] for _ in range(N)]
    read_index = [[] for _ in range(N)]
    for i in range(r):
        read_index[color[i]].append(i) # 色ごとにリードを分類

    for i in range(N): # i番目のハプロタイプを再構築
        for j in range(s): # j番目のSNPについて多数決
            count = [0, 0, 0 ,0] # 0, 1, 2, 3の数
            for k in range(len(read_index[i])): # 色iのk番目のリードを見る
                if (M[read_index[i][k]][j] != -1):
                    allele = M[read_index[i][k]][j]
                    count[allele] += 1
                    
            if max(count) == 0: # どのリードもSNP_jについて情報を持っていない
                hap[i].append(-1)
            else:
                candidate = []
                for i in range(0, 4):
                    if count[i] == max(count):
                        candidate.append(i)
                hap[i].append(random.choice(candidate))
    
    heat_map = [[0 for _ in range(N)] for _ in range(N)] # heat_map[i][j] = 出力ハプロタイプiと答えハプロタイプjの編集距離  
    for i in range(N):
        for j in range(N):
            heat_map[i][j] = edit_distance(hap[i], ans[j], s) / s
    
    plt.figure()
    plt.imshow(heat_map, cmap='hot', interpolation='nearest')
    plt.legend()
    plt.show()