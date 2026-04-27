import streamlit
print(f"Streamlit versão: {streamlit.__version__}")

# Verifica se st.tabs aceita key=
import inspect
sig = inspect.signature(streamlit.tabs)
print(f"Parâmetros de st.tabs: {list(sig.parameters.keys())}")
print()
if 'key' in sig.parameters:
    print("✅ st.tabs suporta key= nesta versão")
else:
    print("❌ st.tabs NÃO suporta key= nesta versão")
    print("   key= foi adicionado no Streamlit 1.31.0")
    print("   A solução é usar session_state para persistir a aba ativa")
input("\nEnter para fechar...")
