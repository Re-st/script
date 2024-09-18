; AutoHotkey Script to Insert Current Date with Ctrl + Home
^Home::
FormatTime, CurrentDate,, yyyy-MM-dd  ; Format the date as YYYY-MM-DD
SendInput %CurrentDate%  ; Output the current date
return
