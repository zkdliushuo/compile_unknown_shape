import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# 设置全局字体样式
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']
plt.rcParams['axes.linewidth'] = 1.2

# 构造模拟数据以近似原图的趋势
x = np.arange(10)

# Prefill Phase 数据
prefill_llama = [
    [1.026, 1.031, 1.033, 1.025, 1.022, 1.028, 1.023, 1.014, 1.012, 1.021], # BS=1
    [1.032, 1.031, 1.033, 1.032, 1.027, 1.018, 1.013, 1.011, 1.013, 1.007], # BS=2
    [1.029, 1.022, 1.033, 1.026, 1.014, 1.011, 1.012, 1.004, 1.009, 1.007]  # BS=4
]
prefill_qwen = [
    [1.019, 1.019, 1.021, 1.024, 1.023, 1.021, 1.017, 1.016, 1.017, 1.019], # BS=1
    [1.014, 1.015, 1.016, 1.020, 1.024, 1.015, 1.015, 1.009, 1.011, 1.016], # BS=2
    [1.013, 1.016, 1.017, 1.016, 1.015, 1.009, 1.012, 1.006, 1.009, 1.004]  # BS=4
]

# Decode Phase 数据
decode_llama = [
    [1.031, 1.025, 1.029, 1.035, 1.032, 1.024, 1.031, 1.015, 1.027, 1.026], # BS=1
    [1.024, 1.028, 1.027, 1.037, 1.029, 1.018, 1.025, 1.015, 1.011, 1.010], # BS=2
    [1.039, 1.027, 1.032, 1.020, 1.021, 1.026, 1.009, 1.008, 1.010, 1.015]  # BS=4
]
decode_qwen = [
    [1.032, 1.038, 1.032, 1.037, 1.037, 1.038, 1.023, 1.034, 1.030, 1.021], # BS=1
    [1.031, 1.030, 1.035, 1.025, 1.024, 1.018, 1.019, 1.014, 1.010, 1.016], # BS=2
    [1.034, 1.034, 1.028, 1.021, 1.024, 1.016, 1.015, 1.006, 1.008, 1.012]  # BS=4
]

# 颜色和样式配置
c_llama = '#ff3b17' 
c_qwen = '#279cf5'  
marker_size = 4
line_width = 2.0

# 1. 稍微调高 figsize (从 1.8 增加到 2.2)，给底部标签留出空间
fig = plt.figure(figsize=(15, 2.2))
gs_main = gridspec.GridSpec(1, 2, wspace=0.25)

phases = ['Prefill Phase', 'Decode Phase']
data_llama = [prefill_llama, decode_llama]
data_qwen = [prefill_qwen, decode_qwen]

for phase_idx in range(2):
    gs_sub = gridspec.GridSpecFromSubplotSpec(1, 3, subplot_spec=gs_main[phase_idx], wspace=0)
    
    for i in range(3):
        ax = fig.add_subplot(gs_sub[i])
        
        line_llama, = ax.plot(x, data_llama[phase_idx][i], color=c_llama, marker='s', markersize=marker_size,
                              markerfacecolor='white', markeredgewidth=1.2, linewidth=line_width, label='Llama2-7B')
        line_qwen, = ax.plot(x, data_qwen[phase_idx][i], color=c_qwen, marker='o', markersize=marker_size,
                             markerfacecolor='white', markeredgewidth=1.2, linewidth=line_width, label='Qwen2-1.5B')
        
        ax.set_ylim(0.985, 1.055)
        ax.axhline(1.00, color='gray', linestyle='--', linewidth=1.5, zorder=0)
        ax.axhline(1.05, color='lightgray', linestyle='--', linewidth=0.8, alpha=0.6, zorder=0)
        
        ax.set_xticks([])
        # 2. 减小 labelpad，让 BS 标签更贴合坐标轴
        ax.set_xlabel(f"BS={2**i}", fontweight='bold', fontsize=13, labelpad=4)
        
        if i == 0:
            ax.set_yticks([1.00, 1.05])
            ax.set_yticklabels(['1.00', '1.05'], fontsize=12)
            ax.set_ylabel("Speedup", fontweight='bold', fontsize=14)
        else:
            ax.set_yticks([])
            ax.spines['left'].set_visible(False)
            
        if i < 2:
            ax.spines['right'].set_color('lightgray')
            ax.spines['right'].set_linewidth(0.8)
            
        if i == 1:
            ax.set_title(phases[phase_idx], fontsize=15, pad=10)
            # 3. 降低 Sequence Length 文本和箭头的 y 轴比例位置 (从 0.08 降到 0.03)
            ax.text(0.5, 0.05, 'Sequence Length', transform=ax.transAxes, ha='center', va='bottom', fontweight='bold', fontsize=10)
            ax.annotate('', xy=(0.02, 0.04), xytext=(0.98, 0.04), xycoords='axes fraction',
                        arrowprops=dict(arrowstyle='<->', color='black', lw=1.0))
            ax.plot([0.02, 0.02], [0.01, 0.06], color='black', transform=ax.transAxes, lw=1.2)
            ax.plot([0.98, 0.98], [0.01, 0.06], color='black', transform=ax.transAxes, lw=1.2)
            
        if i == 0:
            ax.text(0.98, 0.015, '32', transform=ax.transAxes, ha='right', va='bottom', fontsize=9)
        if i == 2:
            ax.text(0.02, 0.015, '2048', transform=ax.transAxes, ha='left', va='bottom', fontsize=9)

        if phase_idx == 1 and i == 2:
            ax.legend(handles=[line_llama, line_qwen], loc='upper right', fontsize=9, framealpha=1, edgecolor='lightgray')

# 4. 手动微调边距，并使用 bbox_inches='tight' 导出
plt.subplots_adjust(bottom=0.22, top=0.82)
plt.savefig("multi_model_speedup.png", bbox_inches='tight', dpi=300)
plt.show()