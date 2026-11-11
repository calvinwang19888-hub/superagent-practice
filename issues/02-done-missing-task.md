# 议题 02：done 命令对不存在的任务编号直接崩溃

标签：`bug`

> 本议题是第 9 课结课项目的“新缺陷议题”，请勿在第 4 课提前使用。

## 现象

```bash
python -m todo_cli done 99
```

```text
Traceback (most recent call last):
  ...
StopIteration
```

（任务编号不存在时 `next()` 抛出 StopIteration，用户看到的是堆栈而不是错误说明。）

## 预期行为

- 编号不存在时输出：`任务 #99 不存在，先用 todo list 查看编号`
- 退出码为 1（命令失败）

## 验收标准

1. 不存在的编号：友好提示 + 退出码 1
2. 编号非整数：已有处理保持不变
3. 补充测试：`test_done_missing_task_should_fail_gracefully`
4. 现有测试全部保持通过
5. PR 描述包含五类交付信息（见仓库 README）
