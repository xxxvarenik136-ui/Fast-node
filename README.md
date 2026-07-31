# Fast-node
You can make fast nodes in terminal with tags and then read it and delete it. You will not forget anything

FastNode (FNode) — консольное приложение для заметок с тегами


Важно: Все теги пишуться через backslash 

Пример: \#tag1 \#tag2


Команды:
  wfnode <текст> \#тег1 \#тег2  — добавить заметку
  
  fnode \#тег1 \#тег2 — найти по тегам  (AND-логика)
  fnode — все заметки
  dfnode <id> — удалить заметку по ID (виден в fnode как [id])

Вывод fnode: [id] текст 

Хранение: ~/.fastnode/data.json

Автозапуск при старте: systemd user service (Type=oneshot)
  — создаёт symlink'и wfnode, fnode, dfnode в ~/.local/bin/
  
Установка: bash install.sh
