"""
Interface Web do Gerador de QR Code (Streamlit)
=================================================

Instalação das dependencias:
    pip install streamlit qrcode[pill]

Como rodar:
    streamlit run qrcode_app.py
"""

import io
import streamlit as st

try:
    import qrcode
    from qrcode.constants import (
        ERROR_CORRECT_L,
        ERROR_CORRECT_H,
        ERROR_CORRECT_M,
        ERROR_CORRECT_Q,
    )
except ImportError:
    st.error('A biblioteca "qrcode" não está instalada. Rode: pip install qrcode[pill]')
    st.stop()


NIVEIS_CORRECAO = {
    "L - baixo (~7%)": ERROR_CORRECT_L,
    "M - médio (~15%)": ERROR_CORRECT_M,
    "Q - alto (~25%)": ERROR_CORRECT_Q,
    "H - máximo (~30%)": ERROR_CORRECT_H,
}


def gerar_qrcode(
    conteudo: str,
    cor_frente: str = "black",
    cor_fundo: str = "white",
    tamanho_caixa: int = 10,
    borda: int = 4,
    nivel_correcao=ERROR_CORRECT_M,
) -> "qrcode.image.pill.PilImage":
    """
    Gera uma imagem de QR Code a partir do conteúdo informado.

    Args:
        conteudo: Texto, URL ou dado a ser codificado no QR Code.
        cor_frente: Cor dos módulos de QR Code  (nome ou hex, ex:"#1a1a2e" ).
        cor_fundo: Cor de fundo (nome ou hex).
        tamanho_caixa: Tamanho em pixels de cada módulo do QR Code.
        borda: Espessura da borda em número de módulos.
        nivel_correcao: Constante de nivel de correção de erro do qrcode
            (ERROR_CORRECT_L, _M, _Q ou _H).

    Returns:
        Objeto de imagem PIL pronto para ser exibido ou salvo.
    """

    qr = qrcode.QRCode(
        version=None,
        error_correction=nivel_correcao,
        box_size=tamanho_caixa,
        border=borda,
    )
    qr.add_data(conteudo)
    qr.make(fit=True)
    return qr.make_image(fill_color=cor_frente, back_color=cor_fundo)


def main():
    st.set_page_config(
        page_title="Gerador de QR Code", page_icon="🔳", layout="centered"
    )

    st.title("🔳 Gerador de QR Code")
    st.caption(
        "Gere QR Codes personalizados a partir de texto, links ou qualquer conteúdo."
    )

    with st.sidebar:
        st.header("Personalização")
        cor_frente = st.color_picker("Cor do QR Code", "#000000")
        cor_fundo = st.color_picker("Cor de fundo", "#FFFFFF")
        tamanho_caixa = st.slider(
            "Tamanho do módulo (px)", min_value=4, max_value=20, value=10
        )
        borda = st.slider("Borda (módulos)", min_value=0, max_value=10, value=4)
        nivel_label = st.selectbox(
            "Nível de correção de erro", list(NIVEIS_CORRECAO.keys()), index=1
        )

    conteudo = st.text_area(
        "Conteúdo do QR Code",
        placeholder="https://exemplo.com ou qualquer texto",
        height=100,
    )

    gerar = st.button("Gerar QR Code", type="primary", use_container_width=True)

    if gerar:
        if not conteudo.strip():
            st.warning("Digite algum conteudo antes de gerar o QR Code.")
        else:
            imagem = gerar_qrcode(
                conteudo=conteudo,
                cor_frente=cor_frente,
                cor_fundo=cor_fundo,
                tamanho_caixa=tamanho_caixa,
                borda=borda,
                nivel_correcao=NIVEIS_CORRECAO[nivel_label],
            )

            buffer = io.BytesIO()
            imagem.save(buffer, format="PNG")
            buffer.seek(0)

            st.image(buffer, caption="QR Code gerado", width=300)

            st.download_button(
                label="⬇️ Baixar PNG",
                data=buffer,
                file_name="qrcode.png",
                mime="image/png",
                use_container_width=True,
            )


if __name__ == "__main__":
    main()
