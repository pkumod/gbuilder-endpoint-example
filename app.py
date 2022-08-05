import json
import os
from http import HTTPStatus
from threading import Thread

from flask import Flask, jsonify, request, abort, send_from_directory

app = Flask(__name__)

# Endpoint status list:
AVAILABLE = 1
PENDING = 2
ERROR = 3

STATUS = AVAILABLE

# 用于记录正在执行的任务
RUNNING = None
THREAD = None


@app.route('/status', methods=['GET'])
def get_endpoint_status():
    """
    获取当前端点的状态
    :return: STATUS
    """
    global STATUS
    return jsonify({'status': STATUS})


@app.route('/tasks', methods=['POST'])
def create_task():
    """
    创建一个新的任务
    :return:
    """
    global STATUS, RUNNING, THREAD
    if STATUS == AVAILABLE:
        STATUS = PENDING
        req = request.form
        task_id = req['task_id']
        task_file = request.files['file']
        immediate = 'immediate' in req
        task_file.save(f'{task_id}_dataset')  # 将传输来的数据直接保存
        RUNNING = task_id
        if immediate:  # 如果是 immediate 任务，直接在主线程内阻塞执行该任务
            process(task_id)
        else:  # 如果是异步执行任务，则开一个新的线程执行任务，同时将线程对象存下来，便于后续的结束任务的操作
            THREAD = Thread(target=process, args=(task_id,))
            THREAD.start()
        return jsonify({'status': HTTPStatus.OK})
    else:
        abort(HTTPStatus.BAD_REQUEST)


def process(task_id):
    """
    处理指定的任务
    :param task_id:
    :return:
    """
    global STATUS, RUNNING, THREAD
    dataset = list(map(lambda line: json.loads(line),
                       open(f'{task_id}_dataset', 'r').read().strip().split('\n')))  # 处理 JSONL 格式的数据集
    # 假设本示例是一个 NER 模型，会将 {"data": data} 的数据进行处理，返回 {"entity": [xxx], "entity_type": [xxx]} 的数据
    result = []
    for line in dataset:
        result.append({'entity': ["示例"], 'entity_type': ["示例"], 'data': line['data']})
    # 将处理后的结果保存到文件中
    open(f'{task_id}_result', 'w').write('\n'.join(map(json.dumps, result)))
    # 状态回位
    STATUS = AVAILABLE
    RUNNING = None
    THREAD = None
    return True


@app.route('/tasks/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """
    获取指定任务的状态
    :param task_id:
    :return:
    """
    global RUNNING
    RUNNING = 0
    PENDING = 1  # 本示例只演示了单任务、单进程的端点服务，因此该状态无需使用
    FINISHED = 2
    ERROR = 3
    NO_TASK = -1
    if task_id == RUNNING:
        return jsonify({'status': RUNNING})
    else:
        if os.path.exists(f'{task_id}.finished'):  # 本示例中直接用一个文件来标记任务的状态
            return jsonify({'status': FINISHED})
        elif os.path.exists(f'{task_id}.error'):
            return jsonify({'status': ERROR})
        else:
            return jsonify({'status': NO_TASK})


@app.route('/tasks/<task_id>/results', methods=['GET'])
def get_task_result(task_id):
    """
    获取指定任务的结果
    :param task_id:
    :return:
    """
    if os.path.exists(f'{task_id}_result'):
        return send_from_directory(f'./train_tasks/{task_id}', f'{task_id}_result')
    else:
        abort(HTTPStatus.NOT_FOUND)


@app.route('/tasks/<task_id>', methods=['DELETE'])
def stop_task(task_id):
    """
    停止指定任务
    :param task_id:
    :return:
    """
    global STATUS, RUNNING, THREAD
    if task_id == RUNNING:
        STATUS = AVAILABLE
        if THREAD is not None:
            THREAD.terminate()
        RUNNING = None
        THREAD = None
        return jsonify({'status': HTTPStatus.OK})
    else:
        abort(HTTPStatus.BAD_REQUEST)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
