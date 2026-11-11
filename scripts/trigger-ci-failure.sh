#!/usr/bin/env bash
# 第 8 课演示：制造一次“默认分支 CI 失败”事件，触发观察模式的修复候选。
# 演示结束后务必运行 restore-after-demo.sh 恢复绿色。
# 用法：./trigger-ci-failure.sh
set -euo pipefail
cd "$(dirname "$0")/.."

cat > tests/test_demo_ci_failure.py <<'EOF'
"""临时演示测试：验证 --priority 高优先级是否被尊重（当前实现有缺陷，必然失败）。"""
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from todo_cli import cli


class DemoPriorityTest(unittest.TestCase):
    def test_add_priority_is_respected(self):
        with mock.patch.object(cli, "DEFAULT_STORE", os.devnull):
            with mock.patch("todo_cli.cli.save_tasks") as save:
                cli.main(["add", "紧急修复", "--priority", "high"])
                self.assertEqual(save.call_args[0][1][0]["priority"], "high")


if __name__ == "__main__":
    unittest.main()
EOF

git checkout -b ci-failure-demo
git add tests/test_demo_ci_failure.py
git commit -m "demo: 临时添加优先级回归测试（触发 CI 失败演示）"
git push origin ci-failure-demo:main
echo ""
echo "已推送演示提交，CI 将变红并触发‘默认分支 CI 失败’事件。"
echo "演示观察结束后，运行 scripts/restore-after-demo.sh 恢复绿色。"
