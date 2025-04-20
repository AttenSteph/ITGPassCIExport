del export_pass_ci.7z
rmdir "export_pass_ci" /S /Q
python -m nuitka --onefile --windows-console-mode=force .\export_pass_ci.py
mkdir export_pass_ci
copy README.MD export_pass_ci
move export_pass_ci.exe export_pass_ci\
.\build-tools\7zr.exe a .\export_pass_ci.7z .\export_pass_ci\ -mx=9 -aoa -bd