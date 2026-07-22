import subprocess
exec(open("fix_configuracao.py","rb").read())
exec(open("fix_crm_app.py","rb").read())
subprocess.run(["git","add","configuracao.py","crm_app.py"])
r=subprocess.run(["git","commit","-m","feat: minha conta em configuracao por perfil"],capture_output=True,text=True)
print("Commit:",r.stdout.strip() or r.stderr.strip())
r2=subprocess.run(["git","push"],capture_output=True,text=True)
print("Push:",r2.stdout.strip() or r2.stderr.strip())
