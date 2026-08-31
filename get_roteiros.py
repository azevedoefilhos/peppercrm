import subprocess
r = subprocess.run(['git','show','HEAD:roteiros.py'], capture_output=True)
with open('roteiros_work.py','wb') as f: f.write(r.stdout)
print(f"OK: {len(r.stdout)} bytes")
