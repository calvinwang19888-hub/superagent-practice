#!/usr/bin/env bash
# 一键发布课堂议题（需要 gh 命令行并已登录目标仓库）
# 用法：./publish-issues.sh <owner/repo> [01|02|03|all]
set -euo pipefail

REPO="${1:?用法: $0 <owner/repo> [01|02|03|all]}"
WHICH="${2:-all}"

DIR="$(cd "$(dirname "$0")/.." && pwd)/issues"

publish() {
  case "$1" in
    01) gh issue create -R "$REPO" -t "list 命令在任务列表为空时崩溃" \
         -b "$(cat "$DIR/01-list-empty-crash.md")" -l "bug" -l "good-first-issue" ;;
    02) gh issue create -R "$REPO" -t "done 命令对不存在的任务编号直接崩溃" \
         -b "$(cat "$DIR/02-done-missing-task.md")" -l "bug" ;;
    03) gh issue create -R "$REPO" -t "add 命令忽略 --priority 参数" \
         -b "$(cat "$DIR/03-priority-ignored.md")" -l "bug" -l "ci-demo" ;;
  esac
  echo "已发布议题 $1"
}

case "$WHICH" in
  01|02|03) publish "$WHICH" ;;
  all) publish 01; publish 03; echo "议题 02 留到第 9 课再发布（结课项目新议题）" ;;
  *) echo "未知参数：$WHICH"; exit 1 ;;
esac
