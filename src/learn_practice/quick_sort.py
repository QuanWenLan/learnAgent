def quicksort(arr):
    """
    快速排序（Quick Sort）函数：对输入列表进行升序排序。

    算法思想：
    1. 选择一个“基准值”（pivot）
    2. 将数组分为两部分：小于 pivot 的元素放左边，大于等于的放右边
    3. 递归地对左右子数组排序
    4. 合并结果：左 + [pivot] + 右

    时间复杂度：
    - 平均情况：O(n log n)
    - 最坏情况：O(n²)（当每次选到最大/最小值作 pivot）
    - 最好情况：O(n log n)

    空间复杂度：O(log n)（递归调用栈的深度，平均情况）

    参数:
        arr (list): 待排序的数字列表

    返回:
        list: 排序后的新列表（不修改原列表）
    """
    # 基线条件（递归终止条件）：空列表或单个元素无需排序
    if len(arr) <= 1:
        return arr

    # 选择第一个元素作为基准值（pivot）
    pivot = arr[0]

    # 分割：将除 pivot 外的元素分为 left 和 right
    # 注意：使用 arr[1:] 跳过 pivot，避免重复包含
    left = [x for x in arr[1:] if x < pivot]  # 所有小于 pivot 的元素
    right = [x for x in arr[1:] if x >= pivot]  # 所有大于或等于 pivot 的元素

    # 递归排序左右子数组，并合并结果
    # 左边（小） + 基准值 + 右边（大）
    return quicksort(left) + [pivot] + quicksort(right)


# ===== 示例用法 =====
if __name__ == "__main__":
    # 测试数据
    numbers = [64, 34, 25, 12, 22, 11, 90]
    print("原始列表:", numbers)

    sorted_numbers = quicksort(numbers)
    print("排序后列表:", sorted_numbers)

    # 验证原列表未被修改（因为函数返回新列表）
    print("原列表是否不变?", numbers == [64, 34, 25, 12, 22, 11, 90])  # True