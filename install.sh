#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
INSTALL_DIR="$HOME/.local/bin"
SERVICE_DIR="$HOME/.config/systemd/user"

mkdir -p "$INSTALL_DIR"
mkdir -p "$SERVICE_DIR"
mkdir -p ~/.fastnode

cp "$SCRIPT_DIR/fastnode.py" "$INSTALL_DIR/fastnode.py"
chmod 755 "$INSTALL_DIR/fastnode.py"

rm -f "$INSTALL_DIR/wfnode" "$INSTALL_DIR/fnode" "$INSTALL_DIR/dfnode"
ln -sf "$INSTALL_DIR/fastnode.py" "$INSTALL_DIR/wfnode"
ln -sf "$INSTALL_DIR/fastnode.py" "$INSTALL_DIR/fnode"
ln -sf "$INSTALL_DIR/fastnode.py" "$INSTALL_DIR/dfnode"

cp "$SCRIPT_DIR/fastnode.service" "$SERVICE_DIR/fastnode.service"

if ! grep -q 'export PATH="\$HOME/.local/bin:\$PATH"' "$HOME/.profile" 2>/dev/null; then
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.profile"
fi
export PATH="$HOME/.local/bin:$PATH"

systemctl --user daemon-reload
systemctl --user enable fastnode.service
systemctl --user start fastnode.service

echo "FNode установлен."
echo "Использование:"
echo "  wfnode <текст> \\#тег1 \\#тег2    — добавить заметку"
echo "  fnode \\#тег1 \\#тег2                   — найти заметки"
echo "  fnode                                       — все заметки"
echo "  dfnode <id>                                 — удалить заметку по ID"