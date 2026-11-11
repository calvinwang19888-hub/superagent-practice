# 议题 03：add 命令忽略 --priority 参数

标签：`bug` `ci-demo`

> 本议题配合第 8 课“CI 失败事件”演示使用。默认分支当前是绿色的；
> 需要制造 CI 失败事件时，教师运行 `scripts/trigger-ci-failure.sh`。

## 现象

```bash
python -m todo_cli add "紧急修复" --priority high
# 输出：已添加 #1 紧急修复（优先级 normal）
```

`--priority high` 被读取后又被无条件覆盖为 `normal`（见 `todo_cli/cli.py` 中
cmd_add 的 BUG-03 注释），用户设置被静默忽略。

## 预期行为

- `--priority low|normal|high` 生效
- 传入非法值时报错并返回退出码 1，而不是静默降级
- 补充测试：`test_add_priority_is_respected` 与 `test_add_priority_invalid_value_fails`

## 与第 8 课的关系

CI 失败演示脚本会向 main 推送一个让 `test_add_priority_is_respected` 失败的提交，
使默认分支 CI 变红，从而触发"默认分支 CI 失败"事件。演示结束后运行
`scripts/restore-after-demo.sh` 恢复绿色。
