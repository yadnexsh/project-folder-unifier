import string
import random
import os

folder_count = 5
name_length = 2
letters = string.ascii_letters + string.digits

def random_folder():
    left = ""
    right = ""
        
    for each in range(name_length):
        left += random.choice(letters)
        right += random.choice(letters)
        
    return left + "-" + right


def main():
    src = os.path.abspath(__file__)
    src_dir = os.path.dirname(src)
    test_folder = os.path.join(src_dir, "test_folder")
    os.makedirs(test_folder, exist_ok=True)

    for each in range(folder_count):
        folder_name = random_folder()
        folder_path = os.path.join(test_folder, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
if __name__ == "__main__":
    main()
