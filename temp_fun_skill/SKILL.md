---
name: temp-fun-skill
description: Temporary fun skills collection with jokes, games, and entertainment. Use when you need quick entertainment, jokes, or simple games.
---

# Temporary Fun Skills

由于clawhub速率限制，这是一个临时娱乐技能集合。

## 可用功能

### 1. 讲笑话
```bash
python3 -c "import random; jokes=['为什么程序员讨厌自然？因为太多bugs！','为什么AI不会打架？因为它们总是神经网络！']; print(random.choice(jokes))"
```

### 2. 猜数字游戏
```bash
python3 -c "import random; number=random.randint(1,10); print('猜一个1-10的数字！'); guess=int(input('你的猜测: ')); print('正确！' if guess==number else f'不对，数字是{number}')"
```

### 3. 硬币翻转
```bash
python3 -c "import random; result='正面' if random.random()>0.5 else '反面'; print(f'硬币翻转结果: {result}')"
```

## 使用方式

直接运行上述Python代码，或让我帮您执行。
