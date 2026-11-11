# 议题 01：list 命令在任务列表为空时崩溃

标签：`bug` `good-first-issue`

## 现象

刚安装后第一次运行 `python -m todo_cli list`（还没有任何任务）：

```text
Traceback (most recent call last):
  ...
IndexError: list index out of range
```

## 预期行为

- 空列表时输出友好提示（例如：`当前没有任务，先用 todo add 添加一条`）
- 退出码仍为 0

## 复现步骤

```bash
cd 仓库根目录
python -m todo_cli list
```

## 验收标准

1. 空列表时不再崩溃，输出友好提示
2. 补充测试：`test_list_empty_should_not_crash`
3. 现有测试全部保持通过
4. PR 描述包含：变更摘要、测试证据、影响范围、回滚说明、评审检查项
