# 华为昇腾CANN知识库

> 来源: GitCode/Github Ascend开源社区
> 更新时间: 2026-03-09
> 维护: 昇腾AI官

---

## CANN (Compute Architecture for Neural Networks)

### 概述
CANN是华为针对AI场景推出的异构计算架构，对上支持多种AI框架，对下服务AI处理器与编程，发挥承上启下的关键作用，是提升昇腾AI处理器计算效率的关键平台。

### 核心功能
- 支持多种AI框架（PyTorch、TensorFlow等）
- 提供高效的异构计算能力
- 为AI处理器提供编程接口
- 提供容器化部署支持

---

## 昇腾开源项目

### 1. cann-container-image
**仓库**: https://github.com/Ascend/cann-container-image
**功能**: CANN容器镜像Dockerfile
**许可证**: Apache-2.0

**核心内容**:
- 提供CANN的Docker容器化方案
- 支持NPU设备挂载（/dev/davinci1等）
- 包含驱动和运行时环境配置
- 镜像发布到AscendHub/DockerHub/Quay.io

**使用示例**:
```bash
docker run \
  --name cann_container \
  --device /dev/davinci1 \
  --device /dev/davinci_manager \
  --device /dev/devmm_svm \
  --device /dev/hisi_hdc \
  -v /usr/local/dcmi:/usr/local/dcmi \
  -v /usr/local/bin/npu-smi:/usr/local/bin/npu-smi \
  -v /usr/local/Ascend/driver/lib64/:/usr/local/Ascend/driver/lib64/ \
  -it ascendai/cann:latest bash
```

**文档**: https://www.hiascend.com/software/cann

---

### 2. op-plugin (算子插件)
**仓库**: https://github.com/Ascend/op-plugin
**功能**: Ascend Extension for PyTorch算子插件
**中文名**: 昇腾PyTorch算子插件

**核心功能**:
- 为PyTorch框架提供NPU算子库调用能力
- 支持自定义算子开发
- 提供算子适配文件

**版本对应关系**:
| op-plugin分支 | Ascend Extension for PyTorch版本 |
|--------------|----------------------------------|
| master | 主线版本（如v2.1.0等） |
| 7.1.0 | 7.1.0版本（如v2.1.0-7.1.0） |
| 7.0.0 | 7.0.0版本（如v2.1.0-7.0.0） |
| 6.0.rc3 | 6.0.rc3版本 |
| 5.0.0 | 5.0.0版本 |

**编译要求**:
- ARM架构: GCC 10.2
- X86架构: GCC 9.3.1（PyTorch 2.6.0+推荐GCC 11.2.1）

**支持的PyTorch版本**:
- v2.1.0, v2.3.1, v2.4.0, v2.5.1, v2.6.0, v2.7.1, v2.8.0, master

**编译步骤**:
```bash
# 1. 配置CANN环境
source /usr/local/Ascend/ascend-toolkit/set_env.sh

# 2. 克隆代码
git clone --branch master https://gitcode.com/ascend/op-plugin.git
cd op-plugin

# 3. 编译构建
bash ci/build.sh --python=3.8 --pytorch=v2.1.0

# 4. 安装
pip3 install --upgrade dist/torch_npu-*.whl
```

**支持的训练设备**:
- Atlas 800 训练服务器（型号：9000/9010）
- Atlas 900 PoD（型号：9000）
- Atlas 300T/300T Pro 训练卡
- Atlas 800T A2 训练服务器
- Atlas 900 A2 PoD 集群基础单元
- Atlas 200T A2 Box16 异构子框
- Atlas 800T A3 训练服务器
- Atlas 900 A3 SuperPoD 超节点

**支持的推理设备**:
- Atlas 800I A2 推理服务器

---

### 3. TorchAir (图模式推理)
**仓库**: https://github.com/Ascend/torchair
**功能**: Torch Ascend Intermediate Representation
**功能**: 支持PyTorch在昇腾NPU上使用图模式进行推理

**核心特性**:
- 继承PyTorch Dynamo模式
- 将FX图转换为GE计算图
- 支持GE计算图在昇腾NPU的编译与执行
- 提供图模式推理能力

