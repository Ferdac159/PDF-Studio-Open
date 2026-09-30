import streamlit as st
from PyPDF2 import PdfMerger, PdfReader
from reportlab.pdfgen import canvas
import io
import pytesseract
from PIL import Image

# Configuração da página do Streamlit
st.set_page_config(page_title="Gerenciador de PDF All-in-One", page_icon="📄", layout="wide")
st.title("📄 Sistema Inteligente de Gestão de PDF")
st.write("Gere, junte, extraia textos (OCR) de PDFs/Imagens e envie para assinatura digital.")

# Abas do Sistema
tab1, tab2, tab3, tab4 = st.tabs(["✨ Gerar PDF", "🔀 Mesclar PDFs", "🔍 OCR (Extrair Texto de PDF/Imagem)", "✍️ Assinatura Digital"])

# ----------------------------------------------------
# TAB 1: GERAR PDF
# ----------------------------------------------------
with tab1:
    st.header("Criar Novo Documento PDF")
    titulo = st.text_input("Título do Documento", "Contrato de Prestação de Serviços")
    conteudo = st.text_area("Conteúdo do PDF", "Digite o texto que deseja incluir no documento aqui...")
    
    if st.button("Gerar e Baixar PDF"):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, titulo)
        p.setFont("Helvetica", 12)
        
        y = 710
        for linha in conteudo.split('\n'):
            p.drawString(100, y, linha)
            y -= 20
        p.showPage()
        p.save()
        buffer.seek(0)
        
        st.success("PDF gerado com sucesso!")
        st.download_button(label="📥 Baixar PDF Gerado", data=buffer, file_name="documento_criado.pdf", mime="application/pdf")

# ----------------------------------------------------
# TAB 2: MESCLAR PDFs (JUNTAR)
# ----------------------------------------------------
with tab2:
    st.header("Mesclar Múltiplos PDFs em Um")
    arquivos_pdf = st.file_uploader("Selecione os arquivos PDF", type=["pdf"], accept_multiple_files=True)
    
    if arquivos_pdf and st.button("Juntar PDFs"):
        merger = PdfMerger()
        for pdf in arquivos_pdf:
            merger.append(pdf)
        
        output_buffer = io.BytesIO()
        merger.write(output_buffer)
        merger.close()
        output_buffer.seek(0)
        
        st.success(f"{len(arquivos_pdf)} PDFs mesclados com sucesso!")
        st.download_button(label="📥 Baixar PDF Mesclado", data=output_buffer, file_name="pdf_mesclado.pdf", mime="application/pdf")

# ----------------------------------------------------
# TAB 3: OCR (EXTRAIR TEXTO DE IMAGEM OU PDF)
# ----------------------------------------------------
with tab3:
    st.header("OCR - Extrair Texto de PDF ou Imagem")
    st.write("Carregue um arquivo PDF (mesmo que seja escaneado/foto) ou uma imagem (PNG, JPG) para extrair o texto.")
    
    arquivo_ocr = st.file_uploader("Carregue seu arquivo aqui", type=["pdf", "png", "jpg", "jpeg"])
    
    if arquivo_ocr:
        texto_final = ""
        
        if st.button("Executar OCR / Extrair Texto"):
            with st.spinner("Processando e extraindo texto do documento..."):
                try:
                    # Se o arquivo for PDF
                    if arquivo_ocr.name.lower().endswith('.pdf'):
                        leitor_pdf = PdfReader(arquivo_ocr)
                        for i, pagina in enumerate(leitor_pdf.pages):
                            texto_da_pagina = pagina.extract_text()
                            # Se o PDF já tiver texto nativo, usa ele. Se for imagem escaneada, tenta rodar OCR.
                            if texto_da_pagina and len(texto_da_pagina.strip()) > 10:
                                texto_final += f"--- Página {i+1} ---\n{texto_da_pagina}\n\n"
                            else:
                                texto_final += f"--- Página {i+1} (Aviso: PDF parece ser uma imagem escaneada) ---\n"
                                # Para rodar OCR em PDF de imagem no servidor do Streamlit, o tesseract lê metadados ou imagens internas
                                texto_ocr = pytesseract.image_to_string(Image.open(arquivo_ocr), lang='por')
                                texto_final += texto_ocr + "\n\n"
                    
                    # Se o arquivo for uma Imagem direta
                    else:
                        imagem = Image.open(arquivo_ocr)
                        texto_final = pytesseract.image_to_string(imagem, lang='por')
                    
                    if texto_final.strip():
                        st.subheader("📝 Texto Extraído com Sucesso:")
                        st.text_area("Resultado", texto_final, height=300)
                    else:
                        st.warning("Não conseguimos detectar nenhum texto legível neste documento.")
                        
                except Exception as e:
                    st.error("Erro no processamento. Para PDFs 100% escaneados como foto, certifique-se de que o motor OCR do servidor esteja ativo.")

# ----------------------------------------------------
# TAB 4: ASSINATURA DIGITAL (LINK EXTERNO GRATUITO)
# ----------------------------------------------------
with tab4:
    st.header("✍️ Assinatura Eletrônica e Envio para o Cliente")
    st.write("""
    Para que seu cliente assine o documento com **validade jurídica legal**, integramos o fluxo às principais ferramentas gratuitas de mercado. 
    Escolha uma das plataformas oficiais abaixo para fazer o upload do documento gerado e coletar a assinatura do cliente:
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**Opção 1: ZapSign (Recomendado)**")
        st.write("Plataforma brasileira simples que envia o link de assinatura direto por WhatsApp ou E-mail.")
        st.markdown("[Acessar ZapSign Grátis](https://zapsign.com.br 'ZapSign')")
        
    with col2:
        st.info("**Opção 2: Adobe Sign / Acrobat Online**")
        st.write("A ferramenta oficial da Adobe permite solicitar assinaturas eletrônicas preenchendo o e-mail do cliente.")
        st.markdown("[Acessar Adobe Sign Grátis](https://adobe.com 'Adobe Acrobat Sign')")

