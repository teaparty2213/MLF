import random
import matplotlib.pyplot as plt
import seaborn as sns

def edit_distance(hap1, hap2, s): # hamming distance between hap1 and hap2
    distance = 0
    for i in range(s):
        if hap1[i] != hap2[i]:
            distance += 1
    return distance

def reconstruct_haplotype(r, s, N, M, color, ans):
    hap = [] # reconstructed haplotypes

    for i in range(N): # reconstruct haplotype i
        read_index = []
        for j in range(r):
            if color[j] == i:
                read_index.append(j) # collect reads with color i
                
        hap_row = [] # reconstructed haplotype i
        for j in range(s): # about position j
            count = [0, 0, 0 ,0] # the number of alleles: 0, 1, 2, 3
            for k in range(len(read_index)): # for all reads with color i
                if (M[read_index[k]][j] != -1):
                    allele = M[read_index[k]][j]
                    count[allele] += 1
                    
            if max(count) == 0: # if no reads with color i are covered at this position
                hap_row.append(-1)
            else:
                candidate = []
                for i in range(0, 4):
                    if count[i] == max(count):
                        candidate.append(i) # collect alleles with the maximum number of reads
                hap_row.append(random.choice(candidate)) # if there are multiple alleles with the maximum number of reads, randomly select one
        hap.append(hap_row)
    
    # calculate the similarity matrix
    heat_map = [[0 for _ in range(N)] for _ in range(N)] # heat_map[i][j] is the similarity between reconstructed haplotype i and answer haplotype j. The value is between 0 and 1.
    for i in range(N):
        for j in range(N):
            heat_map[i][j] = 1 - (edit_distance(hap[i], ans[j], s) / s) # the larger the value, the more similar reconstructed haplotype i and answer haplotype j are.
            
    # sort the rows so that the diagonal elements are close to 1, while keeping the order of columns
    result = []
    new_hap = []
    for j in range(N):
        max_index = 0
        for i in range(len(heat_map)):
            if heat_map[i][j] > heat_map[max_index][j]:
                max_index = i
        result.append(heat_map[max_index])
        new_hap.append(hap[max_index])
        heat_map.pop(max_index)
    
    # visualize as a heatmap
    plt.figure()
    sns.heatmap(result, cmap='Blues', xticklabels=True, yticklabels=True)
    plt.xlabel("Answer")
    plt.ylabel("Reconstructed")
    plt.title("Haplotype similarity matrix of {}-ploid".format(N))
    plt.savefig("./result/{}-ploid_r={}_s={}_eval.png".format(N, r, s))