**版本配套表**:
| TorchAir | PyTorch | torch_npu | CANN | Python |
|----------|---------|-----------|------|--------|
| master | 2.6.0+ | 在研 | 在研 | 3.9/3.10/3.11/3.12 |
| 7.3.0 | 2.6.0/2.7.1/2.8.0 | 7.3.0 | 8.5.0 | 3.9/3.10/3.11 |
| 7.2.0 | 2.1.0 | 7.2.0 | 8.3.RC1 | 3.8/3.9/3.10/3.11 |
| 7.1.0 | 2.1.0 | 7.1.0 | 8.2.RC1 | 3.8/3.9/3.10/3.11 |
| 7.0.0 | 2.1.0/2.3.1/2.4.0 | 7.0.0 | 8.1.RC1 | 3.8/3.9/3.10/3.11 |

**安装步骤**:
```bash
# 1. 克隆代码
git clone https://gitcode.com/ascend/torchair.git
cd torchair
git submodule update --init --recursive

# 2. 配置
cd ./torchair
bash ./configure

# 3. 编译
mkdir build && cd build
cmake ..
make torchair -j8

# 4. 安装
make install_torchair
```

**快速验证**:
```python
import torch
import torchair

config = torchair.CompilerConfig()
npu_backend = torchair.get_npu_backend(compiler_config=config)

class Model(torch.nn.Module):
    def forward(self, x, y):
        return torch.add(x, y)

model = Model()
model = torch.compile(model, backend=npu_backend, dynamic=False)
x = torch.randn(2, 2)
y = torch.randn(2, 2)
model(x, y)
```

**高级特性**:
- 日志功能
- Graph dump功能
- Dynamo export功能（air格式图导出）
- Data dump功能（精度数据dump）
- Graph fusion功能（自定义融合算子）
- Experimental性能提升功能
- Converter功能拓展

---

## 其他昇腾项目

### 4. mind-cluster
**仓库**: https://github.com/Ascend/mind-cluster
**语言**: Go
**功能**: 昇腾集群管理

### 5. AscendNPU-IR
**仓库**: https://github.com/Ascend/AscendNPU-IR
**语言**: C++
**许可证**: Apache-2.0
**功能**: 昇腾NPU中间表示

### 6. SDK项目
- **AgentSDK**: Python SDK
- **MultimodalSDK**: C++多模态SDK
- **IndexSDK**: C++索引SDK
- **RecSDK**: C++推荐SDK

---

## 关键资源链接

### 官方文档
- 昇腾文档中心: https://www.hiascend.com/document
- CANN文档: https://www.hiascend.com/software/cann
- TorchAir使用指南: https://www.hiascend.com/document/detail/zh/Pytorch/720/modthirdparty/torchairuseguide/

### 社区资源
- 昇腾社区论坛: https://www.hiascend.com/forum/
- AscendHub: https://www.hiascend.com/developer/ascendhub/
- GitCode Ascend: https://gitcode.com/ascend
- GitHub Ascend: https://github.com/ascend

### 容器镜像
- DockerHub: https://hub.docker.com/r/ascendai/cann/tags
- Quay.io: https://quay.io/repository/ascend/cann

---

## 技术要点总结

### 模型迁移流程
1. 安装CANN工具包
2. 安装torch_npu插件
3. 安装op-plugin算子插件
4. 使用ATC转换模型或使用TorchAir图模式
5. 在昇腾NPU上运行推理/训练

### 算子开发要点
- 使用TBE DSL进行自定义算子开发
- 通过op-plugin提供PyTorch算子适配
- 注意版本配套关系
- 遵循GCC版本要求

### 调试技巧
- 使用npu-smi查看NPU状态
- 配置CANN环境变量（set_env.sh）
- 使用TorchAir的data dump功能进行精度对比
- 使用graph dump功能查看计算图

---

---

## PyTorch昇腾适配 (torch_npu)

### 概述
**仓库**: https://github.com/ascend/pytorch
**功能**: Ascend Extension for PyTorch - 昇腾NPU适配PyTorch的插件
**名称**: torch_npu

### 核心功能
- 为PyTorch提供昇腾NPU计算能力
- 支持Ascend AI处理器的强大算力
- 提供与PyTorch原生API兼容的接口

### 安装方法

**快速安装（推荐）**:
```bash
# 1. 安装PyTorch
# For Aarch64:
pip3 install torch==2.1.0

# For x86:
pip3 install torch==2.1.0+cpu --index-url https://download.pytorch.org/whl/cpu

# 2. 安装依赖
pip3 install pyyaml setuptools

# 3. 安装torch_npu
pip3 install torch-npu==2.1.0.post17
```

