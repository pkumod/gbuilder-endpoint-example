# gBuilder Custom Endpoint Example

> gBuilder 自定义端点服务示例

## Intro

本 repo 提供了一个通过 Flask 构建 gBuilder 自定义 endpoint 的最简示例，用于演示如何构建自定义端点服务。通过本 repo 启用的自定义端点服务，可以成功注册至 gBuilder 模型中心（需要端点服务能被公网访问到）。

具体的实现请参照 `app.py` 中的内容，与本文的说明配合理解。

## Usage

1. 安装依赖：
    ```bash
    pip install -r requirements.txt
    ```
2. 启动服务：
    ```bash
    python app.py
    ```
3. 将服务地址添加至 gBuilder 模型中心。

> 如果您希望基于本示例直接实现 gBuilder endpoint，请修改 `app.py` 中的 `process` 函数的内容。

## Interface

gBuilder 自定义端点服务需要实现以下接口：

### 1. `status`

通过本接口，gBuilder 系统可以获知自定义 endpoint 的当前状态。

- 请求地址：`/status`
- 请求方式：GET
- 返回内容：
```json
{"status": STATUS}
```
- 状态值（STATUS）及说明：

| STATUS | Description |
|---|---|
| 1 | 当前Endpoint处于可用状态 |
| 2 | 当前Endpoint处于满载状态，需要等待前置任务完成 |
| 3 | 当前Endpoint处于错误状态，暂时无法提供服务 |

- 示例
```bash
curl http://localhost:5050/status
```
返回：
```JSON
{"status": 0}
```

### 2. `tasks`

通过本接口，gBuilder 可以向端点分派任务及数据，或获知当前端点上某个任务的执行状态

#### 2.1 POST `/tasks`

本接口接受 POST 请求，以向端点提交一个 Inference 任务。

- 请求地址：`/tasks`
- 请求方式：POST
- 接收字段：以 `form-data` 形式接收一下字段：


| Field | Description | Required |
|---|---|---|
| task_id | 用于区分不同任务的任务id | Y |
| task_file | 以文件形式传输的数据文件 | Y |
| immediate | 确定是否以异步的形式执行任务。如果是长时间推理任务需要将其设为 true，否则无需填写 | N |

- 返回内容：

```json
{"status": 200}
```

如果出现错误，会以对应错误码形式返回报错。


#### 2.2 GET `/tasks/<task_id>`

通过该接口，gBuilder 可以获知当前 Endpoint 上执行的 id 为 `<task_id>` 的任务的执行状态。

- 请求地址：`/tasks/<task_id>`
- 请求方式：GET
- 返回内容：
```json
{"status": STATUS}
```
- 状态值（STATUS）及说明：

| STATUS | Description |
|---|---|
| 0 | 该任务当前正在执行 |
| 1 | 该任务正在等待前置任务执行完成 |
| 2 | 该任务已经完成 |
| 3 | 执行该任务时发生了错误 |
| -1 | 该端点中没有对应 task_id 的任务 |


#### 2.3 GET `/tasks/<task_id>/results`

通过该接口，gBuilder 可以取得该任务的执行结果。

- 请求地址：`/tasks/<task_id>/results`
- 请求方式：GET (文件下载)
- 返回内容：以文件的形式返回处理好的数据

#### 2.4 DELETE `/tasks/<task_id>`

通过该接口，gBuilder 可以通知本端点即刻停止正在执行的 id 为 `<task_id>` 的任务。

- 请求地址：`/tasks/<task_id>`
- 请求方式：DELETE
- 返回内容：
```json
{"status": 200}
```

如果出现错误，会以对应错误码形式返回报错。

### Data Structure

请参考[数据结构](./STRUCT.md)中的内容，制定模型端点的输入输出。

### Summary

通过实现上述接口，即可以实现一个能够提供服务的 gBuilder Endpoint，可以在 gBuilder 模型中心中通过填写对应的端点地址，将自定义的端点加入 gBuilder 模型中心，从而在 gBuilder 知识图谱构建 Flowline 中提供服务。
