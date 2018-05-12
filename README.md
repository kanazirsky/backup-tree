# backup-tree
Python script to backup directory tree structure

```
usage: backuptree.py [-h] [-p PREFIX] [-a {move,copy}] [--debug] [--dry-run]
                     SOURCE_PATH DEST_PATH

Backup directory tree

positional arguments:
  SOURCE_PATH           source path (should exist)
  DEST_PATH             destination path (should exist)

optional arguments:
  -h, --help            show this help message and exit
  -p PREFIX, --prefix PREFIX
                        backup file prefix (default: system date in YYYY-MM-DD
                        format)
  -a {move,copy}, --action {move,copy}
                        perform one of the actions (default: move)
  --debug               debug output
  --dry-run             dry run (don't actually move files)
 ```