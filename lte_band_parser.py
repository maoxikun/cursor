#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
展锐UDX710 LTE频段解析器
解析AT+SPLBAND=0命令返回的频段编码

作者: AI Assistant  
日期: 2025-01-11
"""

def parse_lte_bands(band_data):
    """
    解析展锐芯片返回的LTE频段数据
    
    Args:
        band_data: 字符串格式的频段数据，如 "0,482,0,149,0"
    
    Returns:
        支持的LTE频段列表
    """
    
    # LTE频段定义 (基于3GPP标准)
    lte_bands = {
        1: {"name": "2100 MHz", "dl": "2110-2170 MHz", "ul": "1920-1980 MHz", "mode": "FDD"},
        2: {"name": "1900 PCS", "dl": "1930-1990 MHz", "ul": "1850-1910 MHz", "mode": "FDD"},
        3: {"name": "1800 DCS", "dl": "1805-1880 MHz", "ul": "1710-1785 MHz", "mode": "FDD"},
        4: {"name": "AWS-1", "dl": "2110-2155 MHz", "ul": "1710-1755 MHz", "mode": "FDD"},
        5: {"name": "850 MHz", "dl": "869-894 MHz", "ul": "824-849 MHz", "mode": "FDD"},
        6: {"name": "850 Japan", "dl": "875-885 MHz", "ul": "830-840 MHz", "mode": "FDD"},
        7: {"name": "2600 MHz", "dl": "2620-2690 MHz", "ul": "2500-2570 MHz", "mode": "FDD"},
        8: {"name": "900 GSM", "dl": "925-960 MHz", "ul": "880-915 MHz", "mode": "FDD"},
        9: {"name": "1800 Japan", "dl": "1844.9-1879.9 MHz", "ul": "1749.9-1784.9 MHz", "mode": "FDD"},
        10: {"name": "AWS-3", "dl": "2110-2170 MHz", "ul": "1710-1770 MHz", "mode": "FDD"},
        11: {"name": "1500 Lower", "dl": "1475.9-1495.9 MHz", "ul": "1427.9-1447.9 MHz", "mode": "FDD"},
        12: {"name": "700 a", "dl": "729-746 MHz", "ul": "699-716 MHz", "mode": "FDD"},
        13: {"name": "700 c", "dl": "746-756 MHz", "ul": "777-787 MHz", "mode": "FDD"},
        14: {"name": "700 PS", "dl": "758-768 MHz", "ul": "788-798 MHz", "mode": "FDD"},
        17: {"name": "700 b", "dl": "734-746 MHz", "ul": "704-716 MHz", "mode": "FDD"},
        18: {"name": "800 Lower", "dl": "860-875 MHz", "ul": "815-830 MHz", "mode": "FDD"},
        19: {"name": "800 Upper", "dl": "875-890 MHz", "ul": "830-845 MHz", "mode": "FDD"},
        20: {"name": "800 DD", "dl": "791-821 MHz", "ul": "832-862 MHz", "mode": "FDD"},
        21: {"name": "1500 Upper", "dl": "1495.9-1510.9 MHz", "ul": "1447.9-1462.9 MHz", "mode": "FDD"},
        22: {"name": "3500 MHz", "dl": "3510-3590 MHz", "ul": "3410-3490 MHz", "mode": "FDD"},
        23: {"name": "2000 S-band", "dl": "2180-2200 MHz", "ul": "2000-2020 MHz", "mode": "FDD"},
        24: {"name": "1600 L-band", "dl": "1525-1559 MHz", "ul": "1626.5-1660.5 MHz", "mode": "FDD"},
        25: {"name": "1900+", "dl": "1930-1995 MHz", "ul": "1850-1915 MHz", "mode": "FDD"},
        26: {"name": "850+", "dl": "859-894 MHz", "ul": "814-849 MHz", "mode": "FDD"},
        27: {"name": "800 SMR", "dl": "852-869 MHz", "ul": "807-824 MHz", "mode": "FDD"},
        28: {"name": "700 APT", "dl": "758-803 MHz", "ul": "703-748 MHz", "mode": "FDD"},
        29: {"name": "700 d", "dl": "717-728 MHz", "ul": "N/A", "mode": "SDL"},
        30: {"name": "2300 WCS", "dl": "2350-2360 MHz", "ul": "2305-2315 MHz", "mode": "FDD"},
        31: {"name": "450 MHz", "dl": "462.5-467.5 MHz", "ul": "452.5-457.5 MHz", "mode": "FDD"},
        32: {"name": "1500 L-band", "dl": "1452-1496 MHz", "ul": "N/A", "mode": "SDL"},
        33: {"name": "TD 1900", "dl": "1900-1920 MHz", "ul": "1900-1920 MHz", "mode": "TDD"},
        34: {"name": "TD 2000", "dl": "2010-2025 MHz", "ul": "2010-2025 MHz", "mode": "TDD"},
        35: {"name": "TD PCS Lower", "dl": "1850-1910 MHz", "ul": "1850-1910 MHz", "mode": "TDD"},
        36: {"name": "TD PCS Upper", "dl": "1930-1990 MHz", "ul": "1930-1990 MHz", "mode": "TDD"},
        37: {"name": "TD PCS Center", "dl": "1910-1930 MHz", "ul": "1910-1930 MHz", "mode": "TDD"},
        38: {"name": "TD 2600", "dl": "2570-2620 MHz", "ul": "2570-2620 MHz", "mode": "TDD"},
        39: {"name": "TD 1900+", "dl": "1880-1920 MHz", "ul": "1880-1920 MHz", "mode": "TDD"},
        40: {"name": "TD 2300", "dl": "2300-2400 MHz", "ul": "2300-2400 MHz", "mode": "TDD"},
        41: {"name": "TD 2600+", "dl": "2496-2690 MHz", "ul": "2496-2690 MHz", "mode": "TDD"},
        42: {"name": "TD 3500", "dl": "3400-3600 MHz", "ul": "3400-3600 MHz", "mode": "TDD"},
        43: {"name": "TD 3700", "dl": "3600-3800 MHz", "ul": "3600-3800 MHz", "mode": "TDD"},
        44: {"name": "TD 700", "dl": "703-803 MHz", "ul": "703-803 MHz", "mode": "TDD"},
        45: {"name": "TD 1500", "dl": "1447-1467 MHz", "ul": "1447-1467 MHz", "mode": "TDD"},
        46: {"name": "TD Unlicensed", "dl": "5150-5925 MHz", "ul": "5150-5925 MHz", "mode": "TDD"},
        47: {"name": "TD V2X", "dl": "5855-5925 MHz", "ul": "5855-5925 MHz", "mode": "TDD"},
        48: {"name": "TD 3600", "dl": "3550-3700 MHz", "ul": "3550-3700 MHz", "mode": "TDD"},
        65: {"name": "2100+", "dl": "2110-2200 MHz", "ul": "1920-2010 MHz", "mode": "FDD"},
        66: {"name": "AWS", "dl": "2110-2200 MHz", "ul": "1710-1780 MHz", "mode": "FDD"},
        67: {"name": "700 EU", "dl": "738-758 MHz", "ul": "N/A", "mode": "SDL"},
        68: {"name": "700 ME", "dl": "753-783 MHz", "ul": "698-728 MHz", "mode": "FDD"},
        69: {"name": "DL b38", "dl": "2570-2620 MHz", "ul": "N/A", "mode": "SDL"},
        70: {"name": "AWS-4", "dl": "1995-2020 MHz", "ul": "1695-1710 MHz", "mode": "FDD"},
        71: {"name": "600 MHz", "dl": "617-652 MHz", "ul": "663-698 MHz", "mode": "FDD"},
        72: {"name": "450 PMR/PAMR", "dl": "461-466 MHz", "ul": "451-456 MHz", "mode": "FDD"},
        73: {"name": "450 APAC", "dl": "460-465 MHz", "ul": "450-455 MHz", "mode": "FDD"},
        74: {"name": "L-band", "dl": "1475-1518 MHz", "ul": "1427-1470 MHz", "mode": "FDD"},
        75: {"name": "DL b50", "dl": "1432-1517 MHz", "ul": "N/A", "mode": "SDL"},
        76: {"name": "DL b51", "dl": "1427-1432 MHz", "ul": "N/A", "mode": "SDL"},
        85: {"name": "700 a+", "dl": "728-746 MHz", "ul": "698-716 MHz", "mode": "FDD"},
    }
    
    try:
        # 解析输入数据
        values = [int(x.strip()) for x in band_data.split(',')]
        print(f"原始数据: {band_data}")
        print(f"解析后的数值: {values}")
        print()
        
        supported_bands = []
        
        # 处理每个数值 (假设这些是十六进制表示)
        for i, value in enumerate(values):
            if value == 0:
                continue
                
            print(f"分析第{i+1}个数值: {value} (0x{value:X})")
            
            # 将数值转换为二进制，分析每个位
            binary = format(value, '032b')
            print(f"二进制表示: {binary}")
            
            # 检查每个位，位置对应频段编号
            for bit_pos in range(32):
                if (value >> bit_pos) & 1:
                    # 计算频段编号
                    band_num = i * 32 + bit_pos + 1
                    
                    if band_num in lte_bands:
                        supported_bands.append(band_num)
                        print(f"  位{bit_pos}: Band {band_num} ({lte_bands[band_num]['name']})")
            print()
        
        return supported_bands
        
    except ValueError as e:
        print(f"数据解析错误: {e}")
        return []

def print_band_details(band_numbers, lte_bands):
    """打印频段详细信息"""
    if not band_numbers:
        print("未检测到支持的LTE频段")
        return
    
    print("=" * 80)
    print("支持的LTE频段详细信息:")
    print("=" * 80)
    print(f"{'频段':<8} {'名称':<15} {'模式':<6} {'下行频率':<20} {'上行频率':<20}")
    print("-" * 80)
    
    for band in sorted(band_numbers):
        if band in lte_bands:
            info = lte_bands[band]
            print(f"Band {band:<3} {info['name']:<15} {info['mode']:<6} {info['dl']:<20} {info['ul']:<20}")
    
    print("-" * 80)
    print(f"总计支持 {len(band_numbers)} 个LTE频段")

def main():
    print("展锐UDX710 LTE频段解析器")
    print("=" * 50)
    
    # 默认数据
    default_data = "0,482,0,149,0"
    
    # 获取用户输入
    user_input = input(f"请输入AT+SPLBAND=0返回的数据 (默认: {default_data}): ").strip()
    
    if not user_input:
        user_input = default_data
    
    print()
    
    # 解析频段
    supported_bands = parse_lte_bands(user_input)
    
    # LTE频段定义
    lte_bands = {
        1: {"name": "2100 MHz", "dl": "2110-2170 MHz", "ul": "1920-1980 MHz", "mode": "FDD"},
        2: {"name": "1900 PCS", "dl": "1930-1990 MHz", "ul": "1850-1910 MHz", "mode": "FDD"},
        3: {"name": "1800 DCS", "dl": "1805-1880 MHz", "ul": "1710-1785 MHz", "mode": "FDD"},
        4: {"name": "AWS-1", "dl": "2110-2155 MHz", "ul": "1710-1755 MHz", "mode": "FDD"},
        5: {"name": "850 MHz", "dl": "869-894 MHz", "ul": "824-849 MHz", "mode": "FDD"},
        6: {"name": "850 Japan", "dl": "875-885 MHz", "ul": "830-840 MHz", "mode": "FDD"},
        7: {"name": "2600 MHz", "dl": "2620-2690 MHz", "ul": "2500-2570 MHz", "mode": "FDD"},
        8: {"name": "900 GSM", "dl": "925-960 MHz", "ul": "880-915 MHz", "mode": "FDD"},
        9: {"name": "1800 Japan", "dl": "1844.9-1879.9 MHz", "ul": "1749.9-1784.9 MHz", "mode": "FDD"},
        10: {"name": "AWS-3", "dl": "2110-2170 MHz", "ul": "1710-1770 MHz", "mode": "FDD"},
        11: {"name": "1500 Lower", "dl": "1475.9-1495.9 MHz", "ul": "1427.9-1447.9 MHz", "mode": "FDD"},
        12: {"name": "700 a", "dl": "729-746 MHz", "ul": "699-716 MHz", "mode": "FDD"},
        13: {"name": "700 c", "dl": "746-756 MHz", "ul": "777-787 MHz", "mode": "FDD"},
        14: {"name": "700 PS", "dl": "758-768 MHz", "ul": "788-798 MHz", "mode": "FDD"},
        17: {"name": "700 b", "dl": "734-746 MHz", "ul": "704-716 MHz", "mode": "FDD"},
        18: {"name": "800 Lower", "dl": "860-875 MHz", "ul": "815-830 MHz", "mode": "FDD"},
        19: {"name": "800 Upper", "dl": "875-890 MHz", "ul": "830-845 MHz", "mode": "FDD"},
        20: {"name": "800 DD", "dl": "791-821 MHz", "ul": "832-862 MHz", "mode": "FDD"},
        21: {"name": "1500 Upper", "dl": "1495.9-1510.9 MHz", "ul": "1447.9-1462.9 MHz", "mode": "FDD"},
        22: {"name": "3500 MHz", "dl": "3510-3590 MHz", "ul": "3410-3490 MHz", "mode": "FDD"},
        23: {"name": "2000 S-band", "dl": "2180-2200 MHz", "ul": "2000-2020 MHz", "mode": "FDD"},
        24: {"name": "1600 L-band", "dl": "1525-1559 MHz", "ul": "1626.5-1660.5 MHz", "mode": "FDD"},
        25: {"name": "1900+", "dl": "1930-1995 MHz", "ul": "1850-1915 MHz", "mode": "FDD"},
        26: {"name": "850+", "dl": "859-894 MHz", "ul": "814-849 MHz", "mode": "FDD"},
        27: {"name": "800 SMR", "dl": "852-869 MHz", "ul": "807-824 MHz", "mode": "FDD"},
        28: {"name": "700 APT", "dl": "758-803 MHz", "ul": "703-748 MHz", "mode": "FDD"},
        29: {"name": "700 d", "dl": "717-728 MHz", "ul": "N/A", "mode": "SDL"},
        30: {"name": "2300 WCS", "dl": "2350-2360 MHz", "ul": "2305-2315 MHz", "mode": "FDD"},
        31: {"name": "450 MHz", "dl": "462.5-467.5 MHz", "ul": "452.5-457.5 MHz", "mode": "FDD"},
        32: {"name": "1500 L-band", "dl": "1452-1496 MHz", "ul": "N/A", "mode": "SDL"},
        33: {"name": "TD 1900", "dl": "1900-1920 MHz", "ul": "1900-1920 MHz", "mode": "TDD"},
        34: {"name": "TD 2000", "dl": "2010-2025 MHz", "ul": "2010-2025 MHz", "mode": "TDD"},
        35: {"name": "TD PCS Lower", "dl": "1850-1910 MHz", "ul": "1850-1910 MHz", "mode": "TDD"},
        36: {"name": "TD PCS Upper", "dl": "1930-1990 MHz", "ul": "1930-1990 MHz", "mode": "TDD"},
        37: {"name": "TD PCS Center", "dl": "1910-1930 MHz", "ul": "1910-1930 MHz", "mode": "TDD"},
        38: {"name": "TD 2600", "dl": "2570-2620 MHz", "ul": "2570-2620 MHz", "mode": "TDD"},
        39: {"name": "TD 1900+", "dl": "1880-1920 MHz", "ul": "1880-1920 MHz", "mode": "TDD"},
        40: {"name": "TD 2300", "dl": "2300-2400 MHz", "ul": "2300-2400 MHz", "mode": "TDD"},
        41: {"name": "TD 2600+", "dl": "2496-2690 MHz", "ul": "2496-2690 MHz", "mode": "TDD"},
        42: {"name": "TD 3500", "dl": "3400-3600 MHz", "ul": "3400-3600 MHz", "mode": "TDD"},
        43: {"name": "TD 3700", "dl": "3600-3800 MHz", "ul": "3600-3800 MHz", "mode": "TDD"},
        44: {"name": "TD 700", "dl": "703-803 MHz", "ul": "703-803 MHz", "mode": "TDD"},
        45: {"name": "TD 1500", "dl": "1447-1467 MHz", "ul": "1447-1467 MHz", "mode": "TDD"},
        46: {"name": "TD Unlicensed", "dl": "5150-5925 MHz", "ul": "5150-5925 MHz", "mode": "TDD"},
        47: {"name": "TD V2X", "dl": "5855-5925 MHz", "ul": "5855-5925 MHz", "mode": "TDD"},
        48: {"name": "TD 3600", "dl": "3550-3700 MHz", "ul": "3550-3700 MHz", "mode": "TDD"},
        65: {"name": "2100+", "dl": "2110-2200 MHz", "ul": "1920-2010 MHz", "mode": "FDD"},
        66: {"name": "AWS", "dl": "2110-2200 MHz", "ul": "1710-1780 MHz", "mode": "FDD"},
        67: {"name": "700 EU", "dl": "738-758 MHz", "ul": "N/A", "mode": "SDL"},
        68: {"name": "700 ME", "dl": "753-783 MHz", "ul": "698-728 MHz", "mode": "FDD"},
        69: {"name": "DL b38", "dl": "2570-2620 MHz", "ul": "N/A", "mode": "SDL"},
        70: {"name": "AWS-4", "dl": "1995-2020 MHz", "ul": "1695-1710 MHz", "mode": "FDD"},
        71: {"name": "600 MHz", "dl": "617-652 MHz", "ul": "663-698 MHz", "mode": "FDD"},
        72: {"name": "450 PMR/PAMR", "dl": "461-466 MHz", "ul": "451-456 MHz", "mode": "FDD"},
        73: {"name": "450 APAC", "dl": "460-465 MHz", "ul": "450-455 MHz", "mode": "FDD"},
        74: {"name": "L-band", "dl": "1475-1518 MHz", "ul": "1427-1470 MHz", "mode": "FDD"},
        75: {"name": "DL b50", "dl": "1432-1517 MHz", "ul": "N/A", "mode": "SDL"},
        76: {"name": "DL b51", "dl": "1427-1432 MHz", "ul": "N/A", "mode": "SDL"},
        85: {"name": "700 a+", "dl": "728-746 MHz", "ul": "698-716 MHz", "mode": "FDD"},
    }
    
    # 打印详细信息
    print_band_details(supported_bands, lte_bands)

if __name__ == "__main__":
    main()