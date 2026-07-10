# 鸡胚成纤维细胞体外观察与实验结果图库说明

本目录汇总整理了短学期动物医学专业关于**鸡胚成纤维细胞原代培养、组织植块培养、细胞活性检测（CCK-8）以及免疫荧光分析（PCNA 与 TUNEL）**的全部图像处理成果。图像均经过 eyepiece 视野提取、多通道融合（Channel Merge）、百分位亮度校准以及学术论文级拼接。

---

## 👤 实验人员信息
- **姓名**：吕启蒙
- **学号**：3230102953
- **专业**：动物医学
- **日期**：2026-07-07

---

## 📁 目录文件结构树

```text
细胞实验结果图/
├── CCK8实验前观察/
│   ├── CCK8_2x2_FBS_ascending.jpg        # 0% -> 5% -> 10% -> 20% FBS 递增浓度拼图（推荐使用）
│   ├── CCK8_2x2_FBS_row_order.jpg        # 按孔板原始顺序排列的 2x2 拼图
│   ├── CCK8_2x2_Serum_ascending.jpg      # 递增浓度拼图（别名版本）
│   └── CCK8_2x2_Serum_row_order.jpg      # 原始顺序排列拼图（别名版本）
│
├── TUNEL处理前观察，可当作正常培养细胞的图/
│   └── cropped_7.7 TUNEL细胞D-gal处理前.jpg # 正常生长状态下的鸡胚成纤维细胞贴壁形态
│
├── 原代细胞培养/
│   └── 白细胞计数区结果.jpg                # 血球计数板四个角计数区的 2x2 拼接图
│
├── 组织培养/
│   └── tissue_culture_2x2_grid.jpg       # 鸡胚组织块贴壁及细胞迁出（生长晕）观察拼图
│
└── 荧光显微结果/
    ├── TUNEL_split_channels_4x3_figure.jpg      # D-gal（0-300 mmol/L）凋亡检测三通道拆分对比图
    ├── TUNEL_split_channels_4x3_watermarked.jpg # TUNEL 对照组带 "2023-Group01" 水印防盗版
    ├── PCNA_split_channels_4x3_figure.jpg       # Serum（0%-20%）增殖检测三通道拆分对比图
    └── PCNA_split_channels_4x3_watermarked.jpg  # PCNA 对照组带 "2023-Group01" 水印防盗版
```

---

## 📝 各实验模块详细说明

