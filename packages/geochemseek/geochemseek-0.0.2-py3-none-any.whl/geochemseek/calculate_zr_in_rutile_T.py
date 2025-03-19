import numpy as np


def calculate_zr_in_rutile_T(
    zr_ppm: np.ndarray, 
    pressure_kbar: float = 10, 
    mode: str = "tomkins_alpha"
) -> np.ndarray:
    """根据金红石中Zr含量计算形成温度

    Args:
        zr_ppm (np.ndarray): 金红石中Zr含量(ppm)，支持标量或数组输入
        pressure_kbar (float): 压力值(单位kbar)，需大于0
        mode (str, optional): 温度计模型，可选['tomkins_alpha', 'watson', 'zack']，默认tomkins_alpha

    Returns:
        np.ndarray: 温度值数组(单位°C)，与输入zr_ppm维度一致

    Raises:
        ValueError: 当输入参数不合法时抛出
        TypeError: 当输入类型错误时抛出

    References:
        - Tomkins, H.S., Powell, R., Ellis, D.J., 2007. The pressure dependence of the zirconium-in-rutile thermometer. Journal of Metamorphic Geology 25, 703-713.
        - Watson, E.B., Wark, D.A., Thomas, J.B., 2006. Crystallization thermometers for zircon and rutile. Contributions to Mineralogy and Petrology 151, 413-433.
        - Zack, T., Moraes, R., Kronz, A., 2004. Temperature dependence of Zr in rutile: empirical calibration of a rutile thermometer. Contributions to Mineralogy and Petrology 148, 471-488.

    Examples:
        >>> calculate_zr_temperature(np.array([20, 50]), 10)
        array([...])
    """
    # 参数校验
    if not isinstance(zr_ppm, np.ndarray):
        raise TypeError("zr_ppm必须为numpy数组")
    if np.any(zr_ppm <= 0):
        raise ValueError("Zr含量必须为正值（单位：ppm）")
    if pressure_kbar <= 0:
        raise ValueError("压力值必须大于0（单位：kbar）")
    if mode.lower() not in ("tomkins_alpha", "watson", "zack"):
        raise ValueError(f"不支持的模型: {mode}，可选模型为tomkins/watson/zack")

    gas_constant = 0.0083144  # 气体常数 (kJ/mol/K)
    valid_zr = np.where(zr_ppm > 0, zr_ppm, np.nan)
    
    if mode.lower() == "watson":
        temperature = 4470 / (7.36 - np.log10(valid_zr)) - 273
    elif mode.lower() == "zack":
        temperature = 134.7 * np.log(valid_zr) - 25
    else:  # Tomkins α石英模型
        temperature = (
            (83.9 + 0.410 * pressure_kbar) 
            / (0.1428 - gas_constant * np.log(valid_zr))
            - 273
        )
    
    return temperature
