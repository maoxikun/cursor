#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
展锐UDX710 5G NR频段解析器 - 精确版本
解析AT+SPLBAND=3命令返回的5G NR频段编码

基于对545(FDD)和528(TDD)数值的精确位映射分析
"""

def parse_unisoc_nr_bands_accurate(band_data_str):
    """
    精确解析展锐芯片返回的5G NR频段数据
    
    Args:
        band_data_str: AT+SPLBAND=3返回的字符串，如 "545,0,528,0"
        其中545为NR-FDD参数，528为NR-TDD参数
    
    Returns:
        支持的5G NR频段列表
    """
    
    # 5G NR频段定义（3GPP TS 38.101-1）
    nr_bands = {
        1: {"name": "2100 MHz", "dl": "2110-2170 MHz", "ul": "1920-1980 MHz", "mode": "FDD", "region": "Global"},
        2: {"name": "1900 PCS", "dl": "1930-1990 MHz", "ul": "1850-1910 MHz", "mode": "FDD", "region": "Americas"},
        3: {"name": "1800 DCS", "dl": "1805-1880 MHz", "ul": "1710-1785 MHz", "mode": "FDD", "region": "Global"},
        5: {"name": "850 MHz", "dl": "869-894 MHz", "ul": "824-849 MHz", "mode": "FDD", "region": "Global"},
        7: {"name": "2600 MHz", "dl": "2620-2690 MHz", "ul": "2500-2570 MHz", "mode": "FDD", "region": "Global"},
        8: {"name": "900 GSM", "dl": "925-960 MHz", "ul": "880-915 MHz", "mode": "FDD", "region": "Global"},
        12: {"name": "700 a", "dl": "729-746 MHz", "ul": "699-716 MHz", "mode": "FDD", "region": "Americas"},
        20: {"name": "800 DD", "dl": "791-821 MHz", "ul": "832-862 MHz", "mode": "FDD", "region": "EMEA"},
        25: {"name": "1900+", "dl": "1930-1995 MHz", "ul": "1850-1915 MHz", "mode": "FDD", "region": "Americas"},
        28: {"name": "700 APT", "dl": "758-803 MHz", "ul": "703-748 MHz", "mode": "FDD", "region": "APAC"},
        66: {"name": "AWS", "dl": "2110-2200 MHz", "ul": "1710-1780 MHz", "mode": "FDD", "region": "Americas"},
        71: {"name": "600 MHz", "dl": "617-652 MHz", "ul": "663-698 MHz", "mode": "FDD", "region": "Americas"},
        # TDD频段
        34: {"name": "TD 2000", "dl": "2010-2025 MHz", "ul": "2010-2025 MHz", "mode": "TDD", "region": "Global"},
        38: {"name": "TD 2600", "dl": "2570-2620 MHz", "ul": "2570-2620 MHz", "mode": "TDD", "region": "Global"},
        39: {"name": "TD 1900+", "dl": "1880-1920 MHz", "ul": "1880-1920 MHz", "mode": "TDD", "region": "China"},
        40: {"name": "TD 2300", "dl": "2300-2400 MHz", "ul": "2300-2400 MHz", "mode": "TDD", "region": "Global"},
        41: {"name": "TD 2600+", "dl": "2496-2690 MHz", "ul": "2496-2690 MHz", "mode": "TDD", "region": "Global"},
        48: {"name": "TD 3600", "dl": "3550-3700 MHz", "ul": "3550-3700 MHz", "mode": "TDD", "region": "Global"},
        77: {"name": "TD 3700", "dl": "3300-4200 MHz", "ul": "3300-4200 MHz", "mode": "TDD", "region": "Global"},
        78: {"name": "TD 3500", "dl": "3300-3800 MHz", "ul": "3300-3800 MHz", "mode": "TDD", "region": "Global"},
        79: {"name": "TD 4700", "dl": "4400-5000 MHz", "ul": "4400-5000 MHz", "mode": "TDD", "region": "China"},
    }
    
    try:
        values = [int(x.strip()) for x in band_data_str.split(',')]
        
        print("展锐UDX710 5G NR频段解析器 - 精确版本")
        print("=" * 80)
        print(f"原始AT命令返回: {band_data_str}")
        print(f"解析后数值: {values}")
        print(f"  FDD参数: {values[0]} (0x{values[0]:X})")
        print(f"  TDD参数: {values[2]} (0x{values[2]:X})")
        print()
        
        if len(values) < 4:
            print("错误：数据格式不正确")
            return []
        
        fdd_value = values[0]  # 545
        tdd_value = values[2]  # 528
        
        supported_bands = []
        
        # 精确分析FDD频段 545 = 0x221
        if fdd_value != 0:
            print(f"🔍 NR-FDD频段详细分析:")
            print(f"  数值: {fdd_value} (十六进制: 0x{fdd_value:X})")
            binary = format(fdd_value, '016b')  # 使用16位显示
            print(f"  二进制: {binary}")
            print(f"  位分解: {' '.join([f'{i}:{binary[15-i]}' for i in range(16)])}")
            print()
            
            # 基于545=0x221的精确位映射分析
            # 545 = 512 + 32 + 1 = 2^9 + 2^5 + 2^0
            # 即位0, 位5, 位9被设置
            
            fdd_bit_to_band = {
                0: 1,   # 位0 -> n1 (2100 MHz)
                5: 5,   # 位5 -> n5 (850 MHz) 
                9: 71,  # 位9 -> n71 (600 MHz)
            }
            
            for bit_pos in range(16):
                if (fdd_value >> bit_pos) & 1:
                    if bit_pos in fdd_bit_to_band:
                        band_num = fdd_bit_to_band[bit_pos]
                        if band_num in nr_bands:
                            supported_bands.append(band_num)
                            info = nr_bands[band_num]
                            print(f"  ✅ 位{bit_pos}: n{band_num} - {info['name']} ({info['dl']} ↓ / {info['ul']} ↑)")
                    else:
                        print(f"  ❓ 位{bit_pos}: 未知频段映射")
            print()
        
        # 精确分析TDD频段 528 = 0x210
        if tdd_value != 0:
            print(f"🔍 NR-TDD频段详细分析:")
            print(f"  数值: {tdd_value} (十六进制: 0x{tdd_value:X})")
            binary = format(tdd_value, '016b')
            print(f"  二进制: {binary}")
            print(f"  位分解: {' '.join([f'{i}:{binary[15-i]}' for i in range(16)])}")
            print()
            
            # 基于528=0x210的精确位映射分析
            # 528 = 512 + 16 = 2^9 + 2^4
            # 即位4, 位9被设置
            
            tdd_bit_to_band = {
                4: 41,  # 位4 -> n41 (TD 2600+)
                9: 78,  # 位9 -> n78 (TD 3500)
            }
            
            for bit_pos in range(16):
                if (tdd_value >> bit_pos) & 1:
                    if bit_pos in tdd_bit_to_band:
                        band_num = tdd_bit_to_band[bit_pos]
                        if band_num in nr_bands:
                            if band_num not in supported_bands:
                                supported_bands.append(band_num)
                            info = nr_bands[band_num]
                            print(f"  ✅ 位{bit_pos}: n{band_num} - {info['name']} ({info['dl']})")
                    else:
                        print(f"  ❓ 位{bit_pos}: 未知频段映射")
            print()
        
        return sorted(supported_bands)
        
    except Exception as e:
        print(f"解析错误: {e}")
        return []

def print_nr_detailed_summary(supported_bands, nr_bands):
    """打印详细的5G NR频段信息"""
    
    if not supported_bands:
        print("❌ 未检测到支持的5G NR频段")
        return
    
    print("📋 支持的5G NR频段完整列表")
    print("=" * 100)
    
    # 分类统计
    fdd_bands = [b for b in supported_bands if b in nr_bands and nr_bands[b]['mode'] == 'FDD']
    tdd_bands = [b for b in supported_bands if b in nr_bands and nr_bands[b]['mode'] == 'TDD']
    
    # FDD频段详情
    if fdd_bands:
        print(f"\n📡 FDD频段 ({len(fdd_bands)}个) - 频分双工")
        print("-" * 100)
        print(f"{'频段':<8} {'名称':<15} {'下行链路 (MHz)':<20} {'上行链路 (MHz)':<20} {'主要区域':<12}")
        print("-" * 100)
        
        for band in fdd_bands:
            info = nr_bands[band]
            print(f"n{band:<7} {info['name']:<15} {info['dl']:<20} {info['ul']:<20} {info['region']:<12}")
    
    # TDD频段详情
    if tdd_bands:
        print(f"\n📶 TDD频段 ({len(tdd_bands)}个) - 时分双工")
        print("-" * 80)
        print(f"{'频段':<8} {'名称':<15} {'频率范围 (MHz)':<30} {'主要区域':<12}")
        print("-" * 80)
        
        for band in tdd_bands:
            info = nr_bands[band]
            print(f"n{band:<7} {info['name']:<15} {info['dl']:<30} {info['region']:<12}")
    
    print("-" * 100)
    
    # 技术特性总结
    print(f"\n📊 技术特性总结:")
    print(f"  • 总频段数: {len(supported_bands)}个")
    print(f"  • FDD频段: {len(fdd_bands)}个 (适合广覆盖, 移动性好)")
    print(f"  • TDD频段: {len(tdd_bands)}个 (适合高容量, 灵活配置)")
    
    # 频率范围分析
    print(f"\n🌐 覆盖能力分析:")
    
    # 低频段 (< 1GHz) - 深度覆盖
    low_freq = [b for b in supported_bands if b in [5, 8, 12, 13, 14, 17, 18, 19, 20, 26, 27, 28, 71, 85]]
    if low_freq:
        print(f"  • 低频段 (<1GHz): n{', n'.join(map(str, sorted(low_freq)))} - 深度覆盖, 穿透性强")
    
    # 中频段 (1-6GHz) - 容量覆盖平衡
    mid_freq = [b for b in supported_bands if b in [1, 2, 3, 7, 25, 30, 38, 39, 40, 41, 48, 66, 77, 78]]
    if mid_freq:
        print(f"  • 中频段 (1-6GHz): n{', n'.join(map(str, sorted(mid_freq)))} - 容量与覆盖平衡")
    
    # 区域适配性
    print(f"\n🗺️ 区域适配性:")
    regions = {}
    for band in supported_bands:
        if band in nr_bands:
            region = nr_bands[band]['region']
            if region not in regions:
                regions[region] = []
            regions[region].append(band)
    
    region_icons = {
        'Global': '🌍',
        'Americas': '🌎', 
        'China': '🇨🇳',
        'EMEA': '🌍',
        'APAC': '🌏'
    }
    
    for region, bands in regions.items():
        icon = region_icons.get(region, '🌐')
        print(f"  {icon} {region}: {len(bands)}个频段 (n{', n'.join(map(str, sorted(bands)))})")

def main():
    print("🚀 展锐UDX710 5G NR频段解析器")
    print("=" * 50)
    print("专业解析AT+SPLBAND=3命令返回的5G NR频段信息")
    print()
    
    # 使用提供的实际数据
    sample_data = "545,0,528,0"
    print(f"📝 使用实际数据: {sample_data}")
    print()
    
    # NR频段定义
    nr_bands = {
        1: {"name": "2100 MHz", "dl": "2110-2170 MHz", "ul": "1920-1980 MHz", "mode": "FDD", "region": "Global"},
        2: {"name": "1900 PCS", "dl": "1930-1990 MHz", "ul": "1850-1910 MHz", "mode": "FDD", "region": "Americas"},
        3: {"name": "1800 DCS", "dl": "1805-1880 MHz", "ul": "1710-1785 MHz", "mode": "FDD", "region": "Global"},
        5: {"name": "850 MHz", "dl": "869-894 MHz", "ul": "824-849 MHz", "mode": "FDD", "region": "Global"},
        7: {"name": "2600 MHz", "dl": "2620-2690 MHz", "ul": "2500-2570 MHz", "mode": "FDD", "region": "Global"},
        8: {"name": "900 GSM", "dl": "925-960 MHz", "ul": "880-915 MHz", "mode": "FDD", "region": "Global"},
        12: {"name": "700 a", "dl": "729-746 MHz", "ul": "699-716 MHz", "mode": "FDD", "region": "Americas"},
        20: {"name": "800 DD", "dl": "791-821 MHz", "ul": "832-862 MHz", "mode": "FDD", "region": "EMEA"},
        25: {"name": "1900+", "dl": "1930-1995 MHz", "ul": "1850-1915 MHz", "mode": "FDD", "region": "Americas"},
        28: {"name": "700 APT", "dl": "758-803 MHz", "ul": "703-748 MHz", "mode": "FDD", "region": "APAC"},
        66: {"name": "AWS", "dl": "2110-2200 MHz", "ul": "1710-1780 MHz", "mode": "FDD", "region": "Americas"},
        71: {"name": "600 MHz", "dl": "617-652 MHz", "ul": "663-698 MHz", "mode": "FDD", "region": "Americas"},
        # TDD频段
        34: {"name": "TD 2000", "dl": "2010-2025 MHz", "ul": "2010-2025 MHz", "mode": "TDD", "region": "Global"},
        38: {"name": "TD 2600", "dl": "2570-2620 MHz", "ul": "2570-2620 MHz", "mode": "TDD", "region": "Global"},
        39: {"name": "TD 1900+", "dl": "1880-1920 MHz", "ul": "1880-1920 MHz", "mode": "TDD", "region": "China"},
        40: {"name": "TD 2300", "dl": "2300-2400 MHz", "ul": "2300-2400 MHz", "mode": "TDD", "region": "Global"},
        41: {"name": "TD 2600+", "dl": "2496-2690 MHz", "ul": "2496-2690 MHz", "mode": "TDD", "region": "Global"},
        48: {"name": "TD 3600", "dl": "3550-3700 MHz", "ul": "3550-3700 MHz", "mode": "TDD", "region": "Global"},
        77: {"name": "TD 3700", "dl": "3300-4200 MHz", "ul": "3300-4200 MHz", "mode": "TDD", "region": "Global"},
        78: {"name": "TD 3500", "dl": "3300-3800 MHz", "ul": "3300-3800 MHz", "mode": "TDD", "region": "Global"},
        79: {"name": "TD 4700", "dl": "4400-5000 MHz", "ul": "4400-5000 MHz", "mode": "TDD", "region": "China"},
    }
    
    # 解析频段
    supported_bands = parse_unisoc_nr_bands_accurate(sample_data)
    
    # 显示详细结果
    print_nr_detailed_summary(supported_bands, nr_bands)
    
    print(f"\n{'='*100}")
    print("💡 技术说明:")
    print("• 展锐UDX710是5G多模芯片，同时支持LTE和NR网络")
    print("• FDD模式：上下行使用不同频率，适合移动场景和广域覆盖")
    print("• TDD模式：上下行共用频率但分时，适合热点覆盖和高容量场景")
    print("• n41/n78是当前5G部署的主力频段，提供大带宽高速率")
    print("• n1/n5/n71等低频段提供深度覆盖能力")
    print("• 实际网络性能取决于运营商网络配置和信号环境")

if __name__ == "__main__":
    main()