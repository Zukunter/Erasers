# Erasers

___

## All | e

The command `e` erase the visible part of the screen

## Purge | E

The command `E` erase the whole scrollback buffer of the shell

---

### Installers
The next command will compile and move onto the path the generated binaries

- Python | With privileges
```bash
python install.py
```

- Bash
```bash
comp=""; for c in clang gcc cl cc; do type -p "$c" >/dev/null && comp=$(type -p "$c") && break; done; if [ -z "$comp" ] && [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then for p in "/c/Program Files/Microsoft Visual Studio"/*/*"/VC/Tools/MSVC"/*"/bin/Hostx64/x64/cl.exe"; do [ -f "$p" ] && comp="$p" && break; done; fi; if [ -z "$comp" ]; then echo "No compiler found"; else c_name=$(basename "$comp" | tr '[:upper:]' '[:lower:]' | sed 's/\.exe//'); declare -A files=(["EraseAll.c"]="e" ["ErasePurge.c"]="E"); if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then t_dir="/c/Windows/System32"; ext=".exe"; else t_dir="/bin"; ext=""; fi; for f in "${!files[@]}"; do b="${files[$f]}$ext"; echo "Compiling $f..."; if [ "$c_name" = "cl" ]; then "$comp" /O2 /nologo "$f" /Fe:"$b" && rm -f "${f%.c}.obj"; else "$comp" -O3 "$f" -o "$b"; fi; [ -f "$b" ] && (mv "$b" "$t_dir/$b" 2>/dev/null && { [[ "$ext" == "" ]] && chmod +x "$t_dir/$b"; echo "Moved $b to $t_dir"; } || echo "Permission denied for $t_dir"); done; fi
```

- Zsh
```zsh
comp=""; for c in clang gcc cl cc; do command -v "$c" >/dev/null && comp=$(command -v "$c") && break; done; if [ -z "$comp" ] && [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then for p in "/c/Program Files/Microsoft Visual Studio"/*/*"/VC/Tools/MSVC"/*"/bin/Hostx64/x64/cl.exe"; do [ -f "$p" ] && comp="$p" && break; done; fi; if [ -z "$comp" ]; then echo "No compiler found"; else c_name=$(basename "$comp" | tr '[:upper:]' '[:lower:]' | sed 's/\.exe//'); typeset -A files=( "EraseAll.c" "e" "ErasePurge.c" "E" ); if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then t_dir="/c/Windows/System32"; ext=".exe"; s_cmd=""; else t_dir="/bin"; ext=""; s_cmd="sudo"; fi; for f in ${(k)files}; do b="${files[$f]}$ext"; echo "Compiling $f..."; if [ "$c_name" = "cl" ]; then "$comp" /O2 /nologo "$f" /Fe:"$b" && rm -f "${f%.c}.obj"; else "$comp" -O3 "$f" -o "$b"; fi; [ -f "$b" ] && ($s_cmd mv "$b" "$t_dir/$b" 2>/dev/null && { [[ "$ext" == "" ]] && $s_cmd chmod +x "$t_dir/$b"; echo "Moved $b to $t_dir"; } || echo "Permission denied for $t_dir. Run the terminal as Admin or check sudo privileges."); done; fi
```

- CMD
```cmd
@echo off & set "comp=" & for %c in (clang.exe gcc.exe cl.exe cc.exe) do (where %c >nul 2>nul && for /f "delims=" %i in ('where %c') do set "comp=%i") & if not defined comp (for /r "C:\Program Files\Microsoft Visual Studio" %p in (cl.exe) do if exist "%p" set "comp=%p") & if not defined comp (echo No compiler found) else (for %a in ("EraseAll.c:e" "ErasePurge.c:E") do (for /f "tokens=1,2 delims=:" %f in (%a) do (echo Compiling %f... & if "x%~nxb"=="xcl.exe" ("%comp%" /O2 /nologo "%f" /Fe:"%g.exe" & del /q "%~nf.obj" >nul 2>nul) else ("%comp%" -O3 "%f" -o "%g.exe") & if exist "%g.exe" (move /y "%g.exe" "C:\Windows\System32\%g.exe" >nul 2>nul && echo Moved %g.exe to System32 || echo Permission denied. Please run CMD as Administrator.))))
```
