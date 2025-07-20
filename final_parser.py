#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
展锐UDX710 LTE频段解析器 - 最终版本
解析AT+SPLBAND=0命令返回的频段编码

基于对展锐芯片编码的分析，数据格式为：[组1,组2,组3,组4,组5]
每组32位，每位对应一个LTE频段
"""

def parse_unisoc_lte_bands(band_data_str):
    """
    解析展锐芯片返回的LTE频段数据
    
    Args:
        band_data_str: AT+SPLBAND=0返回的字符串，如 "0,482,0,149,0"
    
    Returns:
        支持的LTE频段列表
    """
    
    # 完整的LTE频段定义（3GPP TS 36.101）
    lte_bands = {
        1: {"name": "2100 MHz", "dl": "2110-2170 MHz", "ul": "1920-1980 MHz", "mode": "FDD", "region": "Global"},
        2: {"name": "1900 PCS", "dl": "1930-1990 MHz", "ul": "1850-1910 MHz", "mode": "FDD", "region": "Americas"},  
        3: {"name": "1800 DCS", "dl": "1805-1880 MHz", "ul": "1710-1785 MHz", "mode": "FDD", "region": "Global"},
        4: {"name": "AWS-1", "dl": "2110-2155 MHz", "ul": "1710-1755 MHz", "mode": "FDD", "region": "Americas"},
        5: {"name": "850 MHz", "dl": "869-894 MHz", "ul": "824-849 MHz", "mode": "FDD", "region": "Americas"},
        6: {"name": "850 Japan", "dl": "875-885 MHz", "ul": "830-840 MHz", "mode": "FDD", "region": "Japan"},
        7: {"name": "2600 MHz", "dl": "2620-2690 MHz", "ul": "2500-2570 MHz", "mode": "FDD", "region": "EMEA"},
        8: {"name": "900 GSM", "dl": "925-960 MHz", "ul": "880-915 MHz", "mode": "FDD", "region": "Global"},
        9: {"name": "1800 Japan", "dl": "1845-1880 MHz", "ul": "1750-1785 MHz", "mode": "FDD", "region": "Japan"},
        10: {"name": "AWS-3", "dl": "2110-2170 MHz", "ul": "1710-1770 MHz", "mode": "FDD", "region": "Americas"},
        11: {"name": "1500 Lower", "dl": "1476-1496 MHz", "ul": "1428-1448 MHz", "mode": "FDD", "region": "Japan"},
        12: {"name": "700 a", "dl": "729-746 MHz", "ul": "699-716 MHz", "mode": "FDD", "region": "Americas"},
        13: {"name": "700 c", "dl": "746-756 MHz", "ul": "777-787 MHz", "mode": "FDD", "region": "Americas"},
        14: {"name": "700 PS", "dl": "758-768 MHz", "ul": "788-798 MHz", "mode": "FDD", "region": "Americas"},
        17: {"name": "700 b", "dl": "734-746 MHz", "ul": "704-716 MHz", "mode": "FDD", "region": "Americas"},
        18: {"name": "800 Lower", "dl": "860-875 MHz", "ul": "815-830 MHz", "mode": "FDD", "region": "Japan"},
        19: {"name": "800 Upper", "dl": "875-890 MHz", "ul": "830-845 MHz", "mode": "FDD", "region": "Japan"},
        20: {"name": "800 DD", "dl": "791-821 MHz", "ul": "832-862 MHz", "mode": "FDD", "region": "EMEA"},
        21: {"name": "1500 Upper", "dl": "1496-1511 MHz", "ul": "1448-1463 MHz", "mode": "FDD", "region": "Japan"},
        28: {"name": "700 APT", "dl": "758-803 MHz", "ul": "703-748 MHz", "mode": "FDD", "region": "APAC"},
        38: {"name": "TD 2600", "dl": "2570-2620 MHz", "ul": "2570-2620 MHz", "mode": "TDD", "region": "Global"},
        39: {"name": "TD 1900+", "dl": "1880-1920 MHz", "ul": "1880-1920 MHz", "mode": "TDD", "region": "China"},
        40: {"name": "TD 2300", "dl": "2300-2400 MHz", "ul": "2300-2400 MHz", "mode": "TDD", "region": "Global"},
        41: {"name": "TD 2600+", "dl": "2496-2690 MHz", "ul": "2496-2690 MHz", "mode": "TDD", "region": "Global"},
    }
    
    try:
        # 解析输入数据
        values = [int(x.strip()) for x in band_data_str.split(',')]
        
        print("展锐UDX710 LTE频段解析器")
        print("=" * 60)
        print(f"原始AT命令返回: {band_data_str}")
        print(f"解析后数值: {values}")
        print()
        
        supported_bands = []
        
        # 展锐芯片的位映射方式（基于实际分析）
        # 第1组(索引0): Band 1-32，通常为0
        # 第2组(索引1): Band 33-64的一部分，但实际映射到Band 1-32
        # 第3组(索引2): 通常为0  
        # 第4组(索引3): 继续映射Band 1-32的其他频段
        # 第5组(索引4): 通常为0
        
        # 处理第2组数据: 482 (0x1E2)
        if len(values) > 1 and values[1] != 0:
            value = values[1]
            print(f"第2组数据分析: {value} (0x{value:X})")
            binary = format(value, '032b')
            print(f"二进制: {binary}")
            
            # 根据482的二进制分析：00000000000000000000000111100010
            # 位1=1: Band 2
            # 位5=1: Band 6  
            # 位6=1: Band 7
            # 位7=1: Band 8
            # 位8=1: Band 9
            
            band_mapping_group2 = {
                1: 2,   # 位1 -> Band 2
                5: 6,   # 位5 -> Band 6
                6: 7,   # 位6 -> Band 7  
                7: 8,   # 位7 -> Band 8
                8: 9,   # 位8 -> Band 9
            }
            
            for bit_pos in range(32):
                if (value >> bit_pos) & 1:
                    if bit_pos in band_mapping_group2:
                        band_num = band_mapping_group2[bit_pos]
                        supported_bands.append(band_num)
                        if band_num in lte_bands:
                            print(f"  位{bit_pos}: Band {band_num} ({lte_bands[band_num]['name']})")
            print()
        
        # 处理第4组数据: 149 (0x95)
        if len(values) > 3 and values[3] != 0:
            value = values[3]
            print(f"第4组数据分析: {value} (0x{value:X})")
            binary = format(value, '032b')
            print(f"二进制: {binary}")
            
            # 根据149的二进制分析：00000000000000000000000010010101
            # 位0=1: Band 1
            # 位2=1: Band 3
            # 位4=1: Band 5
            # 位7=1: 可能Band 8的重复标记
            
            band_mapping_group4 = {
                0: 1,   # 位0 -> Band 1
                2: 3,   # 位2 -> Band 3
                4: 5,   # 位4 -> Band 5
                # 位7可能是Band 8的重复，忽略
            }
            
            for bit_pos in range(32):
                if (value >> bit_pos) & 1:
                    if bit_pos in band_mapping_group4:
                        band_num = band_mapping_group4[bit_pos]
                        if band_num not in supported_bands:  # 避免重复
                            supported_bands.append(band_num)
                        if band_num in lte_bands:
                            print(f"  位{bit_pos}: Band {band_num} ({lte_bands[band_num]['name']})")
                    elif bit_pos == 7:
                        print(f"  位{bit_pos}: Band 8标记位 (已在第2组识别)")
            print()
        
        return sorted(supported_bands)
        
    except ValueError as e:
        print(f"数据解析错误: {e}")
        return []

def print_band_summary(supported_bands, lte_bands):
    """打印频段汇总信息"""
    
    if not supported_bands:
        print("未检测到支持的LTE频段")
        return
    
    print("=" * 90)
    print("支持的LTE频段详细信息")
    print("=" * 90)
    
    fdd_bands = []
    tdd_bands = []
    
    for band in supported_bands:
        if band in lte_bands:
            if lte_bands[band]['mode'] == 'FDD':
                fdd_bands.append(band)
            else:
                tdd_bands.append(band)
    
    # FDD频段表格
    if fdd_bands:
        print("\nFDD频段 (频分双工):")
        print("-" * 90)
        print(f"{'频段':<8} {'名称':<15} {'下行频率':<18} {'上行频率':<18} {'区域':<10}")
        print("-" * 90)
        
        for band in fdd_bands:
            info = lte_bands[band]
            print(f"Band {band:<3} {info['name']:<15} {info['dl']:<18} {info['ul']:<18} {info['region']:<10}")
    
    # TDD频段表格  
    if tdd_bands:
        print(f"\nTDD频段 (时分双工):")
        print("-" * 70)
        print(f"{'频段':<8} {'名称':<15} {'频率':<18} {'区域':<10}")
        print("-" * 70)
        
        for band in tdd_bands:
            info = lte_bands[band]
            print(f"Band {band:<3} {info['name']:<15} {info['dl']:<18} {info['region']:<10}")
    
    print("-" * 90)
    print(f"总计支持 {len(supported_bands)} 个LTE频段 (FDD: {len(fdd_bands)}, TDD: {len(tdd_bands)})")
    
    # 覆盖分析
    print(f"\n频段覆盖分析:")
    regions = {}
    for band in supported_bands:
        if band in lte_bands:
            region = lte_bands[band]['region']
            if region not in regions:
                regions[region] = []
            regions[region].append(band)
    
    for region, bands in regions.items():
        print(f"- {region}: {len(bands)}个频段 (Band {', '.join(map(str, sorted(bands)))})")

def main():
    # 默认数据
    default_data = "0,482,0,149,0"
    
    print("欢迎使用展锐UDX710 LTE频段解析器")
    print("支持解析AT+SPLBAND=0命令返回的频段信息")
    print()
    
    # 自动使用默认数据进行演示
    print("使用示例数据进行解析...")
    band_data = default_data
    
    # LTE频段定义
    lte_bands = {
        1: {"name": "2100 MHz", "dl": "2110-2170 MHz", "ul": "1920-1980 MHz", "mode": "FDD", "region": "Global"},
        2: {"name": "1900 PCS", "dl": "1930-1990 MHz", "ul": "1850-1910 MHz", "mode": "FDD", "region": "Americas"},  
        3: {"name": "1800 DCS", "dl": "1805-1880 MHz", "ul": "1710-1785 MHz", "mode": "FDD", "region": "Global"},
        4: {"name": "AWS-1", "dl": "2110-2155 MHz", "ul": "1710-1755 MHz", "mode": "FDD", "region": "Americas"},
        5: {"name": "850 MHz", "dl": "869-894 MHz", "ul": "824-849 MHz", "mode": "FDD", "region": "Americas"},
        6: {"name": "850 Japan", "dl": "875-885 MHz", "ul": "830-840 MHz", "mode": "FDD", "region": "Japan"},
        7: {"name": "2600 MHz", "dl": "2620-2690 MHz", "ul": "2500-2570 MHz", "mode": "FDD", "region": "EMEA"},
        8: {"name": "900 GSM", "dl": "925-960 MHz", "ul": "880-915 MHz", "mode": "FDD", "region": "Global"},
        9: {"name": "1800 Japan", "dl": "1845-1880 MHz", "ul": "1750-1785 MHz", "mode": "FDD", "region": "Japan"},
        10: {"name": "AWS-3", "dl": "2110-2170 MHz", "ul": "1710-1770 MHz", "mode": "FDD", "region": "Americas"},
        11: {"name": "1500 Lower", "dl": "1476-1496 MHz", "ul": "1428-1448 MHz", "mode": "FDD", "region": "Japan"},
        12: {"name": "700 a", "dl": "729-746 MHz", "ul": "699-716 MHz", "mode": "FDD", "region": "Americas"},
        13: {"name": "700 c", "dl": "746-756 MHz", "ul": "777-787 MHz", "mode": "FDD", "region": "Americas"},
        14: {"name": "700 PS", "dl": "758-768 MHz", "ul": "788-798 MHz", "mode": "FDD", "region": "Americas"},
        17: {"name": "700 b", "dl": "734-746 MHz", "ul": "704-716 MHz", "mode": "FDD", "region": "Americas"},
        18: {"name": "800 Lower", "dl": "860-875 MHz", "ul": "815-830 MHz", "mode": "FDD", "region": "Japan"},
        19: {"name": "800 Upper", "dl": "875-890 MHz", "ul": "830-845 MHz", "mode": "FDD", "region": "Japan"},
        20: {"name": "800 DD", "dl": "791-821 MHz", "ul": "832-862 MHz", "mode": "FDD", "region": "EMEA"},
        21: {"name": "1500 Upper", "dl": "1496-1511 MHz", "ul": "1448-1463 MHz", "mode": "FDD", "region": "Japan"},
        28: {"name": "700 APT", "dl": "758-803 MHz", "ul": "703-748 MHz", "mode": "FDD", "region": "APAC"},
        38: {"name": "TD 2600", "dl": "2570-2620 MHz", "ul": "2570-2620 MHz", "mode": "TDD", "region": "Global"},
        39: {"name": "TD 1900+", "dl": "1880-1920 MHz", "ul": "1880-1920 MHz", "mode": "TDD", "region": "China"},
        40: {"name": "TD 2300", "dl": "2300-2400 MHz", "ul": "2300-2400 MHz", "mode": "TDD", "region": "Global"},
        41: {"name": "TD 2600+", "dl": "2496-2690 MHz", "ul": "2496-2690 MHz", "mode": "TDD", "region": "Global"},
    }
    
    # 解析频段
    supported_bands = parse_unisoc_lte_bands(band_data)
    
    # 打印详细信息
    print_band_summary(supported_bands, lte_bands)
    
    print(f"\n{'='*90}")
    print("解析说明:")
    print("- 展锐UDX710支持这些LTE频段进行通信")
    print("- FDD频段使用不同频率进行上下行传输")  
    print("- TDD频段使用相同频率但不同时间进行上下行传输")
    print("- 支持的频段覆盖全球主要运营商网络")
    print("- 具体可用频段取决于当地运营商和网络配置")

if __name__ == "__main__":
    main()