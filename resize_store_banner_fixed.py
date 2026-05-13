#!/usr/bin/env python3
"""
将商店主体大图转换为1024x500尺寸（无白色空隙）
"""

import os
import sys
from PIL import Image

def resize_store_banner_fixed(image_path, output_path=None):
    """将商店主体大图转换为1024x500尺寸，避免白色空隙"""
    try:
        # 打开图片
        img = Image.open(image_path)
        width, height = img.size
        
        print(f"处理图片: {os.path.basename(image_path)}")
        print(f"原始尺寸: {width}x{height}")
        
        # 目标尺寸
        target_width = 1024
        target_height = 500
        
        # 计算缩放比例，使图片至少覆盖目标尺寸
        scale_factor = max(target_width / width, target_height / height)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        
        print(f"缩放后尺寸: {new_width}x{new_height}")
        
        # 调整尺寸（放大到至少覆盖目标尺寸）
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # 计算裁剪区域（居中裁剪）
        left = (new_width - target_width) // 2
        top = (new_height - target_height) // 2
        right = left + target_width
        bottom = top + target_height
        
        print(f"裁剪区域: ({left}, {top}, {right}, {bottom})")
        
        # 裁剪图片
        img_cropped = img_resized.crop((left, top, right, bottom))
        
        # 转换为 RGB 模式（移除 alpha 通道）
        if img_cropped.mode in ('RGBA', 'LA', 'P'):
            img_cropped = img_cropped.convert('RGB')
            print("转换为RGB模式（移除alpha通道）")
        
        # 确定输出路径
        if output_path is None:
            # 在原文件名基础上添加 _banner_fixed 后缀
            name, ext = os.path.splitext(image_path)
            output_path = f"{name}_banner_fixed.jpg"
        
        # 保存为JPEG格式
        img_cropped.save(output_path, 'JPEG', quality=85, optimize=True)
        
        print("处理完成！")
        print(f"输出文件: {output_path}")
        print(f"最终尺寸: {target_width}x{target_height}")
        print(f"格式: JPEG (符合要求)")
        print("✅ 无白色空隙，完全填充画布")
        
        return True
        
    except Exception as e:
        print(f"处理失败: {e}")
        return False

def main():
    """主函数"""
    image_path = "Qianxun材料\\商店主体大图.png"
    
    if not os.path.exists(image_path):
        print(f"错误: 图片文件 '{image_path}' 不存在")
        return
    
    print("开始处理商店主体大图（修复白色空隙）...")
    print("=" * 60)
    
    # 处理图片
    success = resize_store_banner_fixed(image_path)
    
    print("=" * 60)
    if success:
        print("商店主体大图处理完成！")
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