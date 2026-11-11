"""JSON 文件存储层：演示“先保存进度，再对外出手”的最小模型。"""

import json
import os


def load_tasks(path):
    """读取任务列表；文件不存在时返回空列表。"""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_tasks(path, tasks):
    """保存任务列表。写坏文件不会丢数据：先写临时文件再替换。"""
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)
