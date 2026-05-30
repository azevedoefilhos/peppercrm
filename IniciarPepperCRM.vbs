' IniciarPepperCRM.vbs
' Inicia o PepperCRM sem janela de cmd e sem aviso de segurança do Windows.
' Coloque este arquivo na area de trabalho ou onde preferir.

Dim shell
Set shell = CreateObject("WScript.Shell")

' Caminho do bat — ajuste se mover a pasta do projeto
Dim batPath
batPath = "C:\Users\welov\PycharmProjects\WebSolution\peppercrm\iniciar_peppercrm.bat"

' 0 = janela oculta, False = nao aguarda terminar
shell.Run "cmd /c """ & batPath & """", 0, False

' Aguarda 4 segundos e abre o navegador
WScript.Sleep 4000
shell.Run "http://localhost:8501", 1, False

Set shell = Nothing
