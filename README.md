
![Project Header](https://capsule-render.vercel.app/api?type=blur&height=300&color=gradient&text=Folder%20Unifier%20CLI)

<p align="center">
A simple and powerful **command-line tool** that automatically organizes folders based on their naming pattern.  
<p/>

--- 

It scans a directory for folders following the format:

```
Main - Sub
Main- Sub
Main - Cam
```

And restructures them into:
```
Main 
 └── Sub1
 └── Sub2
 └── Cam
```
All files inside the original folders are moved into their new structured locations.


## Features

* Automatically restructures folders from ```Main - Sub``` into ```Main/Sub```.
* Moves all files safely into new folders.
* Auto-numbers subfolders to prevent overwriting.
* Dry-run mode to preview changes without modifying anything.
* List directory contents quickly (```--ls```).
* Logs all actions for easy tracking.
* Simple CLI with progress feedback.
* Works cross-platform with robust error handling.

## Requirements

Install dependencies using:

```
pip install -r requirements.txt
```


## Usage

Run the script using:

```
# Organize a directory
python main.py ./photos --organize

# Preview changes without moving files
python main.py ./photos --organize --dry-run

# List all files/folders in a directory
python main.py ./photos --ls

# Show help
python main.py --help
```

## Example

This example demonstrates how the organizer restructures folders.

| Before                  | After                     |
|-------------------------|---------------------------|
| Vacation - Beach        | Vacation/Beach1           |
| Vacation - Mountains    | Vacation/Mountains1       |
| Work - Events           | Work/Events1              |


<table> <tr> <th>Before</th> <th>After</th> </tr> <tr> <td> <pre>
Vacation - Beach
Vacation - Mountains
Work - Events
</pre> </td> <td> <pre>
Vacation
└── Beach1
└── Mountains1
Work
└── Events1
</pre> </td> </tr> </table>
         |

##  Dry Run Mode 

Before making permanent changes, preview what the script *would* do:
```
python main.py ./photos --organize --dry-run
```
This will:
- Show which folders would be created  
- Show which files would be moved  
- Show which folders would be deleted  
 **No real changes are applied**


## License

This project is open-source and free to use for learning and personal projects.
