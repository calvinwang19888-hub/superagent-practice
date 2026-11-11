#!/usr/bin/env bash
# 第 8 课演示收尾：撤销 CI 失败演示提交，恢复默认分支绿色。
# 用法：./restore-after-demo.sh
set -euo pipefail
cd "$(dirname "$0")/.."

git checkout main
git pull origin main
git revert --no-edit HEAD
git push origin main
echo "演示提交已撤销，CI 将恢复绿色。"