**源码编译安装**:
```bash
# 1. 克隆代码
git clone https://github.com/ascend/pytorch.git -b 2.1.0-7.2.0 --depth 1

# 2. 构建Docker镜像
cd pytorch/ci/docker/{arch}  # {arch}为X86或ARM
docker build -t manylinux-builder:v1 .

# 3. 进入容器编译
docker run -it -v /{code_path}/pytorch:/home/pytorch manylinux-builder:v1 bash
cd /home/pytorch
bash ci/build.sh --python=3.8

# 4. 安装编译产物
pip3 install --upgrade dist/torch_npu-*.whl
```

### 版本配套表

| PyTorch版本 | 支持的Python版本 |
|------------|-----------------|
| 1.11.0 | 3.7.x(>=3.7.5), 3.8.x, 3.9.x, 3.10.x |
| 2.1.0 | 3.8.x, 3.9.x, 3.10.x, 3.11.x |
| 2.2.0 | 3.8.x, 3.9.x, 3.10.x |
| 2.3.1 | 3.8.x, 3.9.x, 3.10.x, 3.11.x |
| 2.4.0 | 3.8.x, 3.9.x, 3.10.x, 3.11.x |
| 2.5.1 | 3.9.x, 3.10.x, 3.11.x |
| 2.6.0+ | 3.9.x, 3.10.x, 3.11.x |

### CANN与PyTorch版本对应关系

| CANN版本 | PyTorch版本 | Extension版本 | Github分支 |
|---------|------------|--------------|-----------|
| 8.5.0 | 2.9.0 | 2.9.0 | v2.9.0-7.3.0 |
| 8.5.0 | 2.8.0 | 2.8.0.post2 | v2.8.0-7.3.0 |
| 8.3.RC1 | 2.1.0 | 2.1.0.post17 | v2.1.0-7.2.0 |
| 8.2.RC1 | 2.1.0 | 2.1.0.post13 | v2.1.0-7.1.0 |
| 8.1.RC1 | 2.1.0 | 2.1.0.post12 | v2.1.0-7.0.0 |

### 快速验证
```python
import torch
import torch_npu  # torch_npu 2.5.1+版本不再需要显式导入

x = torch.randn(2, 2).npu()
y = torch.randn(2, 2).npu()
z = x.mm(y)
print(z)
```

### 维护策略

| PyTorch版本 | 维护策略 | 当前状态 | 发布日期 | EOL日期 |
|------------|---------|---------|---------|---------|
| 2.9.0 | Regular Release | Development | 2025/10/15 | - |
| 2.8.0 | Regular Release | Development | 2025/10/15 | - |
| 2.7.1 | Long Term Support | Development | 2025/10/15 | 2026/10/15 |
| 2.6.0 | Regular Release | Development | 2025/07/25 | 2026/01/15 |
| 2.5.1 | Regular Release | Maintained | 2024/11/08 | 2026/08/08 |
| 2.4.0 | Regular Release | Maintained | 2024/10/15 | 2026/06/15 |
| 2.3.1 | Regular Release | Maintained | 2024/06/06 | 2026/06/07 |
| 2.2.0 | Regular Release | EOL | 2024/04/01 | 2025/10/14 |
| 2.1.0 | Long Term Support | Maintained | 2023/10/15 | 2026/12/30 |
| 1.11.0 | Long Term Support | EOL | 2023/04/19 | 2025/10/25 |

---

## MindSpore框架

### 概述
**仓库**: https://github.com/ascend/mindspore
**功能**: 开源深度学习训练/推理框架
**定位**: 端边云全场景AI计算框架

### 核心特性

#### 1. 自动微分 (Automatic Differentiation)
- 基于源码转换（Source Transformation, ST）
- 相比PyTorch的算子重载（OO），支持编译时优化
- 支持复杂控制流、高阶函数和闭包
- 实现程序本身的符号微分

#### 2. 自动并行 (Automatic Parallel)
- 结合数据并行、模型并行、混合并行
- 自动选择最优模型切分策略
- 细粒度算子拆分，开发者无需关注底层实现

### 支持平台

| 硬件平台 | 操作系统 | 状态 |
|---------|---------|------|
| Ascend910 | Ubuntu-x86 | ✅ |
| Ascend910 | Ubuntu-aarch64 | ✅ |
| Ascend910 | EulerOS-aarch64 | ✅ |
| Ascend910 | CentOS-x86 | ✅ |
| GPU CUDA 10.1 | Ubuntu-x86 | ✅ |
| CPU | Ubuntu-x86 | ✅ |
| CPU | Ubuntu-aarch64 | ✅ |
| CPU | Windows-x86 | ✅ |

