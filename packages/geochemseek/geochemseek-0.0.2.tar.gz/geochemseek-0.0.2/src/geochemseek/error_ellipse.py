import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from scipy.stats import chi2

# 在文件顶部添加导入
import config.config as config

def plot_error_ellipse(mean, cov=None, x_err=None, y_err=None, rho=0, confidence=0.95, 
                      ax=None, show_points=False, show_center=False, **kwargs):
    """
    绘制误差椭圆
    
    参数：
    mean : array-like, shape (2,)
        椭圆中心的均值向量
    cov : array-like, shape (2, 2), optional
        协方差矩阵 (如果未提供，则使用x_err, y_err, rho计算)
    x_err : float, optional
        X方向误差
    y_err : float, optional
        Y方向误差
    rho : float, optional
        X和Y的相关系数 (默认0)
    confidence : float, optional
        置信度 (默认 0.95)
    ax : matplotlib.axes.Axes, optional
        要绘制的轴 (默认当前轴)
    show_points : bool, optional
        是否显示散点 (默认False)
    show_center : bool, optional
        是否显示中心点 (默认False)
    **kwargs
        传递给Ellipse的额外参数
        
    返回：
    matplotlib.patches.Ellipse
    """
    if ax is None:
        ax = plt.gca()
        
    # 如果没有提供cov矩阵，根据x_err, y_err, rho计算
    if cov is None:
        if x_err is None or y_err is None:
            raise ValueError("必须提供cov矩阵或x_err和y_err")
        cov = np.array([
            [x_err**2, rho * x_err * y_err],
            [rho * x_err * y_err, y_err**2]
        ])
        
    # 计算特征值和特征向量
    vals, vecs = np.linalg.eigh(cov)
    
    # 计算角度
    x, y = vecs[:, 0]
    theta = np.degrees(np.arctan2(y, x))
    
    # 计算缩放因子
    scale = chi2.ppf(confidence, 2)
    
    # 计算宽度和高度
    width, height = 2 * np.sqrt(scale * vals)
    
    # 创建椭圆 - 先移除data和edgecolor参数
    ellipse_kwargs = kwargs.copy()
    for key in ['data', 'edgecolor']:
        if key in ellipse_kwargs:
            del ellipse_kwargs[key]
    
    # 修改椭圆创建代码段
    ellipse = Ellipse(xy=mean, width=width, height=height, 
                     angle=theta, 
                     edgecolor=kwargs.get('edgecolor', config.ELLIPSE_DEFAULT_COLOR),  # 设置颜色
                     **ellipse_kwargs)
    
    ax.add_patch(ellipse)
    
    # 绘制散点
    if show_points and 'data' in kwargs:
        ax.scatter(kwargs['data'][:, 0], kwargs['data'][:, 1], alpha=0.5)
    
    # 绘制中心点
    if show_center:
        ax.plot(mean[0], mean[1], 'ro')
    
    return ellipse

# 示例用法
if __name__ == "__main__":
    # 示例1：使用协方差矩阵
    np.random.seed(0)
    mean = [0, 0]
    cov = [[1, 0.8], [0.8, 1]]
    data = np.random.multivariate_normal(mean, cov, 1000)
    
    # 绘制
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    
    # 使用协方差矩阵绘制
    plot_error_ellipse(mean, cov=cov, 
                      confidence=0.95, 
                      edgecolor='red', 
                      facecolor='none',
                      ax=ax[0],
                      show_points=True,
                      show_center=True,
                      data=data)
    ax[0].set_title('使用协方差矩阵')
    
    # 示例2：使用x_err, y_err, rho参数
    x_err = 1.0
    y_err = 1.0
    rho = 0.8
    
    plot_error_ellipse(mean, x_err=x_err, y_err=y_err, rho=rho,
                      confidence=0.95, 
                      edgecolor='blue', 
                      facecolor='none',
                      ax=ax[1],
                      show_points=False,
                      show_center=True,
                      data=data)
    ax[1].set_title('使用x_err, y_err, rho参数')
    
    ax[0].set_aspect('equal')
    ax[1].set_aspect('equal')
    plt.show()
