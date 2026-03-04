import matplotlib.pyplot as plt
import numpy as np

# 设置全局字体和排版样式，保持论文级排版
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['mathtext.fontset'] = 'stix'
plt.rcParams['axes.linewidth'] = 1.5

# ---------------------------------------------------------
# 1. 数据生成：模拟符合原图分布特征的散点数据
# ---------------------------------------------------------
np.random.seed(42)
# 为了模拟图表中密度的变化，分段生成X轴数据（低延迟区域更密集）
x_dense = np.random.uniform(18, 100, 200)
x_med = np.random.uniform(100, 200, 150)
x_sparse = np.random.uniform(200, 320, 60)
x = np.concatenate([x_dense, x_med, x_sparse])

# 模拟 Y 轴数据 (基于 y = 1.0 + A/(x-B) 的形式添加随机噪声)
noise = np.random.normal(0, 0.04, len(x))
y = 1.0 + 8.0 / (x - 5) + noise
y = np.clip(y, 0.99, 1.55) # 裁剪以保证不越出视觉边界

# ---------------------------------------------------------
# 提示：如果您在实际工作流中，需要将此绘图脚本集成到自动化流程中，
# 从指定 workspace 路径下加载最新修改的 op_summary.csv 提取算子数据，
# 可以将上述 x, y 的生成逻辑替换为以下代码片段：
'''
import argparse
import os
import glob
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--workspace', type=str, default='./', help='Workspace path')
args, _ = parser.parse_known_args()

# 寻找最新修改的 op_summary.csv 
csv_files = glob.glob(os.path.join(args.workspace, '**', 'op_summary.csv'), recursive=True)
if csv_files:
    latest_csv = max(csv_files, key=os.path.getmtime)
    df = pd.read_csv(latest_csv)
    # 替换为您实际的列名
    x = df['baseline_latency'].values
    y = df['speedup_ratio'].values
'''
# ---------------------------------------------------------

# 2. 创建图表
fig, ax = plt.subplots(figsize=(10, 6))

# 绘制 y=1.0 的基线 (虚线，在图例中排第一)
ax.axhline(y=1.0, color='gray', linestyle='--', linewidth=2.5, label='Baseline (Speedup=1.0)')

# 绘制散点图
# 原图散点带有轻微的透明度，内部填充较浅，边缘较深
ax.scatter(x, y, s=18, color='#3070B3', alpha=0.85, edgecolors='#1A4A7A', linewidths=1.0, label='Kernel Speedup')

# 3. 设置坐标轴刻度和范围
ax.set_xlim(0, 330)
ax.set_ylim(0.9, 1.5)

xticks = [0, 50, 100, 150, 200, 250, 300]
ax.set_xticks(xticks)
ax.set_xticklabels(xticks, fontsize=20)

yticks = [0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
ax.set_yticks(yticks)
ax.set_yticklabels(yticks, fontsize=20)

# 4. 设置坐标轴标签 (包含 LaTeX 格式的微秒符号)
ax.set_xlabel(r'Kernel Latency of Baseline ($\mu s$)', fontsize=24, labelpad=10)
ax.set_ylabel('Speedup Ratio', fontsize=24, labelpad=10)

# 5. 设置网格线和图例
ax.grid(True, linestyle='-', color='#F0F0F0', linewidth=1.2)
ax.set_axisbelow(True)

ax.legend(fontsize=18, frameon=False, loc='upper right', handletextpad=0.8)

# 6. 调整刻度线样式
ax.tick_params(axis='both', which='major', length=6, width=1.5, direction='out')

# 7. 渲染展示
plt.tight_layout()
output_filename = 'figures/evaluation/op-speedup/d_attn_execution_speedup.pdf'
plt.savefig(output_filename, format='pdf', bbox_inches='tight')
print(f"Figure saved to: {output_filename}")

plt.close()