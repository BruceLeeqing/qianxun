#!/usr/bin/env python3
"""
旋转图片90度并调整为1024x500px
作为置顶大图标使用
"""

import os
import sys
from PIL import Image

def process_icon_image(image_path, output_path=None):
    """处理置顶大图标图片"""
    try:
        # 打开图片
        img = Image.open(image_path)
        width, height = img.size
        
        print(f"处理图片: {os.path.basename(image_path)}")
        print(f"原始尺寸: {width}x{height}")
        
        # 旋转90度
        img_rotated = img.rotate(-90, expand=True)  # -90度表示顺时针旋转90度
        rotated_width, rotated_height = img_rotated.size
        print(f"旋转后尺寸: {rotated_width}x{rotated_height}")
        
        # 调整尺寸为1024x500px
        target_width = 1024
        target_height = 500
        
        # 计算缩放比例，保持宽高比
        scale_factor = min(target_width / rotated_width, target_height / rotated_height)
        new_width = int(rotated_width * scale_factor)
        new_height = int(rotated_height * scale_factor)
        
        # 调整尺寸
        img_resized = img_rotated.resize((new_width, new_height), Image.Resampling.LANCZOS)
        print(f"缩放后尺寸: {new_width}x{new_height}")
        
        # 创建1024x500的画布（白色背景）
        canvas = Image.new('RGB', (target_width, target_height), (255, 255, 255))
        
        # 计算居中位置
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        
        # 将图片粘贴到画布中央
        canvas.paste(img_resized, (x_offset, y_offset))
        
        # 转换为 RGB 模式（移除 alpha 通道）
        if canvas.mode in ('RGBA', 'LA', 'P'):
            canvas = canvas.convert('RGB')
            print("转换为RGB模式（移除alpha通道）")
        
        # 确定输出路径
        if output_path is None:
            # 在原文件名基础上添加 _icon 后缀
            name, ext = os.path.splitext(image_path)
            output_path = f"{name}_icon{ext}"
        
        # 保存为JPEG格式
        canvas.save(output_path, 'JPEG', quality=90, optimize=True)
        
        print("处理完成！")
        print(f"输出文件: {output_path}")
        print(f"最终尺寸: {target_width}x{target_height}")
        print(f"格式: JPEG (符合要求)")
        
        return True
        
    except Exception as e:
        print(f"处理失败: {e}")
        return False

def main():
    """主函数"""
    image_path = "Qianxun材料\\79f6e447a6997698565a7b6e84095694.jpg"
    
    if not os.path.exists(image_path):
        print(f"错误: 图片文件 '{image_path}' 不存在")
        return
    
    print("开始处理置顶大图标...")
    print("=" * 60)
    
    # 处理图片
    success = process_icon_image(image_path)
    
    print("=" * 60)
    if success:
        print("置顶大图标处理完成！")
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