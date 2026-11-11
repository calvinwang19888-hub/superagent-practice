"""基线测试：只覆盖当前正确的行为，保持默认分支绿色。

两个已知缺陷的验收测试写在对应 issues/ 文件里，由修复者在 PR 中补充。
"""

import os
import sys
import tempfile
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from todo_cli import cli  # noqa: E402


class TodoCliTest(unittest.TestCase):
    def setUp(self):
        fd, self.store = tempfile.mkstemp(suffix=".json")
        os.close(fd)
        os.remove(self.store)
        patcher = mock.patch.object(cli, "DEFAULT_STORE", self.store)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_add_then_list(self):
        self.assertEqual(cli.main(["add", "写周报"]), 0)
        self.assertEqual(cli.main(["add", "订会议室"]), 0)
        with mock.patch("sys.stdout") as fake:
            self.assertEqual(cli.main(["list"]), 0)
        printed = "".join(c[0][0] for c in fake.write.call_args_list)
        self.assertIn("写周报", printed)
        self.assertIn("订会议室", printed)
        # 标题里不应混入参数文本（--priority 由议题 03 跟踪）
        self.assertNotIn("--priority", printed)

    def test_done_existing_task(self):
        cli.main(["add", "发布版本"])
        tasks = __import__("todo_cli.storage", fromlist=["load_tasks"]).load_tasks(self.store)
        self.assertEqual(cli.main(["done", str(tasks[0]["id"])]), 0)
        tasks = __import__("todo_cli.storage", fromlist=["load_tasks"]).load_tasks(self.store)
        self.assertTrue(tasks[0]["done"])

    def test_unknown_command_fails(self):
        self.assertEqual(cli.main(["bogus"]), 1)

    def test_add_requires_title(self):
        self.assertEqual(cli.main(["add"]), 1)


if __name__ == "__main__":
    unittest.main()
