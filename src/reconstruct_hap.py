import random
import matplotlib.pyplot as plt
import seaborn as sns

def edit_distance(hap1, hap2, s):
    distance = 0
    for i in range(s):
        if hap1[i] != hap2[i]:
            distance += 1
    return distance

def reconstruct_haplotype(r, s, N, M, color, ans):
    hap = []

    for i in range(N): # i番目のハプロタイプを再構築
        read_index = []
        for j in range(r):
            if color[j] == i:
                read_index.append(j)
        hap_row = []
        for j in range(s): # j番目のSNPについて多数決
            count = [0, 0, 0 ,0] # 0, 1, 2, 3の数
            for k in range(len(read_index)): # 色iのk番目のリードを見る
                if (M[read_index[k]][j] != -1):
                    allele = M[read_index[k]][j]
                    count[allele] += 1
                    
            if max(count) == 0: # どのリードもSNP_jについて情報を持っていない
                hap_row.append(-1)
            else:
                candidate = []
                for i in range(0, 4):
                    if count[i] == max(count):
                        candidate.append(i)
                hap_row.append(random.choice(candidate))
        hap.append(hap_row)
    
    heat_map = [[0 for _ in range(N)] for _ in range(N)] # heat_map[i][j] = 出力ハプロタイプiと答えハプロタイプjの近さ(0~1, 1に近いほど正解に近い)  
    for i in range(N):
        for j in range(N):
            heat_map[i][j] = 1 - (edit_distance(hap[i], ans[j], s) / s)
            
    #  対角成分に1に近い数字がくるように行をソート(列は維持する)
    result = []
    for j in range(N):
        max_index = 0
        for i in range(len(heat_map)):
            if heat_map[i][j] > heat_map[max_index][j]:
                max_index = i
        result.append(heat_map[max_index])
        heat_map.pop(max_index)
    
    plt.figure()
    sns.heatmap(result, cmap='Blues', xticklabels=True, yticklabels=True)
    plt.xlabel("Answer")
    plt.ylabel("Reconstructed")
    plt.title("Haplotype similarity matrix of {}-ploid".format(N))
    plt.savefig("./../result/250126_{}-ploid-matrix_q=N.png".format(N))