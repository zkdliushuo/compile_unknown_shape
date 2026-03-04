import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体和排版样式，使其接近原图的论文风格
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'  # 使得数学公式字体与正文一致
plt.rcParams['axes.linewidth'] = 1.5      # 图表边框粗细

# 生成 X 轴数据点 (共16个点，对应 kv_lengths)
# 从 32 开始，间隔 256，最后一个点为 4096
kv_lengths = [32 + i * 256 for i in range(15)] + [4096]

# 提取 Y 轴数据点 (对应您的 speedup_1 到 speedup_4)
speedup_1 = [1.425, 1.295, 1.375, 1.285, 1.215, 1.170, 1.175, 1.160, 1.110, 1.115, 1.105, 1.098, 1.100, 1.110, 1.080, 1.110]
speedup_2 = [1.490, 1.340, 1.330, 1.295, 1.225, 1.195, 1.158, 1.145, 1.120, 1.110, 1.100, 1.095, 1.085, 1.070, 1.055, 1.100]
speedup_3 = [1.430, 1.325, 1.285, 1.245, 1.152, 1.142, 1.110, 1.090, 1.082, 1.078, 1.052, 1.035, 1.037, 1.068, 1.048, 1.025]
speedup_4 = [1.465, 1.278, 1.155, 1.148, 1.085, 1.076, 1.055, 1.042, 1.072, 1.040, 1.038, 1.035, 0.990, 1.020, 1.020, 1.018]

# 创建图表
fig, ax = plt.subplots(figsize=(10, 6))

# 使用您提供的参数绘制四条折线
ax.plot(kv_lengths, speedup_1, 'o-', color='#1f77b4', linewidth=2, markersize=6, 
        label=r'$B=4, h_q=32, h_{kv}=8$')
ax.plot(kv_lengths, speedup_2, 's-', color='#ff7f0e', linewidth=2, markersize=6,
        label=r'$B=4, h_q=64, h_{kv}=16$')
ax.plot(kv_lengths, speedup_3, '^-', color='#2ca02c', linewidth=2, markersize=6,
        label=r'$B=8, h_q=64, h_{kv}=16$')
ax.plot(kv_lengths, speedup_4, 'd-', color='#d62728', linewidth=2, markersize=6,
        label=r'$B=8, h_q=128, h_{kv}=32$')

# 绘制 y=1.0 的灰色虚线参考线
ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=2, alpha=0.8)

# 设置 X 轴和 Y 轴的刻度线与原图完全一致
xticks = [32, 844, 1657, 2470, 3283, 4096]
ax.set_xticks(xticks)
ax.set_xticklabels(xticks, fontsize=20)

yticks = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
ax.set_yticks(yticks)
ax.set_yticklabels(yticks, fontsize=20)

# 设置坐标轴标签
ax.set_xlabel('Length of Cached KV Sequence', fontsize=24, labelpad=10)
ax.set_ylabel('Speedup Ratio', fontsize=24, labelpad=10)

# 设置网格线 (仅水平和垂直的浅色网格)
ax.grid(True, linestyle='-', color='#EFEFEF', linewidth=1.5)
ax.set_axisbelow(True)

# 设置图例
legend = ax.legend(fontsize=18, frameon=False, loc='upper right')

# 调整刻度线的长度和粗细
ax.tick_params(axis='both', which='major', length=6, width=1.5, direction='out')

# 调整布局并展示
plt.tight_layout()

# Save as PDF
output_filename = 'figures/evaluation/op-speedup/d_attn_kv_length_speedup.pdf'
plt.savefig(output_filename, format='pdf', bbox_inches='tight')
print(f"Figure saved to: {output_filename}")

plt.close()