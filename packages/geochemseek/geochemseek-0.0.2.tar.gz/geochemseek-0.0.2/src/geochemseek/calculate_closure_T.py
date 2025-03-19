import numpy as np
import matplotlib.pyplot as plt

def calculate_closure_T(
    a_um: np.ndarray,
    cooling_rates_Ma: np.ndarray,
    A: float,
    E: float,
    D0_cm2s: float
) -> np.ndarray:
    """
    计算矿物闭合温度矩阵（基于Dodson方程）
    
    参数:
    a_um (np.ndarray): 扩散域特征尺寸数组，范围建议1-10000微米
    cooling_rates_Ma (np.ndarray): 冷却速率数组，单位：摄氏度/百万年（°C/Ma）
    A (float): 几何形状常数（默认27对应柱状晶体扩散模型，55对应球体模型，8.7对应平板模型）
    E (float): 活化能，单位：焦耳/摩尔（J/mol）
    D0_cm2s (float): 指前因子扩散系数，单位：平方厘米/秒（cm²/s）
    
    返回:
    np.ndarray: 闭合温度矩阵（单位：°C），矩阵尺寸为(len(a_um), len(cooling_rates_Ma))
    
    计算公式：
    T_c = E / [R * ln(A * D0 * τ / a²)]
    其中：
    - τ = (R*T²)/(E*q) 为特征时间常数
    - q 为冷却速率（转换单位后的°C/s）
    
    示例：
    >>> a = np.arange(1, 10001)
    >>> rates = np.array([10, 100])
    >>> T_matrix = calculate_closure_T(a, rates, A=27, E=228e3, D0_cm2s=np.exp(-8.97))
    """
    
    gas_constant: float = 8.314  #  气体常数：J/(mol·K)
    # 单位转换
    a_m = a_um * 1e-6  # 微米转米
    cooling_rates = cooling_rates_Ma / (1e6 * 31557600)  # °C/Ma转°C/s
    
    # 计算扩散系数
    D0 = D0_cm2s * 1e-4  # cm²/s转m²/s
    
    # 初始化结果矩阵
    Tc_matrix = np.zeros((len(a_m), len(cooling_rates)))
    
    # 主计算循环
    for cr_idx, q in enumerate(cooling_rates):
        for a_idx, a_current in enumerate(a_m):
            Tc_guess_K = 800  # 初始猜测温度（开尔文）
            
            for _ in range(100):
                tau = (gas_constant * Tc_guess_K**2) / (E * q)
                term = (A * D0 * tau) / (a_current**2)
                
                try:
                    Tc_new_K = E / (gas_constant * np.log(term))
                except:
                    Tc_new_K = np.nan
                    break
                
                if not np.isnan(Tc_new_K) and abs(Tc_new_K - Tc_guess_K) < 0.01:
                    break
                Tc_guess_K = Tc_new_K
            
            Tc_matrix[a_idx, cr_idx] = Tc_guess_K - 273.15  # 转摄氏度
    
    return Tc_matrix

def plot_closure_T(a_um: np.ndarray, Tc_matrix: np.ndarray, cooling_rates_Ma: np.ndarray):
    """
    绘制闭合温度-扩散尺寸关系曲线
    
    参数:
    a_um (np.ndarray): 扩散域特征尺寸数组（单位：微米）
    Tc_matrix (np.ndarray): 由calculate_closure_T生成的温度矩阵，形状需与a_um匹配
    cooling_rates_Ma (np.ndarray): 冷却速率数组（单位：°C/Ma）
    
    图形特性：
    - 半对数坐标（x轴对数刻度）
    - 坐标范围：x轴1-10^4 μm，y轴200-1000°C
    - 使用Arial字体，8pt字号
    - 包含图例说明和网格线
    - 紧凑布局（tight_layout）
    """
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial']
    
    fig, ax = plt.subplots(figsize=(3.5, 4))
    
    for i in range(len(cooling_rates_Ma)):
        ax.semilogx(a_um, Tc_matrix[:, i], label=f'{cooling_rates_Ma[i]} °C/Ma')
    
    ax.set_xlim(1, 10000)
    ax.set_ylim(200, 1000)
    ax.set_xlabel('Characteristic diffusion size (μm)', fontsize=8)
    ax.set_ylabel('Closure temperature (°C)', fontsize=8)
    ax.tick_params(axis='both', labelsize=8)
    ax.legend(loc='lower right', fontsize=8)
    ax.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # 测试参数设置
    a_um = np.arange(1, 10001)  # 1-10000微米
    cooling_rates_Ma = np.array([10, 20, 50, 100, 200])  # °C/Ma
    
    # 计算闭合温度
    Tc_matrix = calculate_closure_T(a_um, cooling_rates_Ma, A=27, E=228e3, D0_cm2s=np.exp(-8.97))
    
    # 绘制结果
    plot_closure_T(a_um, Tc_matrix, cooling_rates_Ma)
