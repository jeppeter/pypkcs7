
echo off
set filename=%~f0
for %%F in ("%filename%") do set script_dir=%%~dpF

rmdir /Q /S %script_dir%dist 2>NUL
rmdir /Q /S %script_dir%pkcs7 2>NUL

del /Q /F %script_dir%pkcs7\__init__.py.touched 2>NUL
del /Q /F %script_dir%test\release\release.py.touched 2>NUL

del /Q /F %script_dir%pkcs7\__init__.py 2>NUL
del /Q /F %script_dir%test\release\release.py 2>NUL
del /Q /F %script_dir%rtools.pyc 2>NUL

del /Q /F %script_dir%setup.py 2>NUL
