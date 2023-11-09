@ECHO OFF
REM This batch file opens the blender in background mode and runs a Python script
REM The blender.exe is already in the environment variables
py %~dp0\compressor.py
