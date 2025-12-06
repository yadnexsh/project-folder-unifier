# Folder Organizer – Terminal Utility (Python)

A simple and powerful **command-line tool** that automatically organizes folders based on their naming pattern.  
It scans a directory for folders following the format:

```
Main - Sub
```

And restructures them into:
```
Main/
 └── Sub1/
 └── Sub2/
```
All files inside the original folders are moved into their new structured locations.



## Requirements

Install dependencies using:

```
pip install -r requirements.txt
```


## Usage

Run the script using:

```
python main.py <directory_path> [flags]
```

### Example

python main.py ./photos --organize



## Available Flags

| Flag         | Description                                                  |
|--------------|--------------------------------------------------------------|
| `--help`     | Show help information                                        |
| `--ls`       | List all files and folders in the given directory            |
| `--organize` | Organize folders based on `Main - Sub` format                |
| `--dry-run`  | Preview changes without actually moving any files           |



##  Dry Run Mode 

Before making permanent changes, preview what the script *would* do:

python main.py ./photos --organize --dry-run

This will:
- Show which folders would be created  
- Show which files would be moved  
- Show which folders would be deleted  
 **No real changes are applied**


## License

This project is open-source and free to use for learning and personal projects.
