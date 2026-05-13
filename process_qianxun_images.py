#!/usr/bin/env python3
"""
处理 QianXun材料 目录中的图片文件
使其符合标准：
- JPEG 或 24-bit PNG (无 alpha 通道)
- 最小尺寸: 320px
- 最大尺寸: 3840px
- 截图的最大尺寸不得超过最小尺寸的两倍
"""

import os
import sys
from PIL import Image

def process_image(image_path):
    """处理单个图片文件"""
    try:
        # 打开图片
        img = Image.open(image_path)
        width, height = img.size
        
        print(f"处理: {os.path.basename(image_path)} - 原始尺寸: {width}x{height}")
        
        # 计算目标尺寸
        min_dim = min(width, height)
        max_dim = max(width, height)
        
        # 确保最小尺寸 >= 320px
        if min_dim < 320:
            scale_factor = 320 / min_dim
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            print(f"  - 放大到最小尺寸320px: {width}x{height} → {new_width}x{new_height}")
        # 确保最大尺寸 <= 3840px
        elif max_dim > 3840:
            scale_factor = 3840 / max_dim
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            print(f"  - 缩小到最大尺寸3840px: {width}x{height} → {new_width}x{new_height}")
        # 确保尺寸比例 <= 2:1
        elif max_dim > min_dim * 2:
            # 调整最大尺寸不超过最小尺寸的两倍
            if width > height:
                new_width = min_dim * 2
                new_height = min_dim
            else:
                new_width = min_dim
                new_height = min_dim * 2
            print(f"  - 调整尺寸比例: {width}x{height} → {new_width}x{new_height}")
        else:
            # 尺寸符合要求，只转换格式
            new_width, new_height = width, height
            print(f"  - 尺寸符合要求，只转换格式")
        
        # 调整尺寸
        if (new_width, new_height) != (width, height):
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 转换为 RGB 模式（移除 alpha 通道）
        if img.mode in ('RGBA', 'LA', 'P'):
            img = img.convert('RGB')
            print(f"  - 转换为RGB模式（移除alpha通道）")
        
        # 确定输出格式（保持原格式）
        if image_path.lower().endswith('.png'):
            output_format = 'PNG'
        else:
            output_format = 'JPEG'
        
        # 创建备份
        backup_path = image_path + '.bak'
        os.rename(image_path, backup_path)
        
        # 保存图片
        if output_format == 'JPEG':
            img.save(image_path, 'JPEG', quality=85, optimize=True)
        else:
            img.save(image_path, 'PNG', optimize=True)
        
        # 删除备份
        os.remove(backup_path)
        
        print(f"  ✅ 处理完成: {new_width}x{new_height} {output_format}")
        return True
        
    except Exception as e:
        print(f"  ❌ 处理失败: {e}")
        # 恢复备份
        if os.path.exists(backup_path):
            os.rename(backup_path, image_path)
        return False

def main():
    """主函数"""
    qianxun_materials_dir = "Qianxun材料"
    
    if not os.path.exists(qianxun_materials_dir):
        print(f"错误: 目录 '{qianxun_materials_dir}' 不存在")
        return
    
    # 搜索图片文件
    image_extensions = ['.jpg', '.jpeg', '.png']
    image_files = []
    
    for ext in image_extensions:
        for file in os.listdir(qianxun_materials_dir):
            if file.lower().endswith(ext):
                image_files.append(os.path.join(qianxun_materials_dir, file))
    
    print(f"在 '{qianxun_materials_dir}' 中找到 {len(image_files)} 个图片文件")
    print("=" * 60)
    
    if not image_files:
        print("没有找到需要处理的图片文件")
        return
    
    # 处理每个图片
    success_count = 0
    failed_count = 0
    
    for image_path in image_files:
        if process_image(image_path):
            success_count += 1
        else:
            failed_count += 1
        print()  # 空行分隔
    
    print("=" * 60)
    print(f"处理完成！")
    print(f"成功处理: {success_count} 个")
    print(f"处理失败: {failed_count} 个")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n处理被用户中断")
    except Exception as e:
        print(f"程序出错: {e}")
        sys.exit(1)