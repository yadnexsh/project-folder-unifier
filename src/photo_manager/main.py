

from tqdm import tqdm
import shutil
import sys 
import os
import re
from datetime import datetime
from colorama import Fore,init,Style

init(autoreset=True)


today = datetime.now().strftime("%Y-%m-%d")


def help():
    help_text = """
PHOTO / FOLDER ORGANIZER – HELP
----------------------------------

USAGE:
    python main.py <directory_path> [flags]

EXAMPLES:
    python main.py ./photos --organize
    python main.py ./photos --organize --dry-run
    python main.py ./photos --ls
    python main.py ./photos --help

AVAILABLE FLAGS:
    --help        Show this help menu
    --ls          List all files and folders inside the given directory
    --organize    Organize folders based on 'Main - Sub' naming pattern
    --dry-run     Preview what would happen without making any changes

HOW ORGANIZING WORKS:
    Input Folder Names:
        Vacation - Beach
        Vacation - Mountains
        Work - Events

    Output Structure:
        Vacation/
            Beach1/
            Mountains1/
        Work/
            Events1/

    - Files are moved into newly created structured folders.
    - Original folders are deleted after moving.
    - Auto-numbering prevents overwriting existing folders.

LOGGING:
    - A log.txt file is created inside the target directory.
    - All created and removed folders are recorded with date.
----------------------------------
""" 
    print(help_text)
    

def list_files(directory):
    
    if not os.path.exists(directory):
        print(Fore.RED + f"'{directory}' not found.")
        sys.exit(0)

    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        print(path)
        

def unique_subfolder(main_folder, sub):

    counter = 1
    while True:
        unique_name = f"{sub}{counter}"
        unique = os.path.join(main_folder, unique_name)         # adds number to subfolder
        if not os.path.exists(unique):
            return unique
        counter += 1
    
def organize_files(directory, log_file, detailed_log_file, dry_run=False):
    
    list_directory = os.listdir(directory)
    created_count = 0
    moved_count = 0
    removed_count = 0
    
    for folder in tqdm(list_directory, desc="Processing") :
        src_folder = os.path.join(directory, folder)
        
        if not os.path.isdir(src_folder):
            continue                            # want to run a code if it stops on file
        
        split = re.split(r"\s*-\s*", folder)

        if len(split) == 2:
            main = split[0].strip()
            sub = split[1].strip()                                      # to remve space
            
            main_folder = os.path.join(directory, main)
            sub_folder = unique_subfolder(main_folder, sub)

            
            if dry_run:
                print(f"Code would make {main_folder} and {sub_folder}")
            else:
                os.makedirs(sub_folder, exist_ok=True)
                
                created_count += 1
                
                log = f"{today} | Created {main} > {sub}\n"
                with open(log_file, "a") as file:
                    file.write(log)
                    
                detailed_log = f"{today} | Created | {main_folder} > {sub_folder}\n"
                with open(detailed_log_file, "a") as file:
                    file.write(detailed_log)
            
            list_src_folder = os.listdir(src_folder)
            for item in list_src_folder :         # fetching item inside the folder to move
                
                source = os.path.join(src_folder , item)
                destination = os.path.join(sub_folder, item)
                
                if dry_run:
                    print(f"Code would move '{source}' > '{destination}'")
                else:
                    shutil.move(source, destination)
                    moved_count += 1
                    detailed_log = f"{today} | Moved | {source} > {destination}\n"
                    with open(detailed_log_file, "a") as file:
                        file.write(detailed_log)

            if dry_run:
                print(f"Code Would remove folder > {src_folder}")
            else:
                os.rmdir(src_folder)
                
                removed_count += 1
                
                log = f"{today} | Removed > {folder}\n"
                with open(log_file, "a") as file:
                    file.write(log)
                    
                detailed_log = f"{today} | Removed > {src_folder}\n"
                with open(detailed_log_file, "a") as file:
                    file.write(detailed_log)
                    
            print(f"{folder} > {sub_folder}")
            
            
        else:
            print(f"{folder} | Not Required")
            
    print("\nSUMMARY REPORT")
    print("----------------------")
    print(f"Folders Created : {created_count}")
    print(f"Files Moved     : {moved_count}")
    print(f"Folders Removed : {removed_count}")

def main():
    
    if len(sys.argv) < 2:                                       
        print(Fore.RED + "\nNo directory provided.")
        print("----------------------------------")
        help()
        sys.exit(1)
        
    directory = os.path.abspath(sys.argv[1])
    flags = sys.argv[2:]
    log_file = os.path.join(directory , "log.txt")
    detailed_log_file = os.path.join(directory , "detailed_log.txt")
    valid_flags = ["--help", "--ls", "--dry-run", "--organize"]


    
    if not flags:
        print(Fore.RED + "No action provided. Use --organize or -l.")
        help()
        sys.exit()
    

        
    for each in flags:
        if each not in valid_flags:
            print("Invalid flag" , each)
            print(f"Allowed flags are {valid_flags}")
            sys.exit(1)
    
    if not os.path.exists(directory):
        print(Fore.RED + f"'{directory}' not found.")
        sys.exit(1)

    if "--help" in flags:
        help()
        sys.exit(0)
        
    if "--ls" in flags:
        list_files(directory)
        sys.exit(0)
    
    if "--organize" in flags:
        dry_run = "--dry-run" in flags
        organize_files(directory, log_file, detailed_log_file, dry_run=dry_run)
        sys.exit(0)





    
if __name__ == "__main__":
    main()