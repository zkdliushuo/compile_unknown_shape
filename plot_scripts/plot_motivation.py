import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体样式，尽量匹配原图的无衬线字体
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Helvetica']
plt.rcParams['axes.linewidth'] = 1.5  # 设置坐标轴线宽

# ================= 数据准备 =================
# 注意：y轴顺序在绘图时通常是从下到上，所以数据列表顺序为 [MM, FFN, P-Attn, D-Attn]
labels = ['MM', 'FFN', 'P-Attn', 'D-Attn']

# 左图数据
data_scalar_ratio = [85, 85, 91, 78]   # Teal bars
data_icache_miss = [3.1, 3.9, 16.4, 4.5] # Red bars

# 右图数据
data_invariable = [62, 115, 249, 361] # Blue bars
data_variable = [9, 8, 48, 15]        # Orange bars

# ================= 辅助函数 =================
def setup_axis(ax, x_label):
    """设置通用的坐标轴样式"""
    # 隐藏上边框和右边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False) # 隐藏左边框，只留刻度文字
    
    # 加粗底部边框
    ax.spines['bottom'].set_linewidth(1.5)
    ax.spines['bottom'].set_color('black')
    
    # 设置Y轴刻度字体加粗
    ax.set_yticks(np.arange(len(labels)))
    ax.set_yticklabels(labels, fontsize=14, fontweight='bold')
    
    # 设置X轴网格线
    ax.grid(axis='x', linestyle='--', alpha=0.7, zorder=0)
    
    # 设置X轴标签
    ax.set_xlabel(x_label, fontsize=14, fontweight='bold')
    ax.tick_params(axis='x', labelsize=14)
    ax.tick_params(axis='y', length=0) # 隐藏Y轴刻度线

# ================= 绘图 1: Metrics Analysis (左图) =================
def plot_metrics_analysis():
    fig, ax = plt.subplots(figsize=(8, 4))
    
    y = np.arange(len(labels))
    height = 0.35  # 条形高度
    
    # 颜色定义
    color_teal = '#7DB9B6'
    color_red = '#E66F6A'
    
    # 绘制条形图
    # Scalar Ratio (上方条形)
    bars1 = ax.barh(y + height/2 + 0.02, data_scalar_ratio, height, 
                    label='Scalar Ratio (%)', color=color_teal, edgecolor='none', zorder=3)
    
    # ICache Miss (下方条形) - 带有白色斜线纹理
    bars2 = ax.barh(y - height/2 - 0.02, data_icache_miss, height, 
                    label='I-Cache Miss (%)', color=color_red, edgecolor='white', hatch='///', zorder=3)
    
    # 添加数值标签
    for bar in bars1:
        width = bar.get_width()
        ax.text(width + 2, bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', va='center', ha='left', 
                color=color_teal, fontweight='bold', fontsize=12)
        
    for bar in bars2:
        width = bar.get_width()
        # 对于较小的值，稍微向右移一点以防重叠
        offset = 1
        ax.text(width + offset, bar.get_y() + bar.get_height()/2, 
                f'{width}', va='center', ha='left', 
                color=color_red, fontweight='bold', fontsize=12)

    # 设置图例 (顶部居中，无边框)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), 
              ncol=2, frameon=False, fontsize=14, handletextpad=0.5)
    
    # 设置X轴范围 (稍微留白)
    ax.set_xlim(0, 110)
    
    setup_axis(ax, 'Percentage (%)')
    
    # 调整布局并保存
    plt.tight_layout()
    plt.savefig('metrics_analysis.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("生成完成: metrics_analysis.pdf")

# ================= 绘图 2: Parameter Breakdown (右图) =================
def plot_parameter_breakdown():
    fig, ax = plt.subplots(figsize=(8, 4))
    
    y = np.arange(len(labels))
    height = 0.6  # 堆叠图条形较宽
    
    # 颜色定义
    color_blue = '#517FB2'
    color_orange = '#F69E46'
    
    # 绘制堆叠条形图
    # Invariable Params (底层/左侧)
    bars1 = ax.barh(y, data_invariable, height, 
                    label='Invariable Params', color=color_blue, edgecolor='none', zorder=3)
    
    # Variable Params (顶层/右侧) - 带有白色斜线纹理
    bars2 = ax.barh(y, data_variable, height, left=data_invariable,
                    label='Variable Params', color=color_orange, edgecolor='white', hatch='///', zorder=3)
    
    # 添加数值标签
    # 蓝色条形上的白色文字 (居中或靠右)
    for bar in bars1:
        width = bar.get_width()
        # 文字在条形内部中心
        ax.text(width / 2 if width > 50 else width - 10, 
                bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', va='center', ha='center', 
                color='white', fontweight='bold', fontsize=14)
        
    # 橙色条形旁的黑色文字
    for i, bar in enumerate(bars2):
        width = bar.get_width()
        x_pos = data_invariable[i] + width + 5 # 文字在条形右侧外部
        ax.text(x_pos, bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', va='center', ha='left', 
                color='black', fontsize=14)

    # 设置图例
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), 
              ncol=2, frameon=False, fontsize=14, handletextpad=0.5)
    
    # 设置X轴范围
    ax.set_xlim(0, 450)
    
    setup_axis(ax, 'Number of Schedule Parameters')
    
    # 调整布局并保存
    plt.tight_layout()
    plt.savefig('parameter_breakdown.pdf', format='pdf', bbox_inches='tight')
    plt.close()
    print("生成完成: parameter_breakdown.pdf")

# ================= 执行 =================
if __name__ == "__main__":
    plot_metrics_analysis()
    plot_parameter_breakdown()