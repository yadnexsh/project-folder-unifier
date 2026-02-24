from tqdm import tqdm
# x = [1, 2, 3, 5, 6]
# for each in tqdm(x, desc="Text"):
#     pass

import os
directory = r"H:\Gamut\Projects\project-photo-manager\test_input"
list_directory = os.listdir(r"H:\Gamut\Projects\project-photo-manager\test_input")
for folder in tqdm(list_directory, desc="Processing") :
    src_folder = os.path.join(directory, folder)
    if not os.path.isdir(src_folder):
        continue  