# -*- coding: utf-8 -*-
"""
ok影视pro自动化转换器
自动将文件夹中的txt文件转换为ok影视pro专用格式
"""
import os
import glob
import re
import sys

def read_txt_file(file_path):
    """读取txt文件并提取频道信息"""
    channels = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        
        # 处理不同格式的txt文件
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            if not line:
                i += 1
                continue
            
            # 查找URL行
            if 'http' in line and ('m3u8' in line or '.mp4' in line or '.flv' in line):
                # 查找上一行作为标题
                title = ""
                if i > 0:
                    title_line = lines[i-1].strip()
                    if title_line and not title_line.startswith('#'):
                        title = title_line
                
                # 如果没有找到标题，使用文件名
                if not title:
                    title = os.path.splitext(os.path.basename(file_path))[0]
                
                # 清理标题
                title = clean_title(title)
                channels.append((title, line))
            
            i += 1
        
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
    
    return channels

def clean_title(title):
    """清理标题，移除特殊字符"""
    # 移除文件路径中的非法字符
    title = re.sub(r'[<>:"/\\|?*]', '', title)
    # 限制标题长度
    if len(title) > 50:
        title = title[:47] + '...'
    return title.strip()

def create_oktv_files(channels, output_prefix, records_per_file=200):
    """创建ok影视pro格式的文件"""
    if not channels:
        print("没有找到有效的频道数据")
        return 0
    
    total_files = (len(channels) + records_per_file - 1) // records_per_file
    
    for i in range(total_files):
        start_idx = i * records_per_file
        end_idx = min(start_idx + records_per_file, len(channels))
        
        # 创建输出文件名
        output_file = f"{output_prefix}_{i+1:03d}.txt"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as out:
                for j in range(start_idx, end_idx):
                    title, url = channels[j]
                    out.write(f"{title}\n")
                    out.write(f"{url}\n")
            
            file_size = os.path.getsize(output_file)
            print(f"✅ 生成文件: {output_file} ({end_idx - start_idx}个频道, {file_size}字节)")
            
        except Exception as e:
            print(f"❌ 生成文件 {output_file} 时出错: {e}")
    
    return total_files

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 ok影视pro自动化转换器")
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
        channels = read_txt_file(txt_file)
        if channels:
            all_channels.extend(channels)
            processed_files.append(os.path.basename(txt_file))
    
    if not all_channels:
        print("❌ 没有找到有效的频道数据")
        input("按回车键退出...")
        return
    
    print(f"📊 总共收集到 {len(all_channels)} 个频道")
    print(f"📝 处理了 {len(processed_files)} 个文件")
    
    # 创建输出文件
    output_prefix = "ok影视pro_转换"
    total_files = create_oktv_files(all_channels, output_prefix, records_per_file=200)
    
    print("\n" + "=" * 60)
    print("✅ 转换完成！")
    print(f"📁 输出文件: {output_prefix}_001.txt 到 {output_prefix}_{total_files:03d}.txt")
    print(f"📺 总频道数: {len(all_channels)}")
    print(f"📦 文件数量: {total_files} 个")
    print("\n💡 使用说明:")
    print("1. 将生成的ok影视pro_转换_*.txt文件导入到ok影视pro")
    print("2. 每个文件包含200个频道")
    print("3. 文件大小约20-30KB，适合ok影视pro加载")
    print("=" * 60)
    
    input("按回车键退出...")

if __name__ == "__main__":
    main()