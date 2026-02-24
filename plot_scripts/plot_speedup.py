import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

# 1. 数据准备 (根据原图目测估算的数据)
categories = [
    'P-Attn', 'FFN', 'RMS', 'MM', 'D-Attn', 
    'Gate', 'Sink', 'Perm', 'GN', 'Pool', 
    'Pow', 'Upsample', 'BN', 'Scat', 'AVE'
]

# 估算数值
llvm_spec = [1.032, 1.006, 0.976, 1.014, 1.022, 0.990, 1.018, 0.998, 1.070, 0.990, 1.011, 1.008, 1.020, 1.002, 1.011]
tiling_infer = [1.087, 1.054, 1.082, 1.034, 1.176, 1.031, 1.035, 1.060, 1.107, 0.995, 1.071, 1.103, 1.030, 1.012, 1.062]
optimal = [1.106, 1.058, 1.088, 1.053, 1.185, 1.051, 1.037, 1.080, 1.120, 0.995, 1.073, 1.114, 1.031, 1.020, 1.073]

# 2. 设置绘图参数
x = np.arange(len(categories))  # 标签位置
width = 0.24  # 柱状图宽度

# 设置图表大小 (宽:高)，原图比较宽扁
fig, ax = plt.subplots(figsize=(14, 4))

# 3. 绘制柱状图
# 颜色定义
color_llvm_edge = '#bdbdbd'  # 浅灰色边框
color_ti_fill = '#1f5b8b'    # 深蓝色填充
color_opt_edge = '#f58a5e'   # 橙色边框

# 绘制 Series 1: LLVM-spec (白色填充 + 灰色斜线纹理)
rects1 = ax.bar(x - width, llvm_spec, width, label='LLVM-spec',
                color='white', edgecolor=color_llvm_edge, hatch='//', linewidth=1, zorder=3)

# 绘制 Series 2: TilingInfer (深蓝填充 + 黑色细边框)
rects2 = ax.bar(x, tiling_infer, width, label='TilingInfer',
                color=color_ti_fill, edgecolor='black', linewidth=0.6, zorder=3)

# 绘制 Series 3: Optimal (白色填充 + 橙色点状纹理)
rects3 = ax.bar(x + width, optimal, width, label='Optimal',
                color='white', edgecolor=color_opt_edge, hatch='..', linewidth=1, zorder=3)

# 4. 样式调整

# Y轴范围和网格线
ax.set_ylim(0.90, 1.22)
ax.set_yticks([0.90, 0.95, 1.00, 1.05, 1.10, 1.15, 1.20])
ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0) # 虚线网格，置于底层

# 基准线 (y=1.0)
ax.axhline(y=1.0, color='black', linewidth=1.2, zorder=2)

# X轴标签
ax.set_xticks(x)
# 使用 Liberation Sans 字体（与原图一致）
font_name = 'Liberation Sans'
ax.set_xticklabels(categories, fontsize=11, fontname=font_name)

# Y轴标签
ax.set_ylabel('Normalized Speedup', fontsize=14, fontweight='bold', fontname=font_name, labelpad=10)
# 设置刻度字体
for label in ax.get_yticklabels():
    label.set_fontname(font_name)
    label.set_fontsize(11)

# 去除顶部和右侧的边框脊柱 (Spines) - 可选，若要完全模仿原图盒子可以保留
# 这里保留盒子，因为原图似乎有完整的边框
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
# 原图看起来只有左边和下边比较明显，或者全框比较细。
# 通常学术图表去顶部右侧边框比较常见，但看图上似乎顶部有虚线网格延伸，我们保持简洁。

# 5. 图例 (Legend)
# 需要为 Baseline 创建自定义图例句柄（黑色横线）
baseline_line = Line2D([0], [0], color='black', linewidth=1.2, label='Baseline')
# 获取现有的图例句柄
handles, labels = ax.get_legend_handles_labels()
# 添加 Baseline 图例句柄
handles.append(baseline_line)
labels.append('Baseline')
# 创建图例，四列
legend = ax.legend(
    handles=handles,
    labels=labels,
    loc='upper center', 
    bbox_to_anchor=(0.5, 1.12), # 稍微向上偏移出绘图区
    ncol=4, 
    frameon=False, 
    fontsize=12,
    handletextpad=0.5
)

# 6. 布局紧凑调整并保存
plt.tight_layout()

# 保存为 PDF
output_filename = 'speedup_histogram.pdf'
plt.savefig(output_filename, format='pdf', bbox_inches='tight')
print(f"图表已生成并保存为: {output_filename}")

# 如果需要在窗口显示，取消下面的注释
# plt.show()