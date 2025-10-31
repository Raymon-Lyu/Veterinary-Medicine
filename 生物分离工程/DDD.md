
```mermaid
graph TD
    A(畜牧学) --> B(第一章: 概论);
    A --> C(第二章: 动物遗传育种);
    A --> D(第三章: 动物繁殖);
    A --> E(第四章: 畜禽营养与饲料);
    A --> F(第五章: 畜禽生产各论);

    %% 第一章: 概论
    B --> B1(畜牧学定义);
    B1 --> B1a(研究动物遗传变异、生长发育、生理繁育、消化代谢、营养饲养及产品生产的科学)[cite: 5373];
    B --> B2(畜牧业的重要性);
    [cite_start]B2 --> B2a(国民经济支柱产业)[cite: 5406, 5409];
    [cite_start]B2 --> B2b(提供优质动物产品(肉蛋奶))[cite: 5365, 5415];
    [cite_start]B2 --> B2c(增加就业, 助力乡村振兴)[cite: 5434, 5436];
    [cite_start]B2 --> B2d(提供工业原料 (皮革、阿胶等))[cite: 5447];
    [cite_start]B2 --> B2e(农业现代化的标志)[cite: 5467];
    [cite_start]B2 --> B2f(为人类健康提供模型 (异种移植))[cite: 5122, 5132, 5140];
    B --> B3(我国畜牧业现状与趋势);
    B3 --> B3a(世界畜禽生产大国);
    [cite_start]B3a --> B3a1(2023年猪肉、羊肉、禽蛋产量世界第一)[cite: 5486, 5487, 5490];
    [cite_start]B3a --> B3a2(2024年猪肉、羊肉、禽肉、禽蛋产量世界第一)[cite: 5507, 5512, 5515, 5520];
    [cite_start]B3 --> B3b(世界最大饲料生产国)[cite: 6432, 6437];
    [cite_start]B3 --> B3c(畜禽良种繁育体系不断完善)[cite: 6573];
    [cite_start]B3 --> B3d(面临挑战: 疫病防控严峻, 成本居高不下, 饲料粮不足, 环境污染)[cite: 6578, 6580, 6582, 6584];
    B --> B4(典型疫病对畜牧业的影响);
    [cite_start]B4 --> B4a(非洲猪瘟 (ASF))[cite: 6608];
    [cite_start]B4a --> B4a1(高致死率 [cite: 6613, 6634][cite_start], 导致2019-2020年猪肉产量锐减 [cite: 5635, 6642][cite_start], 推动产业集中度提升 [cite: 6762, 6769, 6781]);
    [cite_start]B4 --> B4b(禽流感 (AIV))[cite: 6953];
    [cite_start]B4b --> B4b1(全球性爆发, 导致大量扑杀 [cite: 4279, 4286][cite_start], 引发“蛋荒”和价格上涨 [cite: 4285, 4298]);
    [cite_start]B4b --> B4b2(主要亚型 H5N1, H7N9, H10N5)[cite: 4311, 6964, 6969, 6985];

    %% 第二章: 动物遗传育种
    [cite_start]C --> C1(动物遗传基础 (自修))[cite: 7921];
    [cite_start]C1 --> C1a(中心法则: DNA -> RNA -> Protein -> Function)[cite: 7923, 7925, 7927, 7928];
    [cite_start]C --> C2(畜禽主要性状分类)[cite: 7954];
    [cite_start]C2 --> C2a(质量性状)[cite: 7981];
    [cite_start]C2a --> C2a1(单/少数基因决定, 表型不连续, 如毛色、血型)[cite: 7986, 7991];
    [cite_start]C2a --> C2a2(遗传方式: 显隐性, 上位作用, 伴性/从性/限性遗传)[cite: 7996, 7997, 7998, 7999, 8000, 8001];
    [cite_start]C2a --> C2a3(实例: 鸡金银羽 (伴性遗传) [cite: 8068, 8076, 8079][cite_start], 牛双肌 [cite: 8137]);
    [cite_start]C2 --> C2b(数量性状)[cite: 7982];
    [cite_start]C2b --> C2b1(多基因控制, 呈连续变异, 受环境影响, 如体重、产奶量)[cite: 7986, 8274, 8276];
    [cite_start]C2b --> C2b2(遗传参数: 遗传力(h2), 重复力, 遗传相关)[cite: 8341, 8342, 8343];
    [cite_start]C2b --> C2b3(遗传力高低: 繁殖性状(<0.1) [cite: 8361] [cite_start]< 生长性状(0.1-0.3) [cite: 8359] [cite_start]< 体构成性状(>0.3) [cite: 8349]);
    [cite_start]C2 --> C2c(阈性状)[cite: 7983];
    [cite_start]C2c --> C2c1(多基因控制, 表型不连续, 如抗病性、产仔数)[cite: 7986];
    [cite_start]C --> C3(选种与选配)[cite: 3169, 3799];
    [cite_start]C3 --> C3a(选种: 选优去劣, 提高群体品质)[cite: 3803, 3804];
    [cite_start]C3a --> C3a1(选择反应 G = h2 * P)[cite: 8505];
    [cite_start]C3 --> C3b(选配: 按目标指定公母畜交配)[cite: 3817];
    [cite_start]C --> C4(动物品种培育)[cite: 3170, 3827];
    [cite_start]C4 --> C4a(方法: 选择育种 [cite: 3858][cite_start], 杂交育种 (简单/复杂) [cite: 3853, 4087, 4129][cite_start], 诱变育种 [cite: 3854, 3859][cite_start], 分子育种 (标记辅助/转基因) [cite: 3855, 3867, 3869]);
    [cite_start]C4 --> C4b(基因编辑育种: 抗病猪 (抗蓝耳病, 抗传胃) [cite: 3876, 3900][cite_start], 抗病牛 [cite: 3965][cite_start], 抗热应激牛 [cite: 3972][cite_start], 抗病羊 [cite: 3981][cite_start], 抗病鸡 [cite: 4000]);
    [cite_start]C --> C5(动物遗传资源保护)[cite: 3171, 4191];

    %% 第三章: 动物繁殖
    [cite_start]D --> D1(生殖器官)[cite: 976];
    [cite_start]D1 --> D1a(公畜: 睾丸、附睾、输精管、副性腺、阴茎等)[cite: 991, 993];
    [cite_start]D1 --> D1b(母畜: 卵巢、输卵管、子宫、阴道等)[cite: 1022];
    [cite_start]D --> D2(生殖细胞与受精)[cite: 1046];
    [cite_start]D2 --> D2a(精子 与 卵子)[cite: 1047, 1048, 1073];
    [cite_start]D2 --> D2b(受精: 精卵结合形成合子)[cite: 1081, 1082];
    [cite_start]D --> D3(生殖激素)[cite: 1089];
    [cite_start]D3 --> D3a(如: GnRH, FSH, LH, LTH等)[cite: 1091];
    [cite_start]D --> D4(发情与配种)[cite: 1100];
    [cite_start]D4 --> D4a(繁殖相关概念: 初情期 [cite: 1107][cite_start], 性成熟 [cite: 1110][cite_start], 体成熟 [cite: 1114][cite_start], 初配年龄 [cite: 1115]);
    [cite_start]D4 --> D4b(发情周期: 牛/猪/马/山羊约21天, 绵羊16-17天)[cite: 1138];
    [cite_start]D4 --> D4c(发情鉴定: 外部观察 (爬跨) [cite: 1132, 1152][cite_start], 试情法 [cite: 1156][cite_start], B超等 [cite: 1158]);
    [cite_start]D4 --> D4d(配种方法: 自然交配 [cite: 1194] [cite_start]和 人工授精(AI) [cite: 1194]);
    [cite_start]D4 --> D4e(AI优点: 提高优良公畜利用率, 减少疾病传播)[cite: 1219, 1222];
    D --> D5(妊娠与分娩);
    [cite_start]D5 --> D5a(妊娠期: 猪(114天) [cite: 1261][cite_start], 羊(150天) [cite: 1261][cite_start], 牛(282天) [cite: 1260][cite_start], 马(336天) [cite: 1262][cite_start], 兔(31天) [cite: 1262]);
    [cite_start]D5 --> D5b(妊娠检查: B超 [cite: 1238, 1254][cite_start], 直肠检查 (大家畜) [cite: 1238, 1253][cite_start], 激素测定等 [cite: 1238, 1248]);
    [cite_start]D5 --> D5c(分娩与接产: 助产 (难产时) [cite: 1278, 1296][cite_start], 断脐消毒 [cite: 1279, 1284]);
    [cite_start]D --> D6(繁育新技术)[cite: 1347];
    [cite_start]D6 --> D6a(同期发情 与 超数排卵)[cite: 1349, 1356];
    [cite_start]D6 --> D6b(性别控制 (X/Y精子分离))[cite: 1359, 1367];
    [cite_start]D6 --> D6c(胚胎移植 (ET))[cite: 1374, 1375];
    [cite_start]D6 --> D6d(体细胞克隆 (核移植))[cite: 1401, 1402];

    %% 第四章: 畜禽营养与饲料
    [cite_start]E --> E1(饲料与畜体化学组成)[cite: 2516, 2580];
    [cite_start]E1 --> E1a(六大营养素: 水, 粗蛋白(CP), 粗脂肪(EE), 碳水化合物, 矿物质, 维生素)[cite: 2592, 2593, 2603, 2604, 2600, 2601, 2602];
    [cite_start]E --> E2(饲料消化性)[cite: 2713];
    [cite_start]E2 --> E2a(消化方式: 物理 (咀嚼, 肌胃研磨) [cite: 2749, 2788][cite_start]，化学 (酶) [cite: 2760][cite_start]，微生物 (瘤胃, 后肠) [cite: 2762, 2802, 2900]);
    [cite_start]E2 --> E2b(消化特点: 猪 (酶消化为主) [cite: 2774][cite_start], 鸡 (肌胃/肠短) [cite: 2785, 2788][cite_start], 反刍 (复胃/微生物) [cite: 2802, 2811, 2820][cite_start], 兔/马 (盲肠发达) [cite: 2879, 2883, 2900]);
    [cite_start]E2 --> E2c(影响因素: 动物 (种类/年龄) [cite: 2986, 2988][cite_start], 饲料 (粗纤维/抗营养因子) [cite: 2997, 8819][cite_start], 加工 (粉碎/膨化) [cite: 8826]);
    E --> E3(六大营养素详解);
    E3 --> E3a(水);
    [cite_start]E3a1(功能: 构成机体 (新生雏鸡85%) [cite: 8835][cite_start], 代谢溶剂 [cite: 8838][cite_start], 调节体温 [cite: 8839]);
    [cite_start]E3a2(来源: 饮水 [cite: 8855][cite_start], 饲料水 [cite: 8880][cite_start], 代谢水 (脂肪最高) [cite: 8895, 8899]);
    [cite_start]E3a3(需水量: 受干物质采食量、温度、生理状态影响)[cite: 8872, 8938];
    E3 --> E3b(蛋白质);
    [cite_start]E3b1(功能: 构成/更新组织 [cite: 9011, 9012][cite_start], 功能物质 (酶/激素/抗体) [cite: 9013][cite_start], 供能 [cite: 9014]);
    [cite_start]E3b2(必需AA (EAA): 体内不能合成或合成不足)[cite: 9190, 9191];
    [cite_start]E3b3(限制性AA (LAA): 木桶理论 [cite: 9278][cite_start]。猪: 赖氨酸[cite: 9245]; [cite_start]鸡: 蛋氨酸 [cite: 9245]);
    [cite_start]E3b4(反刍动物: 瘤胃微生物可合成EAA [cite: 9128][cite_start], 依赖微生物蛋白(MCP)和过瘤胃蛋白(RUP) [cite: 9087]);
    E3 --> E3c(脂类);
    [cite_start]E3c1(功能: 供能/贮能 (最高) [cite: 26, 27][cite_start], 额外能量效应 [cite: 32][cite_start], 脂溶性维生素溶剂 [cite: 79][cite_start], 必需脂肪酸(EFA)来源 [cite: 88]);
    [cite_start]E3c2(必需脂肪酸: 亚油酸 [cite: 101, 111][cite_start], 亚麻酸 [cite: 102, 112]);
    [cite_start]E3c3(代谢紊乱: 脂肪肝出血综合症 (笼养蛋鸡))[cite: 181, 182];
    E3 --> E3d(碳水化合物);
    [cite_start]E3d1(分类: 可利用 (淀粉/糖原) [cite: 225, 227] [cite_start]vs 不可利用 (纤维素/半纤维素/NSP) [cite: 231, 234, 457]);
    [cite_start]E3d2(功能: 供能 (主要) [cite: 269][cite_start]，构成组织 (核酸) [cite: 274]);
    [cite_start]E3d3(粗纤维 (CF) [cite: 289][cite_start]: 优点 (饱感/刺激肠道) [cite: 292, 293] [cite_start]vs 缺点 (消化率低/影响其他养分) [cite: 301, 302]);
    [cite_start]E3d4(NSP (非淀粉多糖) [cite: 456][cite_start]: 抗营养作用 (降吸收/降能值/粘性粪便) [cite: 492, 493, 495][cite_start], 需加酶制剂克服 [cite: 499]);
    E3 --> E3e(矿物质);
    [cite_start]E3e1(常量元素 (Ca, P, Mg, Na, Cl...))[cite: 542, 563];
    [cite_start]E3e2(微量元素 (Fe, Cu, Zn, Mn, Se, I...))[cite: 544, 565];
    [cite_start]E3e3(缺乏症: 佝偻病/软骨病 (Ca/P/Vit D) [cite: 599][cite_start], 贫血 (Fe, 仔猪需补铁) [cite: 710, 721][cite_start], 啄癖/咬尾 (Na/Cl) [cite: 665, 667, 668][cite_start], 白肌病 (Se/Vit E) [cite: 859, 860, 875][cite_start], 滑腱症 (Mn) [cite: 814]);
    E3 --> E3f(维生素);
    [cite_start]E3f1(脂溶性: A (视觉/上皮) [cite: 945, 946][cite_start], D (Ca/P吸收) [cite: 103][cite_start], E (抗氧化) [cite: 107, 915][cite_start], K (凝血) [cite: 110, 915]);
    [cite_start]E3f2(水溶性: B族 (辅酶) [cite: 906][cite_start], C [cite: 913]);
    [cite_start]E3f3(缺乏症: 夜盲症/干眼病 (Vit A) [cite: 945, 954][cite_start], 渗出性素质/脑软化 (Vit E) [cite: 108, 861][cite_start], 出血 (Vit K) [cite: 111]);
    E --> E4(饲料分类);
    [cite_start]E4 --> E4a(按营养: 能量饲料, 蛋白质饲料, 矿物质饲料, 添加剂)[cite: 4833, 4834];
    [cite_start]E4 --> E4b(按配方: 预混料 [cite: 2659][cite_start], 浓缩饲料 [cite: 2660][cite_start], 配合饲料(全价料) [cite: 2660, 2665]);
    [cite_start]E4 --> E4c(按对象: 猪 [cite: 2684][cite_start], 禽 [cite: 2684][cite_start], 反刍 [cite: 2684][cite_start], 水产饲料 [cite: 2684]);

    %% 第五章: 畜禽生产各论
    F --> F1(养猪生产);
    [cite_start]F1 --> F1a(现状: 2024年出栏7.02亿头, 产量5706万吨)[cite: 5417, 5418, 5750, 5752];
    [cite_start]F1 --> F1b(挑战: ASF导致产量波动)[cite: 5635, 5639, 6642];
    [cite_start]F1 --> F1c(产业调控与升级: 调减能繁母猪 [cite: 5970, 6050][cite_start], 推广低蛋白日粮 [cite: 5973][cite_start], 数字化 [cite: 5974]);
    [cite_start]F1 --> F1d(产业集中度: Top 20 占28% (2023年) [cite: 6782][cite_start], 牧原第一 [cite: 6785]);
    [cite_start]F --> F2(养牛生产)[cite: 7067, 7078];
    [cite_start]F2 --> F2a(分类: 家牛属(普通牛/瘤牛/牦牛) [cite: 7150, 7152][cite_start], 水牛属 [cite: 7157]);
    [cite_start]F2 --> F2b(生物学特性: 复胃 [cite: 7210, 7256][cite_start], 反刍 [cite: 7257][cite_start], 草食 [cite: 7255]);
    [cite_start]F2 --> F2c(品种: 中国荷斯坦(奶) [cite: 7341][cite_start], 西门塔尔(兼) [cite: 7350, 7351][cite_start], 夏洛来(肉) [cite: 7355, 7356][cite_start], 利木赞(肉) [cite: 7361, 7362][cite_start], 安格斯(肉) [cite: 7371, 7373]);
    [cite_start]F2 --> F2d(奶牛生产)[cite: 7399, 7400, 7404];
    [cite_start]F2d1(TMR (全混合日粮) 技术)[cite: 7130, 7131];
    [cite_start]F2d2(生产阶段: 犊牛 (0-6月) [cite: 7405] [cite_start]-> 育成牛 (7-14月) [cite: 7405] [cite_start]-> 成年母牛 (泌乳期/干奶期) [cite: 7406]);
    [cite_start]F2d3(犊牛护理: 必喂初乳 (含免疫球蛋白))[cite: 7477, 7480];
    [cite_start]F2d4(泌乳周期: 泌乳期 (305天) [cite: 7563] + [cite_start]干奶期 (60天) [cite: 7566][cite_start]，干奶期对乳腺重构重要 [cite: 7685, 7620]);
    [cite_start]F --> F3(养羊生产)[cite: 1878, 1892];
    [cite_start]F3 --> F3a(遗传: 绵羊 (27对染色体) [cite: 1920] [cite_start]vs 山羊 (30对染色体) [cite: 1922]);
    [cite_start]F3 --> F3b(现状: 2024年出栏3.23亿头 [cite: 6402][cite_start], 产量518万吨 [cite: 6403]);
    [cite_start]F3 --> F3c(生物学特性: 绵羊 (温顺) [cite: 2362, 2363] [cite_start]vs 山羊 (活泼/好动) [cite: 2364][cite_start], 均喜干燥 [cite: 2341, 2347][cite_start], 耐寒怕热 [cite: 2343, 2349]);
    [cite_start]F3 --> F3d(品种: 小尾寒羊 (肉) [cite: 2423, 2509][cite_start], 湖羊 (羔皮) [cite: 2423][cite_start], 滩羊 (裘皮) [cite: 2423][cite_start], 布尔羊 (肉) [cite: 2423][cite_start], 萨能 (奶) [cite: 2426]);
    [cite_start]F --> F4(养禽生产)[cite: 1605, 1615];
    [cite_start]F4 --> F4a(现状: 2024年禽肉产量2660万吨 (世界第一))[cite: 4370, 4452, 6236, 6268];
    [cite_start]F4 --> F4b(现代特点: 集约化、机械化、自动化、配套化)[cite: 1624, 1625, 1626, 1627];
    [cite_start]F4 --> F4c(生物学特性: 无牙 (有肌胃) [cite: 1659, 1662][cite_start]，有气囊 [cite: 1663, 1732][cite_start]，卵生 (仅左侧卵巢发育) [cite: 1666]);
    [cite_start]F4 --> F4d(品种: 来航鸡 (蛋) [cite: 1782][cite_start], 科尼什 (肉) [cite: 1816][cite_start], 洛岛红 (兼) [cite: 1791][cite_start], 乌骨鸡 (药) [cite: 1778, 1829]);
```
