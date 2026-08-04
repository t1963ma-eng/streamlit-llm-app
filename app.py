import os
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

# ローカル実行時は.envから、Streamlit Cloud上ではSecretsから読み込む
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# ---------------------------------------------------
# 画面表示：アプリの概要と操作方法
# ---------------------------------------------------
st.title("専門家AI相談アプリ")

st.write("##### このアプリについて")
st.write(
    """
    このアプリは、入力したテキストをLLM（大規模言語モデル）に送信し、
    選択した専門家の立場から回答してもらうWebアプリです。
    """
)

st.write("##### 操作方法")
st.write(
    """
    1. ラジオボタンで、回答してほしい専門家の種類を選択してください。
    2. 入力フォームに質問や相談内容を入力してください。
    3. 「実行」ボタンを押すと、選択した専門家としてLLMが回答します。
    """
)

st.write("##### 選択できる専門家")
st.write(
    """
    - **キャリアカウンセラー**：転職・キャリア形成に関する相談に回答します。
    - **栄養士**：食事・栄養に関する相談に回答します。
    """
)

st.divider()


# ---------------------------------------------------
# 「入力テキスト」と「ラジオボタンの選択値」を受け取り、
# LLMからの回答を返す関数
# ---------------------------------------------------
def get_llm_response(input_text, selected_item):
    # 選択された専門家に応じてシステムメッセージを切り替える
    if selected_item == "キャリアカウンセラー":
        system_message = (
            "あなたは経験豊富なキャリアカウンセラーです。"
            "転職やキャリア形成に関する相談に対して、"
            "専門的な知見に基づき、具体的かつ分かりやすくアドバイスしてください。"
        )
    else:  # 栄養士
        system_message = (
            "あなたは管理栄養士です。"
            "食事や栄養に関する相談に対して、"
            "科学的根拠に基づき、実践しやすいアドバイスを分かりやすく回答してください。"
        )

    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=input_text),
    ]

    result = llm.invoke(messages)
return result.content


# ---------------------------------------------------
# 画面：ラジオボタン・入力フォーム・実行ボタン
# ---------------------------------------------------
selected_item = st.radio(
    "**質問する専門家を選択してください。**",
    ["キャリアカウンセラー", "栄養士"],
)

st.divider()

input_message = st.text_area(label="**質問・相談内容を入力してください。**")

if st.button("実行"):
    st.divider()
    if input_message:
        with st.spinner("LLMが回答を作成しています..."):
            response = get_llm_response(input_message, selected_item)
        st.write("##### 回答")
        st.write(response)
    else:
        st.warning("質問内容を入力してください。")