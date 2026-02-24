from tqdm import tqdm
import shutil
import sys
import os
import re
from datetime import datetime
from colorama import Fore, init, Style

init(autoreset=True)

today = datetime.now().strftime("%Y-%m-%d")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-7]


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
        unique = os.path.join(main_folder, unique_name)
        if not os.path.exists(unique):
            return unique
        counter += 1


def logs(log_file, log):
    with open(log_file, "a") as file:
        file.write(log)


def verbose(verbose_log_file, verbose_log):
    with open(verbose_log_file, "a") as file:
        file.write(verbose_log)


def organize_files(directory, log_file, verbose_log_file, dry_run=False):

    list_directory = os.listdir(directory)
    created_count = 0
    moved_count = 0
    removed_count = 0

    for folder in tqdm(list_directory, desc="Processing"):

        src_folder = os.path.join(directory, folder)

        if not os.path.isdir(src_folder):
            continue

        if " - " not in folder:
            print(f"{folder} | Not Required")
            continue

        split = re.split(r"\s*-\s*", folder)

        if len(split) == 2:
            
            main = split[0].strip()
            sub = split[1].strip()

            main_folder = os.path.join(directory, main)
            sub_folder = unique_subfolder(main_folder, sub)
            relative_sub = os.path.relpath(sub_folder, directory)

            if dry_run:
                print(f"[DRY RUN] Would create: {sub_folder}")
            else:
                os.makedirs(sub_folder, exist_ok=True)
                created_count += 1

                log_entry = f"{today} | Organized {folder} - {relative_sub}\n"
                logs(log_file, log_entry)

                verbose_entry = (f"\n{today} | CREATED | {sub_folder}\n")
                verbose(verbose_log_file, verbose_entry)


            for item in os.listdir(src_folder):
                source = os.path.join(src_folder, item)
                destination = os.path.join(sub_folder, item)

                if dry_run:
                    print(f"[DRY RUN] Would move: {source} -> {destination}")
                else:
                    shutil.move(source, destination)
                    moved_count += 1

                    verbose_entry = (f"{timestamp} | MOVED | {source} -> {destination}\n")
                    verbose(verbose_log_file, verbose_entry)

            if dry_run:
                print(f"[DRY RUN] Would remove: {src_folder}")
            else:
                os.rmdir(src_folder)
                removed_count += 1

                verbose_entry = (f"{timestamp} | REMOVED | {src_folder}\n")
                verbose(verbose_log_file, verbose_entry)

            print(f"{folder} -> {relative_sub}")

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
        help()
        sys.exit(1)

    directory = os.path.abspath(sys.argv[1])
    flags = sys.argv[2:]

    log_file = os.path.join(directory, "log.txt")
    verbose_log_file = os.path.join(directory, "verbose_log.txt")

    valid_flags = ["--help", "--ls", "--dry-run", "--organize"]

    if not flags:
        print(Fore.RED + "No action provided. Use --organize or --ls.")
        help()
        sys.exit(1)

    for each in flags:
        if each not in valid_flags:
            print(Fore.RED + f"Invalid flag: {each}")
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
        organize_files(directory, log_file, verbose_log_file, dry_run=dry_run)
        sys.exit(0)


if __name__ == "__main__":
    main()
