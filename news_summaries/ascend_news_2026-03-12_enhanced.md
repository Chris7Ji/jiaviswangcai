# 🚀 华为昇腾生态日报 - 2026年03月12日

## 📊 今日概览
- 精选动态：**14条**（中文7条，英文7条）
- 覆盖领域：芯片/超节点/软件栈/生态/应用
- 质量评级：⭐⭐⭐⭐⭐

---

## 🎯 重磅发布

### 1. 华为发布昇腾950系列芯片路线图，2026年Q1上市
**📰 来源**：华为官方/华为全联接大会 | **⏰ 发布时间**：2025年9月 | **🌐 语言**：中/英

**📝 核心内容**：
华为在全联接大会2025上正式公布了未来三年的昇腾AI芯片路线图，包括Ascend 950PR、950DT、960和970四款芯片。这是华为首次系统性地披露AI芯片长期规划，标志着昇腾生态进入快速发展期。

**🔧 技术要点**：
- **涉及产品**：Ascend 950PR（推理预填充/推荐）、Ascend 950DT（训练/解码）、Ascend 960（2027Q4）、Ascend 970（2028Q4）
- **技术亮点**：
  - 950PR采用华为自研HiBL 1.0 HBM内存，成本低于HBM3E/HBM4E
  - 950DT配备HiZQ 2.0 HBM，144GB内存容量，4TB/s访存带宽，2TB/s互联带宽
  - 支持FP8/MXFP8/MXFP4/HiF8等低精度格式
  - 互联带宽提升至2.5倍（2TB/s）
- **性能数据**：950系列FP8/MXFP8/HiF8算力达1 PFLOPS，MXFP4达2 PFLOPS

**💡 应用价值**：
- **适用场景**：大模型训练、推理预填充/解码、推荐系统
- **开发者收益**：自研HBM降低成本，提升性价比；统一架构降低迁移成本
- **生态影响**：填补国产高端AI芯片空白，为MindSpore生态提供硬件基础

**🔗 相关链接**：
- 官方公告：https://www.huawei.com/cn/news/2025/9/hc-xu-keynote-speech
- 技术文档：https://www.hiascend.com/document
- 代码仓库：https://gitee.com/ascend

---

### 2. Atlas 950 SuperPoD超节点首次海外亮相MWC2026
**📰 来源**：华为官方/凤凰网科技 | **⏰ 发布时间**：2026年3月 | **🌐 语言**：中文

**📝 核心内容**：
华为在MWC2026巴塞罗那展会上首次向海外集中展示基于自研"灵衢"（UnifiedBus）互联协议的超节点系列算力产品。Atlas 950 SuperPoD支持8192张昇腾卡互联，是全球规模最大的AI超节点之一。

**🔧 技术要点**：
- **涉及产品**：Atlas 950 SuperPoD、TaiShan 950 SuperPoD
- **技术亮点**：
  - 全液冷AI超节点设计
  - 基于灵衢2.0互联协议，华为已决定开放该技术规范
  - 8192颗Ascend 950DT芯片互联
  - 互联带宽达16.3PB/s
- **性能数据**：FP4算力16EFLOPS，训练性能4.91M TPS，推理性能19.6M TPS

**💡 应用价值**：
- **适用场景**：超大规模AI模型训练、万亿参数模型推理
- **开发者收益**：超节点架构降低分布式训练复杂度
- **生态影响**：标志着中国AI基础设施达到世界领先水平

**🔗 相关链接**：
- 官方公告：https://www.huawei.com/cn/news/2025/9/hc-xu-keynote-speech
- 媒体报道：https://h5.ifeng.com/c/vivoArticle/v002-_6E6M6dbd--r0JvQvAUgyYjiyuNfJcMTPFMyvlr3Suo4__

---

### 3. 智谱AI GLM-5：首个完全基于昇腾生态的千亿参数大模型
**📰 来源**：Medium技术分析 | **⏰ 发布时间**：2026年2月 | **🌐 语言**：英文（已翻译）

**📝 核心内容**：
智谱AI（Zhipu AI，现品牌升级为Z.ai）于2026年2月11日发布GLM-5大模型，拥有7450亿参数，性能对标OpenAI GPT-5.2和Anthropic Claude Opus 4.5。该模型完全基于华为昇腾芯片和MindSpore框架训练，零依赖NVIDIA硬件。

