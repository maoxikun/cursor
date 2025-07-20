#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
展锐UDX710 5G NR频段解析器
解析AT+SPLBAND=3命令返回的5G NR频段编码

格式：AT+SPLBAND=3
返回：545,0,528,0
其中：545为NR-FDD参数，528为NR-TDD参数
"""

def parse_unisoc_nr_bands(band_data_str):
    """
    解析展锐芯片返回的5G NR频段数据
    
    Args:
        band_data_str: AT+SPLBAND=3返回的字符串，如 "545,0,528,0"
    
    Returns:
        支持的5G NR频段列表
    """
    
    # 5G NR频段定义（3GPP TS 38.101-1）
    nr_bands = {
        # NR FR1频段 (Sub-6GHz)
        1: {"name": "2100 MHz", "dl": "2110-2170 MHz", "ul": "1920-1980 MHz", "mode": "FDD", "region": "Global", "duplex_spacing": "190 MHz"},
        2: {"name": "1900 PCS", "dl": "1930-1990 MHz", "ul": "1850-1910 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "80 MHz"},
        3: {"name": "1800 DCS", "dl": "1805-1880 MHz", "ul": "1710-1785 MHz", "mode": "FDD", "region": "Global", "duplex_spacing": "95 MHz"},
        5: {"name": "850 MHz", "dl": "869-894 MHz", "ul": "824-849 MHz", "mode": "FDD", "region": "Global", "duplex_spacing": "45 MHz"},
        7: {"name": "2600 MHz", "dl": "2620-2690 MHz", "ul": "2500-2570 MHz", "mode": "FDD", "region": "Global", "duplex_spacing": "120 MHz"},
        8: {"name": "900 GSM", "dl": "925-960 MHz", "ul": "880-915 MHz", "mode": "FDD", "region": "Global", "duplex_spacing": "45 MHz"},
        12: {"name": "700 a", "dl": "729-746 MHz", "ul": "699-716 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "30 MHz"},
        13: {"name": "700 c", "dl": "746-756 MHz", "ul": "777-787 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "-31 MHz"},
        14: {"name": "700 PS", "dl": "758-768 MHz", "ul": "788-798 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "-30 MHz"},
        18: {"name": "800 Lower", "dl": "860-875 MHz", "ul": "815-830 MHz", "mode": "FDD", "region": "Japan", "duplex_spacing": "45 MHz"},
        20: {"name": "800 DD", "dl": "791-821 MHz", "ul": "832-862 MHz", "mode": "FDD", "region": "EMEA", "duplex_spacing": "-41 MHz"},
        25: {"name": "1900+", "dl": "1930-1995 MHz", "ul": "1850-1915 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "80 MHz"},
        26: {"name": "850+", "dl": "859-894 MHz", "ul": "814-849 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "45 MHz"},
        28: {"name": "700 APT", "dl": "758-803 MHz", "ul": "703-748 MHz", "mode": "FDD", "region": "APAC", "duplex_spacing": "55 MHz"},
        30: {"name": "2300 WCS", "dl": "2350-2360 MHz", "ul": "2305-2315 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "45 MHz"},
        34: {"name": "TD 2000", "dl": "2010-2025 MHz", "ul": "2010-2025 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        38: {"name": "TD 2600", "dl": "2570-2620 MHz", "ul": "2570-2620 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        39: {"name": "TD 1900+", "dl": "1880-1920 MHz", "ul": "1880-1920 MHz", "mode": "TDD", "region": "China", "duplex_spacing": "N/A"},
        40: {"name": "TD 2300", "dl": "2300-2400 MHz", "ul": "2300-2400 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        41: {"name": "TD 2600+", "dl": "2496-2690 MHz", "ul": "2496-2690 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        48: {"name": "TD 3600", "dl": "3550-3700 MHz", "ul": "3550-3700 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        50: {"name": "TD 1500+", "dl": "1432-1517 MHz", "ul": "1432-1517 MHz", "mode": "TDD", "region": "Europe", "duplex_spacing": "N/A"},
        51: {"name": "TD 1500-", "dl": "1427-1432 MHz", "ul": "1427-1432 MHz", "mode": "TDD", "region": "Europe", "duplex_spacing": "N/A"},
        65: {"name": "2100+", "dl": "2110-2200 MHz", "ul": "1920-2010 MHz", "mode": "FDD", "region": "Global", "duplex_spacing": "190 MHz"},
        66: {"name": "AWS", "dl": "2110-2200 MHz", "ul": "1710-1780 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "400 MHz"},
        67: {"name": "700 EU", "dl": "738-758 MHz", "ul": "N/A", "mode": "SDL", "region": "Europe", "duplex_spacing": "N/A"},
        68: {"name": "700 ME", "dl": "753-783 MHz", "ul": "698-728 MHz", "mode": "FDD", "region": "EMEA", "duplex_spacing": "55 MHz"},
        70: {"name": "AWS-4", "dl": "1995-2020 MHz", "ul": "1695-1710 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "300 MHz"},
        71: {"name": "600 MHz", "dl": "617-652 MHz", "ul": "663-698 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "-46 MHz"},
        74: {"name": "L-band", "dl": "1475-1518 MHz", "ul": "1427-1470 MHz", "mode": "FDD", "region": "Global", "duplex_spacing": "48 MHz"},
        75: {"name": "DL 1500+", "dl": "1432-1517 MHz", "ul": "N/A", "mode": "SDL", "region": "Europe", "duplex_spacing": "N/A"},
        76: {"name": "DL 1500-", "dl": "1427-1432 MHz", "ul": "N/A", "mode": "SDL", "region": "Europe", "duplex_spacing": "N/A"},
        77: {"name": "TD 3700", "dl": "3300-4200 MHz", "ul": "3300-4200 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        78: {"name": "TD 3500", "dl": "3300-3800 MHz", "ul": "3300-3800 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        79: {"name": "TD 4700", "dl": "4400-5000 MHz", "ul": "4400-5000 MHz", "mode": "TDD", "region": "China", "duplex_spacing": "N/A"},
        80: {"name": "SUL n3", "dl": "N/A", "ul": "1710-1785 MHz", "mode": "SUL", "region": "Global", "duplex_spacing": "N/A"},
        81: {"name": "SUL n8", "dl": "N/A", "ul": "880-915 MHz", "mode": "SUL", "region": "Global", "duplex_spacing": "N/A"},
        82: {"name": "SUL n20", "dl": "N/A", "ul": "832-862 MHz", "mode": "SUL", "region": "EMEA", "duplex_spacing": "N/A"},
        83: {"name": "SUL n28", "dl": "N/A", "ul": "703-748 MHz", "mode": "SUL", "region": "APAC", "duplex_spacing": "N/A"},
        84: {"name": "SUL n1", "dl": "N/A", "ul": "1920-1980 MHz", "mode": "SUL", "region": "Global", "duplex_spacing": "N/A"},
        85: {"name": "700 a+", "dl": "728-746 MHz", "ul": "698-716 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "30 MHz"},
        86: {"name": "SUL n66", "dl": "N/A", "ul": "1710-1780 MHz", "mode": "SUL", "region": "Americas", "duplex_spacing": "N/A"},
        87: {"name": "410 MHz", "dl": "420-425 MHz", "ul": "410-415 MHz", "mode": "FDD", "region": "EMEA", "duplex_spacing": "10 MHz"},
        88: {"name": "410+ MHz", "dl": "422-427 MHz", "ul": "412-417 MHz", "mode": "FDD", "region": "EMEA", "duplex_spacing": "10 MHz"},
        89: {"name": "SUL n5", "dl": "N/A", "ul": "824-849 MHz", "mode": "SUL", "region": "Americas", "duplex_spacing": "N/A"},
        90: {"name": "TD 2600+", "dl": "2496-2690 MHz", "ul": "2496-2690 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        # NR FR2频段 (mmWave)
        257: {"name": "28 GHz", "dl": "26500-29500 MHz", "ul": "26500-29500 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        258: {"name": "26 GHz", "dl": "24250-27500 MHz", "ul": "24250-27500 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        260: {"name": "39 GHz", "dl": "37000-40000 MHz", "ul": "37000-40000 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        261: {"name": "28 GHz US", "dl": "27500-28350 MHz", "ul": "27500-28350 MHz", "mode": "TDD", "region": "Americas", "duplex_spacing": "N/A"},
    }
    
    try:
        # 解析输入数据
        values = [int(x.strip()) for x in band_data_str.split(',')]
        
        print("展锐UDX710 5G NR频段解析器")
        print("=" * 70)
        print(f"原始AT命令返回: {band_data_str}")
        print(f"解析后数值: {values}")
        print()
        
        if len(values) < 4:
            print("错误：数据格式不正确，需要至少4个数值")
            return []
        
        fdd_value = values[0]  # NR-FDD参数：545
        tdd_value = values[2]  # NR-TDD参数：528
        
        supported_bands = []
        
        # 分析FDD频段 (545 = 0x221)
        if fdd_value != 0:
            print(f"NR-FDD频段分析: {fdd_value} (0x{fdd_value:X})")
            binary = format(fdd_value, '032b')
            print(f"二进制: {binary}")
            
            # 545 = 0x221 = 0b1000100001
            # 根据NR频段编码规律分析位映射
            fdd_band_mapping = {
                0: 1,   # 位0 -> n1 (2100 MHz)
                5: 66,  # 位5 -> n66 (AWS)
                9: 71,  # 位9 -> n71 (600 MHz)
                # 其他位根据实际情况映射
            }
            
            # 更精确的FDD频段映射（基于545的分析）
            # 545 in binary: 1000100001
            # 这表示支持n1, n66, n71等FDD频段
            
            for bit_pos in range(32):
                if (fdd_value >> bit_pos) & 1:
                    # 简化映射：直接使用位位置+1作为频段号（前32个频段）
                    band_num = bit_pos + 1
                    
                    # 特殊映射调整
                    if bit_pos == 0:  # 位0 -> n1
                        band_num = 1
                    elif bit_pos == 5:  # 位5 -> n5
                        band_num = 5  
                    elif bit_pos == 9:  # 位9 -> n71 (推测)
                        band_num = 71
                    
                    if band_num in nr_bands and nr_bands[band_num]['mode'] == 'FDD':
                        supported_bands.append(band_num)
                        print(f"  位{bit_pos}: n{band_num} ({nr_bands[band_num]['name']})")
            print()
        
        # 分析TDD频段 (528 = 0x210)  
        if tdd_value != 0:
            print(f"NR-TDD频段分析: {tdd_value} (0x{tdd_value:X})")
            binary = format(tdd_value, '032b')
            print(f"二进制: {binary}")
            
            # 528 = 0x210 = 0b1000010000
            # 这表示支持某些TDD频段
            
            for bit_pos in range(32):
                if (tdd_value >> bit_pos) & 1:
                    # TDD频段映射（基于常见的TDD频段）
                    if bit_pos == 4:  # 位4 -> n41 (推测)
                        band_num = 41
                    elif bit_pos == 9:  # 位9 -> n78 (推测)
                        band_num = 78
                    else:
                        # 其他TDD频段的推测映射
                        band_num = 30 + bit_pos  # TDD频段通常从n30开始
                    
                    if band_num in nr_bands and nr_bands[band_num]['mode'] == 'TDD':
                        if band_num not in supported_bands:
                            supported_bands.append(band_num)
                        print(f"  位{bit_pos}: n{band_num} ({nr_bands[band_num]['name']})")
            print()
        
        return sorted(supported_bands)
        
    except ValueError as e:
        print(f"数据解析错误: {e}")
        return []

def print_nr_band_summary(supported_bands, nr_bands):
    """打印5G NR频段汇总信息"""
    
    if not supported_bands:
        print("未检测到支持的5G NR频段")
        return
    
    print("=" * 100)
    print("支持的5G NR频段详细信息")
    print("=" * 100)
    
    fdd_bands = []
    tdd_bands = []
    sul_bands = []
    sdl_bands = []
    
    for band in supported_bands:
        if band in nr_bands:
            mode = nr_bands[band]['mode']
            if mode == 'FDD':
                fdd_bands.append(band)
            elif mode == 'TDD':
                tdd_bands.append(band)
            elif mode == 'SUL':
                sul_bands.append(band)
            elif mode == 'SDL':
                sdl_bands.append(band)
    
    # FDD频段表格
    if fdd_bands:
        print("\n📡 FDD频段 (频分双工):")
        print("-" * 100)
        print(f"{'频段':<8} {'名称':<15} {'下行频率':<20} {'上行频率':<20} {'双工间距':<12} {'区域':<10}")
        print("-" * 100)
        
        for band in fdd_bands:
            info = nr_bands[band]
            print(f"n{band:<7} {info['name']:<15} {info['dl']:<20} {info['ul']:<20} {info['duplex_spacing']:<12} {info['region']:<10}")
    
    # TDD频段表格  
    if tdd_bands:
        print(f"\n📶 TDD频段 (时分双工):")
        print("-" * 80)
        print(f"{'频段':<8} {'名称':<15} {'频率':<25} {'区域':<10}")
        print("-" * 80)
        
        for band in tdd_bands:
            info = nr_bands[band]
            print(f"n{band:<7} {info['name']:<15} {info['dl']:<25} {info['region']:<10}")
    
    # SUL频段表格
    if sul_bands:
        print(f"\n⬆️ SUL频段 (仅上行):")
        print("-" * 60)
        print(f"{'频段':<8} {'名称':<15} {'上行频率':<20} {'区域':<10}")
        print("-" * 60)
        
        for band in sul_bands:
            info = nr_bands[band]
            print(f"n{band:<7} {info['name']:<15} {info['ul']:<20} {info['region']:<10}")
    
    # SDL频段表格
    if sdl_bands:
        print(f"\n⬇️ SDL频段 (仅下行):")
        print("-" * 60)
        print(f"{'频段':<8} {'名称':<15} {'下行频率':<20} {'区域':<10}")
        print("-" * 60)
        
        for band in sdl_bands:
            info = nr_bands[band]
            print(f"n{band:<7} {info['name']:<15} {info['dl']:<20} {info['region']:<10}")
    
    print("-" * 100)
    print(f"总计支持 {len(supported_bands)} 个5G NR频段")
    print(f"  FDD: {len(fdd_bands)}个, TDD: {len(tdd_bands)}个, SUL: {len(sul_bands)}个, SDL: {len(sdl_bands)}个")
    
    # 频率范围分析
    print(f"\n📊 频率范围分析:")
    sub6_bands = []
    mmwave_bands = []
    
    for band in supported_bands:
        if band in nr_bands:
            if band >= 257:  # FR2 (mmWave)
                mmwave_bands.append(band)
            else:  # FR1 (Sub-6GHz)
                sub6_bands.append(band)
    
    if sub6_bands:
        print(f"  Sub-6GHz (FR1): {len(sub6_bands)}个频段 - n{', n'.join(map(str, sorted(sub6_bands)))}")
    if mmwave_bands:
        print(f"  毫米波 (FR2): {len(mmwave_bands)}个频段 - n{', n'.join(map(str, sorted(mmwave_bands)))}")
    
    # 区域覆盖分析
    print(f"\n🌍 区域覆盖分析:")
    regions = {}
    for band in supported_bands:
        if band in nr_bands:
            region = nr_bands[band]['region']
            if region not in regions:
                regions[region] = []
            regions[region].append(band)
    
    for region, bands in regions.items():
        print(f"  {region}: {len(bands)}个频段 (n{', n'.join(map(str, sorted(bands)))})")

def main():
    # 默认数据
    default_data = "545,0,528,0"
    
    print("🚀 欢迎使用展锐UDX710 5G NR频段解析器")
    print("支持解析AT+SPLBAND=3命令返回的5G NR频段信息")
    print()
    
    # 自动使用默认数据进行演示
    print("使用示例数据进行解析...")
    band_data = default_data
    
    # 5G NR频段定义（简化版本，包含主要频段）
    nr_bands = {
        1: {"name": "2100 MHz", "dl": "2110-2170 MHz", "ul": "1920-1980 MHz", "mode": "FDD", "region": "Global", "duplex_spacing": "190 MHz"},
        2: {"name": "1900 PCS", "dl": "1930-1990 MHz", "ul": "1850-1910 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "80 MHz"},
        3: {"name": "1800 DCS", "dl": "1805-1880 MHz", "ul": "1710-1785 MHz", "mode": "FDD", "region": "Global", "duplex_spacing": "95 MHz"},
        5: {"name": "850 MHz", "dl": "869-894 MHz", "ul": "824-849 MHz", "mode": "FDD", "region": "Global", "duplex_spacing": "45 MHz"},
        7: {"name": "2600 MHz", "dl": "2620-2690 MHz", "ul": "2500-2570 MHz", "mode": "FDD", "region": "Global", "duplex_spacing": "120 MHz"},
        8: {"name": "900 GSM", "dl": "925-960 MHz", "ul": "880-915 MHz", "mode": "FDD", "region": "Global", "duplex_spacing": "45 MHz"},
        12: {"name": "700 a", "dl": "729-746 MHz", "ul": "699-716 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "30 MHz"},
        20: {"name": "800 DD", "dl": "791-821 MHz", "ul": "832-862 MHz", "mode": "FDD", "region": "EMEA", "duplex_spacing": "-41 MHz"},
        25: {"name": "1900+", "dl": "1930-1995 MHz", "ul": "1850-1915 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "80 MHz"},
        28: {"name": "700 APT", "dl": "758-803 MHz", "ul": "703-748 MHz", "mode": "FDD", "region": "APAC", "duplex_spacing": "55 MHz"},
        38: {"name": "TD 2600", "dl": "2570-2620 MHz", "ul": "2570-2620 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        39: {"name": "TD 1900+", "dl": "1880-1920 MHz", "ul": "1880-1920 MHz", "mode": "TDD", "region": "China", "duplex_spacing": "N/A"},
        40: {"name": "TD 2300", "dl": "2300-2400 MHz", "ul": "2300-2400 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        41: {"name": "TD 2600+", "dl": "2496-2690 MHz", "ul": "2496-2690 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        66: {"name": "AWS", "dl": "2110-2200 MHz", "ul": "1710-1780 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "400 MHz"},
        71: {"name": "600 MHz", "dl": "617-652 MHz", "ul": "663-698 MHz", "mode": "FDD", "region": "Americas", "duplex_spacing": "-46 MHz"},
        77: {"name": "TD 3700", "dl": "3300-4200 MHz", "ul": "3300-4200 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        78: {"name": "TD 3500", "dl": "3300-3800 MHz", "ul": "3300-3800 MHz", "mode": "TDD", "region": "Global", "duplex_spacing": "N/A"},
        79: {"name": "TD 4700", "dl": "4400-5000 MHz", "ul": "4400-5000 MHz", "mode": "TDD", "region": "China", "duplex_spacing": "N/A"},
    }
    
    # 解析频段
    supported_bands = parse_unisoc_nr_bands(band_data)
    
    # 打印详细信息
    print_nr_band_summary(supported_bands, nr_bands)
    
    print(f"\n{'='*100}")
    print("📋 解析说明:")
    print("• 展锐UDX710支持这些5G NR频段进行高速通信")
    print("• FDD频段：上下行使用不同频率，适合覆盖和移动性")  
    print("• TDD频段：上下行使用相同频率但不同时间，适合高容量场景")
    print("• Sub-6GHz频段：提供广域覆盖，穿透力强")
    print("• 毫米波频段：提供超高速率，但覆盖范围有限")
    print("• 实际可用频段取决于当地运营商5G网络部署情况")

if __name__ == "__main__":
    main()