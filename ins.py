import os
import stat
import shutil
import subprocess

def which_c_compiler_is_avaible():
    possible_c_compilers = ["clang", "gcc"]

    for possible_c_compiler in possible_c_compilers:
        where_it_is = shutil.which(possible_c_compiler)

        if where_it_is != None:
            return where_it_is

    return None

c_compiler = which_c_compiler_is_avaible();

files_and_name = {
        "EraseAll.c" : "e", 
        "ErasePurge.c" : "E"
}



for file, bin_name in files_and_name.items():
    output = subprocess.run([c_compiler, "-O3", file, "-o", bin_name])
    if not os.path.exists(bin_name): print("Could not found the os' path.")

    path_env = os.environ.get("PATH", "")
    path_dirs = path_env.split(os.pathsep)

    target_dir = None
    for dir in path_dirs:
        if os.path.isdir(dir) and os.access(dir, os.W_OK): 
            if os.name == 'nt' and 'system32' in dir.lower():
                continue
            target_dir = dir
            break

    if not target_dir: print("Could not find where to move binarys.")

    destination_path = os.path.join(target_dir, bin_name)

    try:
        # Move the file using pure Python logic
        shutil.move(bin_name, destination_path)

        if os.name != 'nt':
            current_permissions = os.stat(destination_path).st_mode
            # Add executable permissions to owner, group, and others
            os.chmod(destination_path, current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    except Exception as e:
        print(f"{e}")





