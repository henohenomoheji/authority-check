import mimetypes

import streamlit as st

from src.image_interpretation import (
    ImageTooLargeError,
    InterpretationRequest,
    InvalidImageFormatError,
    InvalidPromptError,
    MissingConfigurationError,
    ModelTimeoutError,
    ModelUnavailableError,
    interpret_image,
)

st.title("画像解釈")
st.caption("画像と指示プロンプトを入力し、説明文を生成します。")

uploaded_file = st.file_uploader(
    "画像ファイルを選択",
    type=["png", "jpg", "jpeg", "webp"],
    accept_multiple_files=False,
)
instruction_prompt = st.text_area(
    "指示プロンプト（任意）",
    placeholder="例: 200文字以内で要点を箇条書きで説明してください。",
    max_chars=2000,
)

if st.button("解釈実行", type="primary"):
    if uploaded_file is None:
        st.error("画像をアップロードしてください。")
        st.stop()

    image_bytes = uploaded_file.getvalue()
    mime_type = uploaded_file.type or mimetypes.guess_type(uploaded_file.name)[0] or "image/jpeg"

    req = InterpretationRequest(
        image_bytes=image_bytes,
        filename=uploaded_file.name,
        mime_type=mime_type,
        instruction_prompt=instruction_prompt,
    )

    try:
        with st.spinner("画像を解釈中です..."):
            result = interpret_image(req)
        st.success("説明文を生成しました。")
        st.markdown("### 生成結果")
        st.write(result.description_text)

        with st.expander("実行メタ情報"):
            st.write("request_id:", result.request_id)
            st.write("model_name:", result.model_name)
            st.write("latency_ms:", result.latency_ms)

    except InvalidImageFormatError:
        st.error("対応外の画像形式です。")
    except ImageTooLargeError:
        st.error("画像サイズが上限を超えています。")
    except InvalidPromptError as exc:
        st.error(str(exc))
    except MissingConfigurationError as exc:
        st.error(f"設定エラー: {exc}")
    except ModelTimeoutError:
        st.error("時間をおいて再実行してください。")
    except ModelUnavailableError:
        st.error("現在利用できません。")
