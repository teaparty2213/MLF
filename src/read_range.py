# calculate the range of read index at each site
def read_range(r, s, M):
    read_range_list = []
    first = 0
    last = 0
    for j in range(s):
        i = 0
        while (i < r and M[i][j] == -1):
            i += 1
        first = i
        while (i < r and M[i][j] != -1):
            i += 1
        last = i - 1
        read_range_list.append((first, last))
    return read_range_list