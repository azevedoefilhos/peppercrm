' IniciarPepperCRM.vbs
' Inicia o PepperCRM sem janela de cmd e sem aviso de segurança do Windows.
' Coloque este arquivo na area de trabalho ou onde preferir.

Dim shell
Set shell = CreateObject("WScript.Shell")

' Caminho do projeto — ajuste se mover a pasta
Dim projPath
projPath = "C:\Users\welov\PycharmProjects\WebSolution\peppercrm"

' Caminho do python do venv
Dim python
python = projPath & "\..\venv\Scripts\python.exe"

' Inicia o Streamlit com headless=true para nao abrir browser automaticamente
' 0 = janela oculta, False = nao aguarda terminar
Dim cmd
cmd = """" & python & """ -m streamlit run """ & projPath & "\crm_app.py"" --server.headless true --server.port 8501"
shell.Run "cmd /c " & cmd, 0, False

' Aguarda 5 segundos para o Streamlit subir e entao abre o Firefox
WScript.Sleep 5000
shell.Run "http://localhost:8501", 1, False

Set shell = Nothing
