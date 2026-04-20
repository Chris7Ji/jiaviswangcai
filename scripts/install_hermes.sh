#!/bin/bash

# Hermes Agent 独立安装脚本 (Standalone)
# 安装目录: ~/hermes-standalone

HERMES_DIR="$HOME/hermes-standalone"

echo "正在准备 Hermes Agent 独立部署环境..."

# 1. 创建独立目录
mkdir -p "$HERMES_DIR"
cd "$HERMES_DIR" || exit

# 2. 创建虚拟环境
echo "创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 3. 克隆代码
echo "下载 Hermes Agent 源码..."
git clone https://github.com/nousresearch/hermes-agent.git .

# 4. 安装依赖
echo "安装依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. 生成配置文件
echo "配置环境变量..."
cat <<EOF > .env
# Hermes Agent 独立运行配置
MINIMAX_API_KEY=YOUR_API_KEY_HERE
HERMES_DB_PATH=./hermes_data.db
EOF

echo "----------------------------------------------------"
echo "安装完成！"
echo "独立运行目录: $HERMES_DIR"
echo "请进入目录并修改 .env 文件中的 API Key 后执行:"
echo "cd ~/hermes-standalone && source venv/bin/activate && python main.py"
echo "----------------------------------------------------"
