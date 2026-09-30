import streamlit as st
from PyPDF2 import PdfMerger, PdfReader
from reportlab.pdfgen import canvas
import io
import pytesseract
from PIL import Image

# Configuração da página do Streamlit
st.set_page_config(page_title="Gerenciador de PDF All-in-One", page_icon="📄", layout="wide")
st.title("📄 Sistema Inteligente de Gestão de PDF")
st.write("Gere, junte, extraia textos (OCR) e envie para assinatura digital em um só lugar.")

# Abas do Sistema
tab1, tab2, tab3, tab4 = st.tabs(["✨ Gerar PDF", "🔀 Mesclar PDFs", "🔍 OCR (Extrair Texto)", "✍️ Assinatura Digital"])

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
# TAB 3: OCR (EXTRAIR TEXTO)
# ----------------------------------------------------
with tab3:
    st.header("OCR - Extrair Texto de Imagem ou PDF Digitalizado")
    arquivo_ocr = st.file_uploader("Carregue uma imagem do documento (PNG, JPG)", type=["png", "jpg", "jpeg"])
    
    if arquivo_ocr:
        imagem = Image.open(arquivo_ocr)
        st.image(imagem, caption="Imagem Carregada", width=300)
        
        if st.button("Executar OCR"):
            with st.spinner("Processando texto..."):
                try:
                    texto_extraido = pytesseract.image_to_string(imagem, lang='por')
                    st.subheader("Texto Extraído:")
                    st.text_area("Resultado", texto_extraido, height=250)
                except Exception as e:
                    st.error("Para executar o OCR localmente, certifique-se de ter o Tesseract-OCR instalado no sistema.")

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
