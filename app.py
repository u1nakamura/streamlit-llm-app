from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from dotenv import load_dotenv
import os

# .envの読み込み
load_dotenv()

# LangChainのLLM初期化（OpenAI APIキーは.envに設定済みである前提）
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

# 専門家ごとのシステムプロンプト
expert_messages = {
    "医療の専門家": "あなたは患者の症状や健康相談に優しく丁寧に答える医療の専門家です。",
    "法律の専門家": "あなたは一般市民の法律相談に対して的確かつ平易に説明する弁護士です。",
}

# LLMへの問い合わせ関数
def ask_llm(user_input: str, expert_type: str) -> str:
    system_prompt = expert_messages.get(expert_type, "あなたは優秀なアシスタントです。")
    prompt = ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_prompt),
        HumanMessagePromptTemplate.from_template("{question}")
    ])
    chain = LLMChain(llm=llm, prompt=prompt)
    response = chain.run({"question": user_input})
    return response

# Streamlit UI構成
st.title("🧠 専門家に質問できるLLMアプリ")
st.write("以下のフォームに質問を入力し、専門家の種類を選択して送信してください。")

expert_type = st.radio("専門家の種類を選択してください", list(expert_messages.keys()))
user_input = st.text_area("質問を入力してください")

if st.button("送信"):
    if user_input.strip():
        with st.spinner("回答を生成中..."):
            answer = ask_llm(user_input, expert_type)
        st.success("回答:")
        st.write(answer)
    else:
        st.warning("質問を入力してください。")