**🔧 技术要点**：
- **涉及产品**：Ascend 910B芯片、MindSpore框架
- **技术亮点**：
  - 使用10万张Ascend 910B芯片训练
  - 完全基于MindSpore框架，无NVIDIA GPU参与
  - 在实体清单限制下实现技术突破
- **性能数据**：745B参数，性能对标GPT-5.2/Claude Opus 4.5

**💡 应用价值**：
- **适用场景**：通用大语言模型、企业级AI应用
- **开发者收益**：证明国产全栈AI方案可行性
- **生态影响**：里程碑式突破，验证昇腾+MindSpore可支撑前沿大模型训练

**🔗 原文链接**：https://thamizhelango.medium.com/mindspore-zhipu-ai-huawei-ascend-how-china-built-a-frontier-ai-model-without-a-single-nvidia-68403d92cedb

---

### 4. DeepSeek V4：万亿参数模型原生支持昇腾优化
**📰 来源**：Digital Applied | **⏰ 发布时间**：2026年3月 | **🌐 语言**：英文（已翻译）

**📝 核心内容**：
DeepSeek V4预计将于2026年Q1-Q2发布，拥有约1万亿参数、100万token上下文窗口，并原生支持华为Ascend 910B/C硬件优化。这是首个针对非NVIDIA生态优化的万亿参数开源模型。

**🔧 技术要点**：
- **涉及产品**：Ascend 910B/C、CANN、MindSpore
- **技术亮点**：
  - 稀疏MoE架构，每次推理激活约320亿参数
  - 原生多模态（文本+视觉+音频）
  - 定制CANN算子和MindSpore适配层
  - FP8训练优化，适配Ascend原生FP8支持
- **性能数据**：~1T总参数，~32B激活参数，1M上下文长度

**💡 应用价值**：
- **适用场景**：企业级文档处理、代码分析、多模态理解
- **开发者收益**：开源权重可本地部署，降低API依赖
- **生态影响**：推动昇腾生态在国际开源社区的影响力

**🔗 原文链接**：https://www.digitalapplied.com/blog/deepseek-v4-trillion-parameter-open-source-multimodal

---

### 5. 华为2026年计划生产60万颗昇腾910C芯片
**📰 来源**：ABHS行业分析 | **⏰ 发布时间**：2026年 | **🌐 语言**：英文（已翻译）

**📝 核心内容**：
华为计划在2026年生产约60万颗Ascend 910C AI芯片，较2025年产量几乎翻倍。包括其他昇腾型号在内，今年可能向中国AI行业分发多达160万颗芯片。主要客户包括阿里巴巴、腾讯和DeepSeek。

**🔧 技术要点**：
- **涉及产品**：Ascend 910C、SMIC 7nm工艺
- **技术亮点**：
  - 基于中芯国际增强型7nm工艺
  - 采用自研HBM技术
  - 单芯片BF16性能约670 TFLOPS
- **性能数据**：
  | 规格 | 昇腾910C | NVIDIA B200 |
  |------|---------|-------------|
  | 工艺节点 | SMIC 7nm | TSMC 4nm |
  | BF16性能 | ~670 TFLOPS | ~2,250 TFLOPS |
  | 内存带宽 | ~900 GB/s | ~8 TB/s |
  | 2026产量目标 | 60万颗 | 未披露 |

**💡 应用价值**：
- **适用场景**：AI推理、中小规模训练
- **开发者收益**：国产替代方案，供应链安全
- **生态影响**：大规模量产降低算力成本，推动生态普及

**🔗 原文链接**：https://www.abhs.in/blog/huawei-ascend-910c-china-nvidia-alternative-2026

---

### 6. 从PyTorch/TensorFlow迁移到MindSpore：工程模型适配指南
**📰 来源**：Developer Tech | **⏰ 发布时间**：2025年6月 | **🌐 语言**：英文（已翻译）

**📝 核心内容**：
华为推出了CloudMatrix 384 AI芯片集群，用于大规模AI模型训练。该系统通过光互连的高密度昇腾910C处理器网络，在能效和训练速度方面实现了提升。尽管单颗昇腾芯片性能不及西方竞争对手的顶级GPU，但该系统整体性能据称可超越基于GPU的集群。

**🔧 技术要点**：
- **框架迁移**：从PyTorch/TensorFlow迁移到MindSpore
- **MindConverter工具**：帮助转换模型定义，但需手动调整和微调
- **MindIR格式**：MindSpore中间表示，用于跨平台部署的静态图表示
- **CANN适配**：华为的计算架构（类似NVIDIA CUDA），包括ACL计算库、运行时和调优工具
- **执行模式**：GRAPH_MODE（预编译计算图，性能更好）vs PYNATIVE_MODE（即时执行，便于调试）

