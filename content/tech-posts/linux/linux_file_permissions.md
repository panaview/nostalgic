+++
date = '2025-05-11T23:03:20+02:00'
title = 'Refresher: Linux File Permissions'
+++

- Command `id` can be used to display current user group and identity:
e.g. Display current user group identity: `id -gn`

- rwx chmod 777 chmod ugo+rwx common file permissions

- Special permission: chmod X###
- setuid (always executes as user who owns the file, no matter who is passing the command)
- setgid (execute file as group owner of the file, file created has group ownevership set to
- directory owner, useful for collaboration)
- sticky bit (directory-level special permission that restricts file deletion, only file owner can
delete file within directory)
- directory bit