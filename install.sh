#!/bin/bash
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST_NAME="com.fs2-menubar.plist"
PLIST_SRC="$DIR/$PLIST_NAME"
PLIST_DST="$HOME/Library/LaunchAgents/$PLIST_NAME"

# Create venv and install dependencies
if [ ! -d "$DIR/.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$DIR/.venv"
fi
echo "Installing dependencies..."
"$DIR/.venv/bin/pip" install -q -r "$DIR/requirements.txt"

# Generate plist with correct paths
sed \
    -e "s|VENV_PYTHON|$DIR/.venv/bin/python|" \
    -e "s|MAIN_PY|$DIR/main.py|" \
    -e "s|WORKING_DIR|$DIR|" \
    "$PLIST_SRC" > "$PLIST_DST"

# Load the service
launchctl load "$PLIST_DST"

echo "fs2-menubar installed and running."
echo "To uninstall: launchctl unload $PLIST_DST && rm $PLIST_DST"
