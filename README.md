# backuptree.py
Python script to backup directory tree structure.

```
usage: backuptree.py [-h] [-p PREFIX] [-a {move,copy}] [--debug] [--dry-run]
                     SOURCE_PATH DEST_PATH

Backup directory tree. Make the same directory structure in destination
directory and add prefix (with current date by default) to each file name.

positional arguments:
  SOURCE_PATH           source path (should exist)
  DEST_PATH             destination path (should exist)

optional arguments:
  -h, --help            show this help message and exit
  -p PREFIX, --prefix PREFIX
                        backup file prefix (default: system date in YYYY-MM-DD_ format)
  -a {move,copy}, --action {move,copy}
                        perform one of the actions with each file (default: move)
  --debug               debug output
  --dry-run             don't preform real actions, use with --debug to test your settings
 ```

# Example
```
$> tree test-data
test-data
├── a
│   ├── sub_a
│   │   ├── sub_sub_a
│   │   │   └── file_1.data
│   │   └── sub_sub_b
│   │       └── file_2.data
│   └── sub_b
│       ├── file_3.data
│       └── sub_sub_a
└── backup

7 directories, 3 files

$> ./backuptree.py test-data/a test-data/backup
2018-05-12 21:11:39,217: 3 files, 5 directories processed

$> tree test-data
test-data
├── a
│   ├── sub_a
│   │   ├── sub_sub_a
│   │   └── sub_sub_b
│   └── sub_b
│       └── sub_sub_a
└── backup
    ├── sub_a
    │   ├── sub_sub_a
    │   │   └── 2018-05-12_file_1.data
    │   └── sub_sub_b
    │       └── 2018-05-12_file_2.data
    └── sub_b
        ├── 2018-05-12_file_3.data
        └── sub_sub_a

12 directories, 3 files
```