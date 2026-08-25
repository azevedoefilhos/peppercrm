from dotenv import load_dotenv; load_dotenv()
import sys; sys.path.insert(0,'.')
from database import query

r = query("""SELECT column_name FROM information_schema.columns
    WHERE table_name='pedido' ORDER BY ordinal_position""")
print("Campos da tabela pedido:")
for col in (r or []):
    print(f"  {col[0]}")
