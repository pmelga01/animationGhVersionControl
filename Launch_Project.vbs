Set FSO = CreateObject("Scripting.FileSystemObject")
Set WshShell = CreateObject("WScript.Shell")

' 1. Get the absolute path of the folder where THIS .vbs script is located
strScriptFolder = FSO.GetParentFolderName(WScript.ScriptFullName)

' 2. Combine that folder path with the path to your batch file using backslashes
' This ensures it works even if the project is on a different drive
strBatchPath = strScriptFolder & "\tools\scripts\launch_win.bat"

' 3. Run the batch file invisibly (the "0" at the end hides the window)
' We use triple quotes to handle any spaces in your folder names
WshShell.Run chr(34) & strBatchPath & chr(34), 0

Set WshShell = Nothing
Set FSO = Nothing