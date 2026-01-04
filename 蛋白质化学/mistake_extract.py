import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
import os

# 用于存储选定时间范围的全局变量
selected_time_range = []

def line_select_callback(eclick, erelease):
    """
    鼠标框选的回调函数。
    当鼠标释放时，记录选定的时间范围。
    """
    global selected_time_range
    # eclick 和 erelease 分别是鼠标按下和释放的事件
    x1 = eclick.xdata
    x2 = erelease.xdata
    
    # 获取时间范围（x轴）
    t_start = min(x1, x2)
    t_end = max(x1, x2)
    
    selected_time_range = [t_start, t_end]
    print(f"已选择时间范围: {t_start:.2f} 秒 到 {t_end:.2f} 秒")

def analyze_and_select_region():
    # ================= 配置区域 =================
    # 请确保文件名与您本地的文件名完全一致
    filename = '12_25休克.dat'
    
    # 采样率
    fs = 800.0
    
    # 血压换算比例
    scale_bp = 90.0 / 7486.0 
    # ===========================================

    # 1. 检查文件是否存在
    if not os.path.exists(filename):
        print(f"错误: 找不到文件 '{filename}'")
        print("请确认数据文件和本脚本在同一个目录下。")
        return

    print(f"正在读取文件: {filename} ...")
    
    try:
        # 2. 读取数据
        data_raw = np.fromfile(filename, dtype=np.int16)
        
        # 处理数据长度
        if data_raw.size % 4 != 0:
            valid_len = (data_raw.size // 4) * 4
            data_raw = data_raw[:valid_len]
            
        data_4ch = data_raw.reshape(-1, 4)
        
        # 提取 Channel 1 并转换为 mmHg
        ch1_raw = data_4ch[:, 0]
        ch1_mmhg = ch1_raw * scale_bp
        
        # 创建时间轴
        time = np.arange(len(ch1_mmhg)) / fs
        
        print("数据读取成功。")

        # 3. 交互式选择
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(time, ch1_mmhg, color='#1f77b4', linewidth=0.5, label='Raw Waveform')
        ax.set_title('请用鼠标框选您感兴趣的区域 (Select ROI)', fontsize=14)
        ax.set_xlabel('Time (s)', fontsize=12)
        ax.set_ylabel('Pressure (mmHg)', fontsize=12)
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.legend()

        # 创建矩形选择器
        # drawtype='box' 绘制矩形框
        # useblit=True 使用光栅技术加速绘制
        # button=[1] 仅响应鼠标左键
        # interactive=True 允许在选择完成后调整框的大小和位置
        rs = RectangleSelector(ax, line_select_callback,
                               drawtype='box', useblit=True,
                               button=[1], minspanx=5, minspany=5,
                               spancoords='pixels', interactive=True)

        print("\n【操作说明】")
        print("1. 在弹出的图像上，按住鼠标左键拖动，框选您想要放大的波形区域。")
        print("2. 选择完成后，请关闭该窗口。程序将自动绘制并保存您选定的区域。")
        
        # 阻塞程序，直到窗口关闭
        plt.show() 

        # 4. 绘制选定区域
        if selected_time_range:
            t_start, t_end = selected_time_range
            
            # 将时间转换为索引
            idx_start = int(t_start * fs)
            idx_end = int(t_end * fs)
            
            # 确保索引在有效范围内
            idx_start = max(0, idx_start)
            idx_end = min(len(time), idx_end)
            
            if idx_start >= idx_end:
                print("选择的区域无效（时间过短或范围错误），请重新运行并选择。")
                return

            # 提取选定片段的数据
            time_seg = time[idx_start:idx_end]
            signal_seg = ch1_mmhg[idx_start:idx_end]
            
            print(f"\n正在生成选定区域 ({t_start:.2f}-{t_end:.2f} s) 的图像...")

            # 绘制选定片段
            fig_sel, ax_sel = plt.subplots(figsize=(10, 6))
            ax_sel.plot(time_seg, signal_seg, color='#1f77b4', linewidth=1.0)
            ax_sel.set_title(f'Selected Waveform Fragment ({t_start:.2f} - {t_end:.2f} s)', fontsize=14)
            ax_sel.set_xlabel('Time (s)', fontsize=12)
            ax_sel.set_ylabel('Pressure (mmHg)', fontsize=12)
            ax_sel.grid(True, linestyle='--', alpha=0.7)
            
            # 保存图像
            output_file = 'selected_waveform.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            print(f"成功！选定区域的波形图已保存为: {output_file}")
            
            # 显示结果图像
            plt.show()
        else:
            print("\n您未选择任何区域就关闭了窗口，未生成新的图像。")

    except Exception as e:
        print(f"运行时发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # 运行前重置全局变量
    selected_time_range = []
    analyze_and_select_region()