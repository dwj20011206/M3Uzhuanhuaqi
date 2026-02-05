# -*- coding: utf-8 -*-
"""
OKTV专用M3U转换器
基于oktv_converter.py架构，支持从txt文件转换为OKTV格式的M3U文件
"""
import os
import glob
import re

def extract_txt_data(txt_file):
    """从TXT文件提取频道数据 - 逗号分隔格式"""
    channels = []
    
    try:
        with open(txt_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # 跳过空行和标题行
            if not line or line.startswith('#genre#') or line.startswith('精品'):
                continue
            
            # 解析逗号分隔的格式：标题,URL
            if ',' in line:
                parts = line.split(',', 1)  # 只分割第一个逗号
                if len(parts) == 2:
                    title = parts[0].strip()
                    url = parts[1].strip()
                    
                    # 检查URL是否有效
                    if url and 'http' in url and ('m3u8' in url or '.mp4' in url or '.flv' in url):
                        # 清理标题 - 保持与oktv_converter.py一致的规则
                        title = re.sub(r'[<>:"/\\|?*]', '', title)  # 移除文件非法字符
                        title = re.sub(r'[\-：]+', ' - ', title)  # 统一分隔符
                        if len(title) > 30:
                            title = title[:27] + '...'
                        
                        channels.append((title, url))
        
    except Exception as e:
        print(f"读取文件 {txt_file} 时出错: {e}")
    
    return channels

def create_oktv_m3u_format(channels, records_per_file=200):
    """创建OKTV专用M3U格式文件"""
    if not channels:
        print("没有找到有效的频道数据")
        return 0
    
    total_files = (len(channels) + records_per_file - 1) // records_per_file
    
    for i in range(total_files):
        start_idx = i * records_per_file
        end_idx = min(start_idx + records_per_file, len(channels))
        
        # 使用oktv标准命名格式
        filename = f"oktv_{i+1:03d}_simple.m3u"
        
        try:
            with open(filename, 'w', encoding='utf-8') as out:
                # 写入OKTV格式头部
                out.write("#EXTM3U\n")
                out.write("#PLAYLIST:OKTV视频\n")
                
                for j in range(start_idx, end_idx):
                    title, url = channels[j]
                    # 简化标题 - 按照oktv_converter.py的规则
                    title = re.sub(r'[\-：]+', ' - ', title)  # 统一分隔符
                    if len(title) > 40:
                        title = title[:37] + '...'
                    
                    out.write(f"#EXTINF:-1,{title}\n")
                    out.write(f"{url}\n")
            
            file_size = os.path.getsize(filename)
            print(f"✅ 生成 {filename}: {end_idx - start_idx} 个频道, {file_size} 字节")
            
        except Exception as e:
            print(f"❌ 生成文件 {filename} 时出错: {e}")
    
    return total_files

def main():
    """主程序"""
    print("=" * 60)
    print("🚀 OKTV专用M3U转换器")
    print("=" * 60)
    
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 查找所有txt文件
    txt_files = glob.glob(os.path.join(script_dir, "*.txt"))
    
    if not txt_files:
        print("❌ 在当前文件夹中未找到txt文件")
        input("按回车键退出...")
        return
    
    print(f"📁 找到 {len(txt_files)} 个txt文件")
    
    # 读取所有文件的数据
    all_channels = []
    processed_files = []
    
    for txt_file in txt_files:
        print(f"📖 正在处理: {os.path.basename(txt_file)}")
        channels = extract_txt_data(txt_file)
        if channels:
            all_channels.extend(channels)
            processed_files.append(os.path.basename(txt_file))
            print(f"   提取到 {len(channels)} 个频道")
    
    if not all_channels:
        print("❌ 没有找到有效的频道数据")
        input("按回车键退出...")
        return
    
    print(f"📊 总共收集到 {len(all_channels)} 个频道")
    print(f"📝 处理了 {len(processed_files)} 个文件")
    
    # 创建OKTV格式的M3U文件
    print("\n🚀 开始创建OKTV格式M3U文件:")
    total_files = create_oktv_m3u_format(all_channels, records_per_file=200)
    
    print("\n" + "=" * 60)
    print("✅ 转换完成！")
    print(f"📁 输出文件: oktv_001_simple.m3u 到 oktv_{total_files:03d}_simple.m3u")
    print(f"📺 总频道数: {len(all_channels)}")
    print(f"📦 文件数量: {total_files} 个")
    print("\n💡 使用说明:")
    print("1. 将生成的M3U文件导入到OKTV播放器")
    print("2. 每个文件包含200个频道")
    print("3. 文件大小约25-35KB，适合播放器加载")
    print("4. 标准M3U格式，兼容性好")
    print("5. 严格按照oktv_001_simple(1).m3u格式生成")
    print("=" * 60)
    
    input("按回车键退出...")

if __name__ == "__main__":
    main()