### 安装方法

**pip安装（CPU版本示例）**:
```bash
pip install https://ms-release.obs.cn-north-4.myhuaweicloud.com/1.2.0-rc1/MindSpore/cpu/ubuntu_x86/mindspore-1.2.0rc1-cp37-cp37m-linux_x86_64.whl
```

**Docker镜像**:
```bash
# CPU版本
docker pull mindspore/mindspore-cpu:1.1.0
docker run -it mindspore/mindspore-cpu:1.1.0 /bin/bash

# GPU版本（需安装nvidia-container-toolkit）
docker pull mindspore/mindspore-gpu:1.1.0
docker run -it -v /dev/shm:/dev/shm --runtime=nvidia --privileged=true mindspore/mindspore-gpu:1.1.0 /bin/bash
```

### 快速入门
```python
import numpy as np
import mindspore.context as context
import mindspore.nn as nn
from mindspore import Tensor
from mindspore.ops import operations as P

context.set_context(mode=context.GRAPH_MODE, device_target="CPU")

class Mul(nn.Cell):
    def __init__(self):
        super(Mul, self).__init__()
        self.mul = P.Mul()
    
    def construct(self, x, y):
        return self.mul(x, y)

x = Tensor(np.array([1.0, 2.0, 3.0]).astype(np.float32))
y = Tensor(np.array([4.0, 5.0, 6.0]).astype(np.float32))

mul = Mul()
print(mul(x, y))
# [ 4. 10. 18.]
```

### 维护状态

| 分支 | 状态 | 初始发布 | 下一阶段 | EOL日期 |
|------|------|---------|---------|---------|
| r1.7 | Maintained | 2022-04-29 | Unmaintained | 2023-04-29 |
| r1.6 | Maintained | 2022-01-29 | Unmaintained | 2023-01-29 |
| r1.5 | Maintained | 2021-10-15 | Unmaintained | 2022-10-15 |
| r1.4 | Maintained | 2021-08-15 | Unmaintained | 2022-08-15 |
| r1.3 | Maintained | 2021-07-15 | Unmaintained | 2022-07-15 |
| r1.2 | EOL | 2021-04-15 | - | - |
| r1.1 | EOL | 2020-12-31 | - | 2021-09-30 |
| r1.0 | EOL | 2020-09-24 | - | 2021-07-30 |

---

## ModelZoo模型库

### 概述
**仓库**: https://github.com/ascend/ModelZoo-PyTorch
**功能**: 昇腾模型库，提供典型网络和预训练模型

### 目录结构

| 目录 | 说明 |
|------|------|
| ACL_PyTorch | 基于昇腾芯片的推理模型参考 |
| PyTorch | 基于昇腾芯片的训练模型参考 |
| AscendIE | 基于昇腾芯片的推理引擎模型参考 |

### 使用说明
- 提供公共数据集下载和预处理脚本
- 模型仅可用于非商业研究和教育
- 支持在Gitee或ModelZoo论坛提交需求

---

## 完整版本配套参考

### CANN 8.x系列

| CANN版本 | torch_npu | PyTorch | MindSpore | 状态 |
|---------|-----------|---------|-----------|------|
| 8.5.0 | 7.3.0 | 2.6-2.9 | - | 最新 |
| 8.3.RC1 | 7.2.0 | 2.1-2.8 | - | 稳定 |
| 8.2.RC1 | 7.1.0 | 2.1-2.6 | - | 稳定 |
| 8.1.RC1 | 7.0.0 | 2.1-2.5 | - | 稳定 |
| 8.0.0 | 6.0.0 | 2.1-2.4 | - | 维护 |

### 推荐组合
- **最新开发**: CANN 8.5.0 + torch_npu 7.3.0 + PyTorch 2.9.0
- **稳定生产**: CANN 8.3.RC1 + torch_npu 7.2.0 + PyTorch 2.1.0
- **长期支持**: CANN 8.2.RC1 + torch_npu 7.1.0 + PyTorch 2.1.0

---

*本知识库由昇腾AI官维护，持续更新中...*
*最后更新: 2026-03-09*
*数据来源: GitCode/Github Ascend开源社区*
