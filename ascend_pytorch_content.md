# 昇腾PyTorch插件深度解析与性能调优指南

> 本文基于 Ascend/pytorch 官方仓库深度解析。

## 第一章 项目概述
torch_npu 是 PyTorch 框架连接昇腾 NPU 硬件的核心适配层，其使命是实现 PyTorch 原生算子与昇腾底层 CANN 架构的无缝映射。

## 第四章 算子融合技术拆解
算子融合（Operator Fusion）是提升 NPU 计算性能的核心秘密武器，它通过将 Conv+Bias+ReLU 等多个算子合并为一个计算内核，减少了 NPU 频繁读写内存的次数。

## 第五章 HCCL 分布式训练
HCCL 提供了多机多卡通信的高速公路，通过集合通信算子（AllReduce/Broadcast等）实现了 NPU 卡间的高效协作。

## 第九章 硬件覆盖与支持
本插件全面支持 Atlas 训练与推理系列：
- **Atlas 训练系列**：包括 Atlas 900、Atlas 800 (9000/9010) 以及 Atlas A2 系列。
- **Atlas 推理系列**：支持 Atlas 800I A2/A3、Atlas 300I/T A3 等多款高性能计算卡。
