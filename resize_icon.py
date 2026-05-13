#!/usr/bin/env python3
"""
将千寻图标转换为512x512尺寸
"""

import os
import sys
from PIL import Image

def resize_icon(image_path, output_path=None):
    """将图标转换为512x512尺寸"""
    try:
        # 打开图片
        img = Image.open(image_path)
        width, height = img.size
        
        print(f"处理图标: {os.path.basename(image_path)}")
        print(f"原始尺寸: {width}x{height}")
        
        # 目标尺寸
        target_size = 512
        
        # 计算缩放比例，保持宽高比
        scale_factor = min(target_size / width, target_size / height)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        print(f"缩放后尺寸: {new_width}x{new_height}")
        
        # 调整尺寸
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 创建512x512的画布（透明背景）
        if img.mode in ('RGBA', 'LA'):
            # 保持透明背景
            canvas = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
        else:
            # 转换为RGBA模式以支持透明背景
            canvas = Image.new('RGBA', (target_size, target_size), (0, 0, 0, 0))
            img_resized = img_resized.convert('RGBA')
        
        # 计算居中位置
        x_offset = (target_size - new_width) // 2
        y_offset = (target_size - new_height) // 2
        
        # 将图片粘贴到画布中央
        canvas.paste(img_resized, (x_offset, y_offset), img_resized if img_resized.mode == 'RGBA' else None)
        
        # 确定输出路径
        if output_path is None:
            # 在原文件名基础上添加 _512 后缀
            name, ext = os.path.splitext(image_path)
            output_path = f"{name}_512{ext}"
        
        # 保存为PNG格式（保持透明通道）
        canvas.save(output_path, 'PNG', optimize=True)
        
        print("处理完成！")
        print(f"输出文件: {output_path}")
        print(f"最终尺寸: {target_size}x{target_size}")
        print(f"格式: PNG (保持透明通道)")
        
        return True
        
    except Exception as e:
        print(f"处理失败: {e}")
        return False

def main():
    """主函数"""
    image_path = "Qianxun材料\\千寻图标.png"
    
    if not os.path.exists(image_path):
        print(f"错误: 图片文件 '{image_path}' 不存在")
        return
    
    print("开始处理千寻图标...")
    print("=" * 60)
    
    # 处理图片
    success = resize_icon(image_path)
    
    print("=" * 60)
    if success:
        print("图标处理完成！")
    else:
        print("处理失败")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n处理被用户中断")
    except Exception as e:
        print(f"程序出错: {e}")
        sys.exit(1)