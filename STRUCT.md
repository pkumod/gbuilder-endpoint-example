# 输入输出结构/格式

> gBuilder Endpoint 的全部数据都以 JSONL ([JSON Line](https://jsonlines.org)) 形式存储，即一行一个标准 JSON 对象。

在一行内，JSON 对象包括的键值与具体任务相关，具体如下所示：

**1. NER 模型**

输入：
```json
{"data": "我是待抽取的语料"}
```

输出：
```json
{"data": "我是待抽取的语料", "entity": ["实体1", "实体2"], "entity_type": ["实体1的类型", "实体2的类型"]}
```

**2. RE 模型**

输入：
```json
{"data": "我是待抽取的语料", "entity_pair": [["头实体1", "尾实体2"], ["头实体2", "尾实体2"]], "entity_type_pair": [["头实体1的类型", "尾实体2的类型"], ["头实体2的类型", "尾实体2的类型"]]}
```

输出：
```json
{"data": "我是待抽取的语料", "entity_pair": [["头实体1", "尾实体2"], ["头实体2", "尾实体2"]], "entity_type_pair": [["头实体1的类型", "尾实体2的类型"], ["头实体2的类型", "尾实体2的类型"]], "relation": ["第一个实体对之间的关系", "第二个实体对之间的关系"]}
```

> `entity_type_pair` 可选

**3. JE 模型**

输入：
```json
{"data": "我是待抽取的语料"}
```

输出：
```json
{"data": "我是待抽取的语料", "entity_pair": [["头实体1", "尾实体2"], ["头实体2", "尾实体2"]], "entity_type_pair": [["头实体1的类型", "尾实体2的类型"], ["头实体2的类型", "尾实体2的类型"]], "relation": ["第一个实体对之间的关系", "第二个实体对之间的关系"]}
```

> `entity_type_pair` 可选
