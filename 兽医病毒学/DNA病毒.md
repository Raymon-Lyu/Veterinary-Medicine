<center><h1>DNA病毒</h1></center>

## 双股DNA病毒
### 痘病毒科
- 体积最大的病毒，天花是其中致病力最强的
- 能够引起全身或化脓性皮肤损害
##### 特征
- 遗传物质为dsDNA，但是自带DNA、mRNA合成酶，所以DNA复制发生在细胞质中
- **基因组**：
```mermaid
graph TD
    %% === 核心概念 ===
    subgraph Concept [核心概念: 它是如何构成的?]
        direction TB
        L1("<b>看起来是双链</b><br>(就像普通的 DNA 梯子)")
        L2("<b>实际上是一条单链</b><br>(首尾相连的大圈，被压扁了)")
        
        L1 -.->|变性/解旋后| L2
    end

    %% === 结构示意 ===
    subgraph Structure [痘病毒 DNA 结构示意]
        direction LR
        
        %% 定义节点
        Left_Loop((("<b>左端发卡环</b><br>(Hairpin Loop)")))
        Right_Loop((("<b>右端发卡环</b><br>(Hairpin Loop)")))
        
        Top_Strand[/"<b>上链 (Top Strand)</b><br>富含 A-T 序列"/]
        Bottom_Strand[/"<b>下链 (Bottom Strand)</b><br>与上链互补配对"\]
        
        %% 连接关系
        Left_Loop === Top_Strand
        Top_Strand === Right_Loop
        Right_Loop === Bottom_Strand
        Bottom_Strand === Left_Loop
        
        %% 碱基配对
        Top_Strand -.-|氢键连接<br>(中间部分是双链)| Bottom_Strand
    end

    %% === 功能示意 ===
    subgraph Function [为什么要有这个结构?]
        direction TB
        Step1[1. 解决末端问题] -->|没有游离的 5' 或 3' 端| Step2[酶无法直接啃咬/降解]
        Step1 -->|复制时| Step3[2. 自我引物 (Self-priming)]
        
        Step3 --> Action1("切开一个口子 (Nick)")
        Action1 --> Action2("发卡弹开，折叠成引物")
        Action2 --> Action3("聚合酶开始延伸")
    end

    %% === 样式美化 ===
    style Left_Loop fill:#ffcc80,stroke:#e65100,stroke-width:2px
    style Right_Loop fill:#ffcc80,stroke:#e65100,stroke-width:2px
    style Top_Strand fill:#e1f5fe,stroke:#0277bd
    style Bottom_Strand fill:#e1f5fe,stroke:#0277bd
    
    style Concept fill:#fff9c4,stroke:#fbc02d
    style Function fill:#f3e5f5,stroke:#8e24aa
```
### 非洲猪瘟病毒科
## 单股DNA病毒