**💡 应用价值**：
- **适用场景**：已有PyTorch/TensorFlow模型的迁移
- **开发者收益**：提供完整的迁移工具和文档支持
- **生态影响**：降低从CUDA生态迁移到昇腾生态的门槛

**🔗 原文链接**：https://www.developer-tech.com/news/adapting-engineering-models-to-huaweis-ai-learning-framework/

---

### 7. 重构以获更好结果：华为AI技术栈深度解析
**📰 来源**：AI News | **⏰ 发布时间**：2025年10月 | **🌐 语言**：英文（已翻译）

**📝 核心内容**：
华为发布了CloudMatrix 384 AI芯片集群，这是一个用于AI学习的新系统。它采用通过光链路连接的昇腾910C处理器集群。分布式架构意味着该系统在资源利用率和芯片时间方面可以超越传统的GPU硬件设置，尽管单颗昇腾芯片的性能低于竞争对手。

**🔧 技术要点**：
- **框架迁移**：从PyTorch/TensorFlow到MindSpore的转换
- **MindIR部署**：使用mindspore.export将训练好的网络转换为MindIR格式
- **CANN工具链**：Profiler、MindStudio、Operator Tuner用于运行时性能调优
- **执行模式**：GRAPH_MODE（预编译）vs PYNATIVE_MODE（即时执行）

**💡 应用价值**：
- **适用场景**：企业级AI应用开发和部署
- **开发者收益**：提供详细的迁移指南和优化工具
- **生态影响**：帮助开发者理解和适应华为AI技术栈

**🔗 原文链接**：https://www.artificialintelligence-news.com/news/re-engineering-for-better-results-the-huawei-ai-stack/

---

## 🧩 技术动态

### 8. Ascend C自定义算子开发指南更新
**📰 来源**：MindSpore官方文档 | **🌐 语言**：中文

MindSpore 2.3.1版本更新了Ascend C自定义算子开发指南，提供从开发到部署的完整流程：
- **开发阶段**：使用Ascend C编程语言快速开发自定义算子
- **编译部署**：离线编译确保算子在昇腾AI处理器高效运行
- **框架集成**：通过`ops.Custom`接口集成到MindSpore

**关键API**：
```python
ops.Custom(func="aclnnAddCustom", out_shape=out_shape, 
           out_dtype=lambda x, _: x, func_type="aot")
```

**链接**：https://www.mindspore.cn/tutorials/experts/zh-CN/r2.3.1/operation/op_custom_ascendc.html

---

### 9. MindSpore模型迁移最佳实践
**📰 来源**：华为云社区 | **🌐 语言**：中文

华为云ModelArts平台提供完整的PyTorch/TensorFlow到MindSpore的迁移方案：
- **MindConverter工具**：自动转换模型定义，支持API映射
- **MindIR格式**：跨平台部署的静态图表示
- **GRAPH_MODE/PYNATIVE_MODE**：灵活切换动态图和静态图

**迁移要点**：
- 注意算子行为差异（如卷积padding模式）
- 权重初始化方法可能需要调整
- 使用CANN Profiler进行性能调优

**链接**：https://www.developer-tech.com/news/adapting-engineering-models-to-huaweis-ai-learning-framework/

---

### 10. 昇腾社区CANN版本更新
**📰 来源**：昇腾社区 | **🌐 语言**：中文

昇腾社区持续更新CANN（Compute Architecture for Neural Networks）版本，提供：
- 算子库扩展
- 通信库优化
- 图引擎升级
- 毕昇编译器改进

**链接**：https://www.hiascend.com/productbulletins

---

## 🌐 生态建设

### 11. 软通动力：华为昇腾AI软件生态龙头
**📰 来源**：东方财富 | **🌐 语言**：中文

软通动力作为华为生态中稀缺的「双钻石、全栈式」核心伙伴，深度参与华为CANN异构计算架构、MindSpore昇思框架的核心生态共建。公司是昇腾AI软件生态的绝对龙头，合作层级与技术深度远超同业。

**链接**：https://caifuhao.eastmoney.com/news/20260309194421973974530

---

### 12. 华为Atlas 950 SuperCluster：全球最强AI集群
**📰 来源**：Convequity技术分析 | **⏰ 发布时间**：2025年9月 | **🌐 语言**：英文（已翻译）

