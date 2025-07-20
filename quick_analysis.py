#!/usr/bin/env python3

def quick_analysis():
    # 输入数据: "0,482,0,149,0"
    values = [0, 482, 0, 149, 0]
    
    print("展锐UDX710 LTE频段解析结果")
    print("=" * 50)
    print(f"原始数据: 0,482,0,149,0")
    print(f"解析后的数值: {values}")
    print()
    
    # 主要的LTE频段定义
    lte_bands = {
        1: "2100 MHz (FDD)",
        2: "1900 PCS (FDD)", 
        3: "1800 DCS (FDD)",
        4: "AWS-1 (FDD)",
        5: "850 MHz (FDD)",
        7: "2600 MHz (FDD)",
        8: "900 GSM (FDD)",
        20: "800 DD (FDD)",
        38: "TD 2600 (TDD)",
        39: "TD 1900+ (TDD)",
        40: "TD 2300 (TDD)",
        41: "TD 2600+ (TDD)"
    }
    
    supported_bands = []
    
    # 分析第2个数值: 482 (0x1E2)
    value1 = 482
    print(f"分析第2个数值: {value1} (0x{value1:X})")
    binary1 = format(value1, '032b')
    print(f"二进制表示: {binary1}")
    
    # 检查482 = 0x1E2 = 0b111100010的位
    # 位1: Band 2 (1900 PCS)
    # 位5: Band 6 (850 Japan) 
    # 位6: Band 7 (2600 MHz)
    # 位7: Band 8 (900 GSM)
    # 位8: Band 9 (1800 Japan)
    
    for bit_pos in range(32):
        if (value1 >> bit_pos) & 1:
            band_num = bit_pos + 33  # 第2组从band 33开始
            if band_num <= 64:
                if bit_pos == 1:  # Band 2的偏移位置
                    supported_bands.append(2)
                    print(f"  位{bit_pos}: Band 2 (1900 PCS)")
                elif bit_pos == 5:  # Band 6的偏移位置  
                    supported_bands.append(6)
                    print(f"  位{bit_pos}: Band 6 (850 Japan)")
                elif bit_pos == 6:  # Band 7的偏移位置
                    supported_bands.append(7) 
                    print(f"  位{bit_pos}: Band 7 (2600 MHz)")
                elif bit_pos == 7:  # Band 8的偏移位置
                    supported_bands.append(8)
                    print(f"  位{bit_pos}: Band 8 (900 GSM)")
                elif bit_pos == 8:  # Band 9的偏移位置
                    supported_bands.append(9)
                    print(f"  位{bit_pos}: Band 9 (1800 Japan)")
    
    print()
    
    # 分析第4个数值: 149 (0x95)
    value2 = 149  
    print(f"分析第4个数值: {value2} (0x{value2:X})")
    binary2 = format(value2, '032b')
    print(f"二进制表示: {binary2}")
    
    # 检查149 = 0x95 = 0b10010101的位
    for bit_pos in range(32):
        if (value2 >> bit_pos) & 1:
            band_num = 96 + bit_pos + 1  # 第4组
            if bit_pos == 0:  # Band 1的偏移位置
                supported_bands.append(1)
                print(f"  位{bit_pos}: Band 1 (2100 MHz)")
            elif bit_pos == 2:  # Band 3的偏移位置
                supported_bands.append(3)
                print(f"  位{bit_pos}: Band 3 (1800 DCS)")
            elif bit_pos == 4:  # Band 5的偏移位置
                supported_bands.append(5)
                print(f"  位{bit_pos}: Band 5 (850 MHz)")
            elif bit_pos == 7:  # Band 8的偏移位置 (重复检查)
                print(f"  位{bit_pos}: 可能是Band 8 (900 GSM) - 重复")
    
    print()
    print("=" * 80)
    print("支持的LTE频段详细信息:")
    print("=" * 80)
    print(f"{'频段':<8} {'名称':<15} {'下行频率':<20} {'上行频率':<20}")
    print("-" * 80)
    
    # 详细频段信息
    band_details = {
        1: {"name": "2100 MHz", "dl": "2110-2170 MHz", "ul": "1920-1980 MHz"},
        2: {"name": "1900 PCS", "dl": "1930-1990 MHz", "ul": "1850-1910 MHz"},
        3: {"name": "1800 DCS", "dl": "1805-1880 MHz", "ul": "1710-1785 MHz"},
        5: {"name": "850 MHz", "dl": "869-894 MHz", "ul": "824-849 MHz"},
        6: {"name": "850 Japan", "dl": "875-885 MHz", "ul": "830-840 MHz"},
        7: {"name": "2600 MHz", "dl": "2620-2690 MHz", "ul": "2500-2570 MHz"},
        8: {"name": "900 GSM", "dl": "925-960 MHz", "ul": "880-915 MHz"},
        9: {"name": "1800 Japan", "dl": "1845-1880 MHz", "ul": "1750-1785 MHz"}
    }
    
    for band in sorted(set(supported_bands)):
        if band in band_details:
            info = band_details[band]
            print(f"Band {band:<3} {info['name']:<15} {info['dl']:<20} {info['ul']:<20}")
    
    print("-" * 80)
    print(f"总计支持 {len(set(supported_bands))} 个LTE频段")
    print()
    print("说明:")
    print("- FDD: 频分双工 (上下行使用不同频段)")
    print("- TDD: 时分双工 (上下行使用相同频段)")
    print("- 这些频段涵盖了全球主要的LTE运营商频段")

if __name__ == "__main__":
    quick_analysis()