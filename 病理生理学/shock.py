import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 设置绘图风格
sns.set_style("whitegrid")
plt.rcParams['font.sans-serif'] = ['Arial']  # 防止字体报错
plt.rcParams['axes.unicode_minus'] = False

# 1. 定义时间轴 (模拟休克发展的三个阶段)
# 0-10: 代偿期 (Stage I)
# 10-20: 淤血期 (Stage II)
# 20-30: 衰竭期 (Stage III)
t = np.linspace(0, 30, 300)

# 2. 模拟心输出量 (CO) 的变化
# 逻辑：随着失血/回心血量减少，CO 是一直在下降的
# - Stage I: 代偿性心率加快，CO 下降较慢
# - Stage II: 回心血量受阻，CO 加速下降
# - Stage III: 心衰，CO 归零
def simulate_co(t):
    co = []
    for x in t:
        if x < 10:
            co.append(100 - 2 * x)  # 轻微下降
        elif x < 20:
            co.append(80 - 4 * (x - 10)) # 加速下降
        else:
            co.append(40 - 3 * (x - 20)) # 衰竭
    return np.array(co)

# 3. 模拟总外周阻力 (TPR) 的变化 (这是休克机制的核心！！！)
# 逻辑：
# - Stage I: 交感兴奋，血管收缩 -> TPR 飙升
# - Stage II: 酸中毒，血管麻痹 -> TPR 跳水
# - Stage III: 麻痹/微血栓 -> TPR 失效
def simulate_tpr(t):
    tpr = []
    for x in t:
        if x < 10:
            # 代偿期：阻力代偿性上升 (儿茶酚胺)
            tpr.append(1.0 + 0.05 * x) 
        elif x < 20:
            # 淤血期：阻力崩塌 (酸中毒/扩血管物质)
            # 这里模拟了一个指数级衰减
            decay = 1.5 * np.exp(-0.3 * (x - 10))
            tpr.append(max(0.4, decay))
        else:
            # 衰竭期：维持低水平
            tpr.append(0.4 - 0.01 * (x - 20))
    return np.array(tpr)

# 计算数据
CO_percent = simulate_co(t)
TPR_ratio = simulate_tpr(t)

# 4. 计算平均动脉压 (MAP)
# 公式：BP = CO * TPR (这里做归一化处理)
# 初始状态 BP = 100 * 1.0 = 100
BP_simulated = CO_percent * TPR_ratio

# --- 绘图可视化 ---
plt.figure(figsize=(12, 6))

# 绘制三条曲线
plt.plot(t, CO_percent, label='Cardiac Output (CO)', color='blue', linestyle='--', alpha=0.6)
plt.plot(t, TPR_ratio * 100, label='Total Peripheral Resistance (TPR)', color='green', linewidth=2)
plt.plot(t, BP_simulated, label='Blood Pressure (BP)', color='red', linewidth=3)

# 划分三个阶段的背景区域
plt.axvspan(0, 10, color='green', alpha=0.1, label='Stage I: Compensatory')
plt.axvspan(10, 20, color='orange', alpha=0.1, label='Stage II: Progressive')
plt.axvspan(20, 30, color='red', alpha=0.1, label='Stage III: Refractory')

# 添加关键注释 (Annotation) - 你的考点都在这里！
plt.text(5, 130, "Vasoconstriction\n(Catecholamines)", ha='center', color='green', fontweight='bold')
plt.text(15, 20, "Vasodilation\n(Acidosis/H+)", ha='center', color='green', fontweight='bold')
plt.text(5, 105, "BP Normal!", ha='center', color='red', fontweight='bold')
plt.text(15, 60, "BP Crash!", ha='center', color='red', fontweight='bold')

# 图表装饰
plt.title('Hemodynamic Changes during 3 Stages of Shock', fontsize=16)
plt.xlabel('Time (Arbitrary Units)', fontsize=12)
plt.ylabel('Relative Value (%)', fontsize=12)
plt.legend(loc='upper right')
plt.ylim(0, 160)
plt.grid(True, linestyle='--', alpha=0.5)

plt.show()