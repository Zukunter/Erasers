import os
import stat
import shutil
import subprocess
import sys
import glob

def get_available_c_compiler():
    possible_c_compilers = ["clang", "gcc", "cl", "cc"]
    for compiler in possible_c_compilers:
        if shutil.which(compiler) is not None:
            return compiler

    if os.name == 'nt':
        program_files = os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)")
        # Search patterns for common modern Visual Studio installation paths
        vs_patterns = [
            os.path.join(program_files, "Microsoft Visual Studio", "*", "*", "VC", "Tools", "MSVC", "*", "bin", "Hostx64", "x64", "cl.exe"),
            os.path.join("C:\\Program Files", "Microsoft Visual Studio", "*", "*", "VC", "Tools", "MSVC", "*", "bin", "Hostx64", "x64", "cl.exe")
        ]
        
        for pattern in vs_patterns:
            matches = glob.glob(pattern)
            if matches:
                # Return the absolute path to the latest found cl.exe
                return matches[-1]

    return None

c_compiler = get_available_c_compiler()

if c_compiler is None:
    print("Error: No suitable C compiler (clang, gcc, Visual Studio/cl, cc) found on this system.")
    sys.exit(1)

# Clean up display name if it's a full path string
compiler_name = os.path.basename(c_compiler).lower().replace(".exe", "")
print(f"Using compiler: {c_compiler}")

files_and_name = {
    "EraseAll.c" : "e", 
    "ErasePurge.c" : "E"
}

# Determine the cross-platform system binary directory
if os.name == 'nt':
    system_root = os.environ.get('SystemRoot', 'C:\\Windows')
    target_dir = os.path.join(system_root, 'System32')
else:
    target_dir = "/bin"

for file, bin_name in files_and_name.items():
    if os.name == 'nt' and not bin_name.endswith('.exe'):
        output_name = f"{bin_name}.exe"
    else:
        output_name = bin_name

    # Handle Visual Studio / MSVC specific syntax arguments
    if compiler_name == "cl":
        # /O2: Optimization level, /Fe: Output file name, /nologo: Hides MSVC banner
        compile_args = [c_compiler, "/O2", "/nologo", file, f"/Fe:{output_name}"]
    else:
        # Clang, GCC, and CC standard Unix flags
        compile_args = [c_compiler, "-O3", file, "-o", output_name]

    print(f"Compiling {file}...")
    output = subprocess.run(compile_args)
    
    # Visual Studio generates intermediate '.obj' files during compilation; we clean them up
    if compiler_name == "cl":
        obj_file = file.replace(".c", ".obj")
        if os.path.exists(obj_file):
            os.remove(obj_file)

    if not os.path.exists(output_name): 
        print(f"Compilation failed for {file}.")
        continue

    destination_path = os.path.join(target_dir, output_name)

    try:
        shutil.move(output_name, destination_path)
        print(f"Successfully moved {output_name} to {destination_path}")

        if os.name != 'nt':
            current_permissions = os.stat(destination_path).st_mode
            os.chmod(destination_path, current_permissions | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    except PermissionError:
        print(f"Permission denied: Could not write to {target_dir}")
        if os.name == 'nt':
            print("Please run this script from an Administrator Command Prompt/PowerShell.")
        else:
            print("Please run this script using 'sudo python3 install.py'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
