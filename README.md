# sentence-splitter-lite

健壮的中英文分句小工具。零第三方依赖，纯字符扫描实现，专门处理各种句末边界。

## 处理的边界情况

- **英文缩写**：`Dr. Smith`、`U.S.`、`3 p.m.` 不会被误切；
- **小数点**：`3.14159`、`$9.99` 不误判为句末；
- **省略号**：`Wait...`、`他沉默了……` 整体附着在句尾；
- **感叹/问号叠加**：`Really?!`、`这怎么可能！？` 视为一个句末；
- **引号/括号**：`He said "Hello."` 闭合引号随句吸收。

## 快速开始

```bash
python3 cli.py "Dr. Smith bought it for $3.14. Wait... really?!"
# 1. Dr. Smith bought it for $3.14.
# 2. Wait... really?!
```

## 使用示例

```bash
# JSON 数组输出
python3 cli.py --json "你好。世界！"

# 管道输入
echo "The value is 3.14. Done." | python3 cli.py
```

## 无 API Key 如何运行

本工具**完全不需要 API Key**，分句为本地规则计算。

## 目录结构

```
sentence-splitter-lite/
├── splitter.py   # 核心分句逻辑
├── cli.py        # 命令行入口
├── tests/
│   └── test_splitter.py
├── README.md
├── LICENSE
└── .gitignore
```

## 测试

```bash
python3 -m unittest discover -s tests
```

## 许可证

[MIT](./LICENSE)
