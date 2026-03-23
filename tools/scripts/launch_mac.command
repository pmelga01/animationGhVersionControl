#!/bin/bash
# Move up two levels from /tools/scripts/ to the repo root
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

export BLENDER_USER_CONFIG="$REPO_ROOT/tools/config"
export BLENDER_USER_SCRIPTS="$REPO_ROOT/tools/scripts"

echo "Launching Project Blender..."
open "/Applications/Blender.app"

# This command tells the Terminal to quit itself after launching
osascript -e 'tell application "Terminal" to quit' &
