from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# OpenAI APIキーが環境変数で設定されていることを前提とします

# Streamlitアプリのタイトルと説明
st.set_page_config(page_title="専門家 LLM アシスタント")
st.title("🧠 専門家 LLM アシスタント")
st.markdown("""
このアプリでは、選択した専門家になりきるLLMに質問ができます。  
左のラジオボタンから専門家の種類を選び、質問を入力してください。
""")

# 専門家の選択
expert_type = st.radio(
    "以下の専門家から選んでください：",
    ["医師（健康相談）", "法律家（法律アドバイス）", "旅行プランナー（観光提案）"]
)

# ユーザー入力
user_input = st.text_input("質問を入力してください：", placeholder="例：最近寝つきが悪いのですが...")

# 専門家ごとのシステムメッセージ定義
def get_system_prompt(expert_type):
    if expert_type == "医師（健康相談）":
        return "あなたは優秀な日本人の医師です。ユーザーの健康相談に対して、丁寧かつ正確にアドバイスを行ってください。"
    elif expert_type == "法律家（法律アドバイス）":
        return "あなたは日本の法律に詳しい弁護士です。法的観点からユーザーの相談に明確に答えてください。"
    elif expert_type == "旅行プランナー（観光提案）":
        return "あなたは旅行会社で働くプロの旅行プランナーです。季節や場所を考慮しておすすめを提案してください。"
    else:
        return "あなたは博識なアシスタントAIです。親切に答えてください。"

# LLM応答関数
def ask_expert(question, expert_type):
    system_prompt = get_system_prompt(expert_type)

    # LangChainのプロンプトテンプレート
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("user", "{input}")
    ])

    chain = prompt | ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    response = chain.invoke({"input": question})
    return response.content

# 実行ボタン
if st.button("送信") and user_input:
    with st.spinner("専門家が回答中..."):
        output = ask_expert(user_input, expert_type)
        st.success("回答が届きました！")
        st.write(output)