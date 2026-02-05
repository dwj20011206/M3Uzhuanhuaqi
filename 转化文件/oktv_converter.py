# -*- coding: utf-8 -*-
import os
import re

def extract_m3u_data(m3u_file):
    """从M3U文件提取数据"""
    channels = []
    
    with open(m3u_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找所有EXTINF和URL对
    pattern = r'#EXTINF:.*?,(.*?)\n(.*?)(?=\n|$)'
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
    
    for title, url in matches:
        title = title.strip()
        url = url.strip()
        
        if url and 'http' in url:
            # 简化标题 - 移除特殊字符和过长内容
            title = re.sub(r'[<>:"/\\|?*]', '', title)  # 移除文件非法字符
            if len(title) > 30:
                title = title[:27] + '...'
            channels.append((title, url))
    
    return channels

def create_oktv_format(channels, records_per_file=200):
    """创建ok影视pro专用格式"""
    total_files = (len(channels) + records_per_file - 1) // records_per_file
    
    for i in range(total_files):
        start_idx = i * records_per_file
        end_idx = min(start_idx + records_per_file, len(channels))
        
        # ok影视pro通常使用.txt扩展名或者简化m3u
        filename = f"oktv_{i+1:03d}.txt"
        
        with open(filename, 'w', encoding='utf-8') as out:
            # ok影视pro格式：第一行标题，第二行URL
            for j in range(start_idx, end_idx):
                title, url = channels[j]
                out.write(f"{title}\n")
                out.write(f"{url}\n")
        
        file_size = os.path.getsize(filename)
        print(f"生成 {filename}: {end_idx - start_idx} 个频道, {file_size} 字节")

def create_m3u_simple_format(channels, records_per_file=200):
    """创建简化M3U格式"""
    total_files = (len(channels) + records_per_file - 1) // records_per_file
    
    for i in range(total_files):
        start_idx = i * records_per_file
        end_idx = min(start_idx + records_per_file, len(channels))
        
        filename = f"oktv_{i+1:03d}_simple.m3u"
        
        with open(filename, 'w', encoding='utf-8') as out:
            out.write("#EXTM3U\n")
            out.write("#PLAYLIST:OKTV视频\n")
            
            for j in range(start_idx, end_idx):
                title, url = channels[j]
                # 简化标题
                title = re.sub(r'[\-：]+', ' - ', title)  # 统一分隔符
                if len(title) > 40:
                    title = title[:37] + '...'
                
                out.write(f"#EXTINF:-1,{title}\n")
                out.write(f"{url}\n")
        
        file_size = os.path.getsize(filename)
        print(f"生成 {filename}: {end_idx - start_idx} 个频道, {file_size} 字节")

# 主程序
print("开始为ok影视pro优化文件...")

# 提取数据
channels = extract_m3u_data('fixed_18+2026.m3u')
print(f"提取到 {len(channels)} 个频道")

# 创建两种格式
print("\n创建.txt格式文件（推荐）:")
create_oktv_format(channels, records_per_file=200)

print("\n创建简化M3U格式文件:")
create_m3u_simple_format(channels, records_per_file=200)

print(f"\n✅ 处理完成！")
print("📱 ok影视pro使用建议：")
print("1. 先尝试加载 .txt 格式文件")
print("2. 如果不行，尝试加载 .txt 格式文件")
print("3. 每个文件包含200个频道，应该能稳定加载")
print("4. 文件名格式：oktv_001.txt, oktv_002.txt, ...")