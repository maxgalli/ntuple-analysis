def _print_names_right_aligned(left_aligned_name, lst):
    names_lst = [str(element) for element in lst]
    longest_name = max(names_lst, key=len)
    safe_number = len(longest_name) + len(left_aligned_name) + 5
    right_aligned_names = '\n'.join([
        f'{name:>{safe_number-len(longest_name)+len(name)}}' for name in names_lst
        ])
    return right_aligned_names
