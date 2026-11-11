"""命令行入口：add / list / done 三个子命令。

main(argv) 返回退出码（0 成功，1 失败），方便测试与 CI。
"""

import sys

from .storage import load_tasks, save_tasks

DEFAULT_STORE = ".todo.json"
PRIORITIES = ("low", "normal", "high")


def _find_flag(argv, flag):
    """从参数里取 --flag value；找不到返回 None。"""
    if flag in argv:
        i = argv.index(flag)
        if i + 1 < len(argv):
            return argv[i + 1]
    return None


def _title_words(argv):
    """去掉 --priority 及其取值后，剩下的词就是任务标题。"""
    words = []
    skip_next = False
    for item in argv:
        if skip_next:
            skip_next = False
            continue
        if item == "--priority":
            skip_next = True
            continue
        words.append(item)
    return words


def cmd_add(store, argv):
    title = " ".join(_title_words(argv))
    if not title:
        print("用法：todo add <任务描述> [--priority low|normal|high]")
        return 1

    # BUG-03（issues/03-priority-ignored.md）：
    # --priority 参数被读取后又被无条件覆盖为默认值，用户设置被静默忽略。
    # 预期修复：尊重用户取值；非法取值报错并返回退出码 1。
    requested = _find_flag(argv, "--priority")
    priority = "normal"

    tasks = load_tasks(store)
    task = {
        "id": max((t["id"] for t in tasks), default=0) + 1,
        "title": title,
        "priority": priority,
        "done": False,
    }
    tasks.append(task)
    save_tasks(store, tasks)
    print("已添加 #%d %s（优先级 %s）" % (task["id"], task["title"], task["priority"]))
    return 0


def cmd_list(store, argv):
    tasks = load_tasks(store)
    if not tasks:
        # BUG-01（issues/01-list-empty-crash.md）：
        # 空列表时误取 tasks[0]，直接崩溃；应输出友好提示。
        print(tasks[0]["title"])
        return 0
    for t in tasks:
        mark = "x" if t["done"] else " "
        print("#%-3d [%s] %-6s %s" % (t["id"], mark, t["priority"], t["title"]))
    return 0


def cmd_done(store, argv):
    if not argv:
        print("用法：todo done <任务编号>")
        return 1
    try:
        task_id = int(argv[0])
    except ValueError:
        print("任务编号必须是整数：%r" % argv[0])
        return 1

    tasks = load_tasks(store)
    # BUG-02（issues/02-done-missing-task.md）：
    # 编号不存在时 IndexError 崩溃；应提示“任务不存在”并返回退出码 1。
    task = next(t for t in tasks if t["id"] == task_id)
    task["done"] = True
    save_tasks(store, tasks)
    print("已完成 #%d %s" % (task["id"], task["title"]))
    return 0


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    argv = list(argv)
    store = DEFAULT_STORE
    if not argv:
        print("用法：todo add|list|done ...")
        return 1
    cmd, rest = argv[0], argv[1:]
    if cmd == "add":
        return cmd_add(store, rest)
    if cmd == "list":
        return cmd_list(store, rest)
    if cmd == "done":
        return cmd_done(store, rest)
    print("未知命令：%s（可用：add / list / done）" % cmd)
    return 1
