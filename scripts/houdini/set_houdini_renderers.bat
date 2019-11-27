if not exist "%USERPROFILE%\Documents\houdini17.0" MkDir "%USERPROFILE%\Documents\houdini17.0"
copy "\\digitalfxserver\CompEnvironment\houdini_plugins\houdini.env" "%USERPROFILE%\Documents\houdini17.0\houdini.env"
clear
exit