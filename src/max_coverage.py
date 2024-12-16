def max_coverage(read_range_list):
    max_coverage = 0
    for i in range(len(read_range_list)):
        max_coverage = max(max_coverage, read_range_list[i][1] - read_range_list[i][0] + 1)
    return max_coverage