### 1. 原代细胞培养与计数 (Primary Culture & Counting)
- **位置**：[原代细胞培养/白细胞计数区结果.jpg](file:///D:/just_soso/horse%20cow/Veterinary%20Medicine/短学期/细胞实验结果图/原代细胞培养/白细胞计数区结果.jpg)
- **内容**：展示了血球计数板的四个大格角区（左上、右上、左下、右下）的 2x2 拼接图像。
- **实验数据**：原代细胞悬液浓度约 **$4.8 \times 10^6 \text{ cells/mL}$**，平均每小格约 30 个细胞，台盼蓝染色存活率在 90% 以上。

### 2. 组织块植块培养观察 (Tissue Explant Culture)
- **位置**：[组织培养/tissue_culture_2x2_grid.jpg](file:///D:/just_soso/horse%20cow/Veterinary%20Medicine/短学期/细胞实验结果图/组织培养/tissue_culture_2x2_grid.jpg)
- **内容**：展示了剪切为 $1\text{ mm}^3$ 的鸡胚躯干组织块贴附于培养皿底壁后的体外生长情况。
- **现象描述**：可见明显的“**生长晕 (Growth Halo)**”现象，即原代表现为长突起的梭形或星形细胞从组织块边缘向外迁出并呈放射状贴壁增殖。

### 3. CCK-8 实验前细胞形态观察 (Pre-CCK8 Observations)
- **位置**：[CCK8实验前观察/CCK8_2x2_FBS_ascending.jpg](file:///D:/just_soso/horse%20cow/Veterinary%20Medicine/短学期/细胞实验结果图/CCK8实验前观察/CCK8_2x2_FBS_ascending.jpg)
- **内容**：在加入 CCK-8 试剂前，观察 0%（无血清饥饿）、5%、10% 和 20% FBS (胎牛血清) 培养 24h 后的细胞密度与形态变化。
- **生物学表现**：
  - **0% 组**：细胞密度极低，发生严重“饥饿”，表现出凋亡、核固缩及贴壁不良；
  - **10% 组**：成纤维细胞贴壁极佳，融合成单层，细胞密度最高，生长状态最好；
  - **20% 组**：密度略低于 10% 组，可能由于高浓度血清中的反馈抑制因子或营养稀释所致。

### 4. 正常贴壁细胞对照 (Normal Cultured Cells Control)
- **位置**：[TUNEL处理前观察，可当作正常培养细胞 of 图/cropped_7.7 TUNEL细胞D-gal处理前.jpg](file:///D:/just_soso/horse%20cow/Veterinary%20Medicine/短学期/细胞实验结果图/TUNEL处理前观察，可当作正常培养细胞的图/cropped_7.7%20TUNEL细胞D-gal处理前.jpg)
- **内容**：在添加凋亡诱导剂 D-半乳糖 (D-gal) 前的细胞形态，可作为标准的正常贴壁对照细胞（成纤维细胞）形态。

### 5. 荧光显微镜多通道对比图 (Fluorescence Microscopy Results)
本模块采用了国际顶尖期刊（如 *Nature Cell Biology*）推荐的通道拆分横向对比布局，每一行对应一个实验组别，横向展示：**DAPI（蓝色细胞核） $\rightarrow$ Target 荧光通道 $\rightarrow$ Merge（双通道叠加）**，且配有外围白色边距的浓度标志及 `50 μm` 白色比例尺。

#### 🟢 TUNEL 细胞凋亡检测 (D-gal 梯度诱导)
- **位置**：
  - 纯净学术版：[荧光显微结果/TUNEL_split_channels_4x3_figure.jpg](file:///D:/just_soso/horse%20cow/Veterinary%20Medicine/短学期/细胞实验结果图/荧光显微结果/TUNEL_split_channels_4x3_figure.jpg)
  - 防伪水印版：[荧光显微结果/TUNEL_split_channels_4x3_watermarked.jpg](file:///D:/just_soso/horse%20cow/Veterinary%20Medicine/短学期/细胞实验结果图/荧光显微结果/TUNEL_split_channels_4x3_watermarked.jpg)
- **原理**：TdT 酶介导 FITC-12-dUTP 标记断裂 DNA 的 3'-OH 末端，发生凋亡的细胞发**绿色荧光**。
- **表现**：随着 D-gal 浓度（0, 100, 200, 300 mmol/L）增加，DAPI 蓝色细胞核密度明显减少，而 TUNEL 绿色荧光斑点增多，细胞核出现固缩，凋亡率极显著上升。

#### 🔴 PCNA 细胞增殖检测 (Serum 梯度促进)
- **位置**：
  - 纯净学术版：[荧光显微结果/PCNA_split_channels_4x3_figure.jpg](file:///D:/just_soso/horse%20cow/Veterinary%20Medicine/短学期/细胞实验结果图/荧光显微结果/PCNA_split_channels_4x3_figure.jpg)
  - 防伪水印版：[荧光显微结果/PCNA_split_channels_4x3_watermarked.jpg](file:///D:/just_soso/horse%20cow/Veterinary%20Medicine/短学期/细胞实验结果图/荧光显微结果/PCNA_split_channels_4x3_watermarked.jpg)
- **原理**：增殖细胞核抗原 (PCNA) 在 S 期高表达，二抗标记后发**红色荧光**，定位活跃增殖细胞。
- **表现**：在 0% Serum 组，细胞密度极低且红色荧光微弱；在 5% 和 10% 组中，细胞密度及 PCNA 红色荧光比例大幅提升，显示血清能极显著刺激成纤维细胞的增殖。

---

> **注意：**所有防伪水印版本均在子图正中心呈 -30° 倾斜融合了“`2023-Group01`”半透明字样，可用于公开展示或防盗保护。
