import streamlit as st
import os
import shutil
from drive_utils import download_file
from pdf_utils import merge_pdfs

st.set_page_config(page_title="PDF Merge by G-Drive Links", page_icon="📄", layout="centered")

st.title("PDF Merge by G-Drive Links")
st.markdown("Agrupe múltiplos arquivos PDF do Google Drive em um único documento.")

with st.expander("ℹ️ Instruções", expanded=False):
    st.markdown("""
    1. **Links Públicos**: Certifique-se de que os arquivos no Drive estão configurados como **"Qualquer pessoa com o link"**.
    2. **Colar Links**: Cole os links abaixo. Você pode colar um por linha ou separá-los por espaço.
    3. **Unificar**: Clique no botão para processar.
    4. **Salvar**: Baixe o arquivo final e use o atalho para abrir sua pasta do Drive e fazer o upload manual.
    """)

st.divider()

# Reset state function
def reset_state():
    st.session_state.links_input = ""
    st.session_state.folder_input = ""
    st.session_state.filename_input = "documento_unificado.pdf"

# Header & Reset Button
col_header, col_btn = st.columns([3, 1])
with col_header:
    st.subheader("1. Links dos Arquivos")
with col_btn:
    if st.button("🔄 Novo Merge", use_container_width=True):
        reset_state()
        st.rerun()
links_input = st.text_area(
    "Cole os links dos PDFs aqui:", 
    height=200,
    placeholder="https://drive.google.com/file/d/...\nhttps://drive.google.com/file/d/...",
    key="links_input"
)

st.subheader("2. Configurações")
output_filename = st.text_input("Nome do Arquivo Final:", value="documento_unificado.pdf", key="filename_input")
if not output_filename.endswith('.pdf'):
    output_filename += ".pdf"
    
folder_link_input = st.text_input("Link da Pasta de Destino (Opcional):", placeholder="Para facilitar o upload manual depois", key="folder_input")

st.divider()

if st.button("Unificar Arquivos", type="primary", use_container_width=True):
    if not links_input.strip():
        st.error("⚠️ Por favor, insira pelo menos um link de PDF.")
    else:
        # Process
        with st.status("Processando...", expanded=True) as status:
            # Setup temp dir
            temp_dir = "temp_pdfs"
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            
            # 1. Parse Links
            raw_text = links_input.replace('\n', ' ').replace('\t', ' ')
            links = [l.strip() for l in raw_text.split() if l.strip()]
            
            if not links:
                status.update(label="Nenhum link encontrado!", state="error")
                st.stop()
                
            status.write(f"🔍 {len(links)} links encontrados. Iniciando download...")
            failed_files = []
            downloaded_files = []
            
            # 2. Download Files
            progress_bar = status.progress(0)
            
            for i, link in enumerate(links):
                output_path = os.path.join(temp_dir, f"arquivo_{i}.pdf")
                status.write(f"Baixando arquivo {i+1}...")
                
                success, msg = download_file(link, output_path)
                
                if success:
                    downloaded_files.append(output_path)
                else:
                    status.write(f"❌ Falha no arquivo {i+1}")
                    failed_files.append({
                        'index': i + 1,
                        'link': link,
                        'msg': msg
                    })
                
                progress_bar.progress((i + 1) / len(links))
            
            if failed_files:
                status.update(label=f"❌ Problemas encontrados em {len(failed_files)} arquivo(s).", state="error")
                
                st.error("⚠️ **Atenção: Não foi possível baixar todos os arquivos.**")
                
                st.markdown("Confira a lista de erros abaixo:")
                
                for fail in failed_files:
                    with st.expander(f"❌ Arquivo {fail['index']} (Clique para detalhes)"):
                        st.markdown(f"**Link:** `{fail['link']}`")
                        st.divider()
                        st.info(f"**Diagnóstico:** {fail['msg']}")
                        st.caption("Dica: Verifique se o link está público ('Qualquer pessoa') e se o arquivo existe.")
                
                st.warning("🛑 **A unificação foi cancelada.** Corrija os links acima e tente novamente.")
                st.stop()

            if not downloaded_files:
                status.update(label="Nenhum arquivo válido encontrado.", state="error")
                st.stop()

            # 3. Merge
            status.write("📂 Unificando PDFs...")
            merged_pdf_path = os.path.join(temp_dir, output_filename)
            success, msg = merge_pdfs(downloaded_files, merged_pdf_path)
            
            if not success:
                status.update(label=f"Erro ao Unificar: {msg}", state="error")
                st.stop()
            
            status.update(label="Concluído!", state="complete")
            st.success("✅ Arquivos unificados com sucesso!")
            
            # 4. Provide Downloader
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                with open(merged_pdf_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Baixar PDF Unificado",
                        data=f,
                        file_name=output_filename,
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
            
            # 5. Link to Folder
            with col_res2:
                if folder_link_input:
                    st.link_button("📂 Abrir Pasta no Drive", folder_link_input, use_container_width=True)
                else:
                    st.caption("Dica: Informe o link da pasta para ver o atalho aqui.")