**📝 核心内容**：
Atlas 950 SuperCluster由64个互联的Atlas 950超节点组成，集成超过52万颗Ascend 950DT芯片，总算力达524 EFLOPS（FP8）。

**技术亮点**：
- 支持UBoE和RoCE协议
- UBoE相比传统RoCE具有更低静态延迟、更高可靠性
- 2026年Q4上市

**系统级性能对比**：
- 与NVIDIA NVL144（2026年下半年上市）相比：规模是56.8倍，总算力是6.7倍，内存容量是15倍，互联带宽是62倍
- 与NVIDIA NVL576（2027年计划）相比：Atlas 950超节点在各方面仍具优势

**集群规模**：
- Atlas 950 SuperCluster：64个超节点互联，52万+颗950DT芯片，524 EFLOPS FP8
- Atlas 960 SuperCluster（2027Q4）：百万卡级别，2 ZFLOPS FP8 / 4 ZFLOPS FP4

**🔗 原文链接**：https://convequity.substack.com/p/huawei-ascend-ai-chip-roadmap-and

---

### 13. 华为公布三年昇腾AI芯片路线图，950将于2026年推出
**📰 来源**：Huawei Central | **⏰ 发布时间**：2025年9月 | **🌐 语言**：英文（已翻译）

**📝 核心内容**：
华为在2025年9月18日的Connect 2025大会上宣布了新的昇腾AI芯片路线图。轮值董事长徐直军宣布将于2026年推出Ascend 950 AI芯片，并透露未来几代AI芯片的计划。

**产品规划**：
- **Ascend 950PR**：2026年Q1上市，首款采用华为自研HBM技术的芯片，针对推理预填充和推荐服务优化
- **Ascend 950DT**：2026年Q4上市，针对解码和训练优化，提升内存容量和带宽
- **Ascend 960**：2027年Q4上市，规格和框架仍在规划中
- **Ascend 970**：2028年Q4上市，目标FP4和FP8算力较960翻倍

**技术特点**：
- 950系列支持低精度数据格式，向量计算能力增强
- 互联带宽增加2.5倍
- 自研HBM技术是最大亮点

**🔗 原文链接**：https://www.huaweicentral.com/huawei-reveals-3-year-ascend-ai-chip-roadmap-950-coming-in-2026/

---

## 📚 开发者资源

### 14. MindSpore迁移指南：环境准备与资料获取
**📰 来源**：MindSpore官方文档 | **🌐 语言**：中文

MindSpore 2.0文档提供详细的模型迁移指南，包括：
- 开发环境配置
- MindSpore组件（models/Hub）介绍
- 云上训练教程（ModelArts）
- API映射参考

**链接**：https://www.mindspore.cn/docs/zh-CN/r2.0/migration_guide/enveriment_preparation.html

---

### 15. 昇腾开发资源下载中心
**📰 来源**：昇腾社区 | **🌐 语言**：中文

昇腾社区提供一站式开发资源下载：
- CANN商用版/社区版
- MindStudio全流程开发工具链
- 固件与驱动
- Ascend Deployer部署工具

**链接**：https://www.hiascend.com/developer/download

---

### 16. 构筑开放基础软件栈，共建昇腾AI算力新生态
**📰 来源**：华为技术期刊 | **🌐 语言**：中文

华为发布技术白皮书，阐述昇腾AI软件栈战略：
- MindSpore创新动静结合模式
- 支持AI与科学计算融合编程
- 全场景部署能力（云/边/端）

**链接**：https://www.huawei.com/cn/huaweitech/publication/202503/new-ecology-of-ascend-computing-power

---

## 📈 趋势洞察

2026年是昇腾生态发展的关键之年。从华为公布的三年路线图来看，昇腾950/960/970系列将遵循"一年一代、算力翻倍"的节奏持续演进，目标在单芯片性能上逐步缩小与NVIDIA的差距。更重要的是，华为通过"超节点+集群"的架构创新，在系统层面实现了差异化竞争优势——Atlas 950 SuperPoD和SuperCluster的推出，标志着国产AI基础设施已具备支撑万亿参数大模型训练的能力。

从生态角度看，智谱AI GLM-5和DeepSeek V4等前沿模型选择昇腾作为训练平台，验证了国产全栈方案的可行性。随着60万颗昇腾910C的量产和950系列的上市，昇腾生态正从"可用"走向"好用"，有望在2026-2027年迎来爆发式增长。

---
*报告生成时间：2026-03-12 13:50 | 数据来源：华为官方 + 全球技术社区*
