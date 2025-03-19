import numpy as np
from scipy.stats import ttest_ind

def bool_1d(x_sel, x_all): 
    
    idx = []
    for x0 in x_all:
        if x0 in x_sel:
            idx.append(True)
        else:
            idx.append(False) 
    idx = np.array(idx).squeeze()
    
    return idx


def ttest_3d(matrix1, matrix2, axis=0, equal_var=False):
    """
    对两个三维矩阵沿指定维度进行独立样本t检验，返回p值矩阵
    
    参数：
    matrix1 (np.ndarray) : 第一个三维数据矩阵
    matrix2 (np.ndarray) : 第二个三维数据矩阵
    axis (int)          : 沿哪个维度进行检验 (0/1/2)
    equal_var (bool)    : 是否假设方差齐性，默认False（使用Welch's t-test）
    
    返回：
    p_values (np.ndarray) : p值矩阵，维度比输入少一维
    
    示例：
    >>> A = np.random.randn(10, 20, 30)  # 维度0有10个样本
    >>> B = np.random.randn(15, 20, 30)  # 维度0有15个样本
    >>> p = ttest_3d(A, B, axis=0)       # 沿样本维度检验
    >>> p.shape
    (20, 30)
    """
    # 验证输入维度
    if matrix1.ndim != 3 or matrix2.ndim != 3:
        raise ValueError("输入必须是三维矩阵")
    
    # 验证非检验维度的一致性
    target_shape = [s for i, s in enumerate(matrix1.shape) if i != axis]
    compare_shape = [s for i, s in enumerate(matrix2.shape) if i != axis]
    if target_shape != compare_shape:
        raise ValueError(f"非检验维度不匹配: {target_shape} vs {compare_shape}")
    
    # 执行t检验
    _, p_values = ttest_ind(matrix1, matrix2, axis=axis, equal_var=equal_var)
    
    return p_values

