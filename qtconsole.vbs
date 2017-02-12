DIM objShell
set objShell=wscript.createObject("wscript.shell")
iReturn=objShell.Run("C:\ProgramData\Anaconda2\Scripts\ipython.exe qtconsole --colors=linux --colors=linux --ConsoleWidget.font_size=10", 0, TRUE)
