from langgraph_agent import run_game_agent

import streamlit as st

st.set_page_config(page_title="Game Agent 工作台", layout="wide")
st.title("🎮 Game Project Agent")

user_input = st.text_area("请输入你对游戏项目的需求：", height=150)

if st.button("生成游戏代码"):
    with st.spinner("Agent 正在思考中..."):
        response = run_game_agent(user_input)
    st.success("Agent 已完成生成：")
    st.code(response, language="markdown")
