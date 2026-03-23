#!/bin/bash
# 1. Resolve Paths
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PROJECT_ROOT="$(dirname "$repo_root")"

echo "--- MAC PROJECT SETUP STARTING ---"

# 2. Create local folders
mkdir -p "$PROJECT_ROOT/local/temp"
mkdir -p "$PROJECT_ROOT/local/cache"
echo "[OK] Created local/ directories."

# 3. Create Symbolic Link
# Path: /Volumes/GoogleDrive/Shared drives/...
SOURCE_DRIVE="/Volumes/GoogleDrive/Shared drives/AnimationDrive/shared"
TARGET_LINK="$PROJECT_ROOT/shared"

if [ -L "$TARGET_LINK" ]; then
    echo "[INFO] 'shared' link already exists."
else
    ln -s "$SOURCE_DRIVE" "$TARGET_LINK"
    echo "[OK] Created link to Google Drive."
fi

echo "--- SETUP COMPLETE! ---"
