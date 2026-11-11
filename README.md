# todo_cli — Super Agent 实战课程练习仓库

一个只有三个命令的极简任务清单工具（`add` / `list` / `done`），
专门为《Super Agent 十小时实战课》准备。它**故意**埋了 3 个已知缺陷，
供学员和 Super Agent 完成"议题 → 工单 → 修复 → 测试 → PR"的完整链路。

## 快速开始

```bash
# 本地运行（零依赖，Python 3.9+）
python -m todo_cli add "第一项任务" --priority high
python -m todo_cli list
python -m todo_cli done 1

# 运行测试
python -m unittest discover -s tests -v
```

## 已知缺陷（教师按课程节奏发布）

| 议题 | 文件 | 用在哪节课 |
|---|---|---|
| list 空列表崩溃 | `issues/01-list-empty-crash.md` | 第 4 课（第一条研发链路） |
| done 编号不存在时崩溃 | `issues/02-done-missing-task.md` | 第 9 课（结课项目新议题） |
| add 忽略 --priority | `issues/03-priority-ignored.md` | 第 8 课（CI 失败事件演示） |

教师用 `scripts/publish-issues.sh` 一键发布议题（需要 `gh` 命令行并已登录）。

## 仓库约定（配合 Super Agent 使用）

详见 `docs/SAFE-USE.md`，要点：

- 本仓库只用于课堂：**不要**配置到个人或生产仓库
- Super Agent 的交付 PR 一律**人工评审，不自动合并**
- CI 在 push / PR 时运行全部测试（`.github/workflows/ci.yml`）
- 每个缺陷的修复都要求附验收测试，保持默认分支绿色

## 目录结构

```text
todo_cli/            极简任务清单工具（内含 2 个标注清楚的缺陷）
tests/               基线测试（默认分支保持绿色）
issues/              教师按课程节奏发布的议题
scripts/             议题发布与 CI 失败演示脚本
docs/                安全使用约定与课程对照说明
```
