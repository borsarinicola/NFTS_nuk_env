if not exist "%USERPROFILE%\Documents\houdini17.0" MkDir "%USERPROFILE%\Documents\houdini17.0"
copy "\\digitalfxserver\shared\NFTS_nuk_env\scripts\houdini\houdini.env" "%USERPROFILE%\Documents\houdini17.0\houdini.env"
clear
exit