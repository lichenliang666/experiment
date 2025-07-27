import streamlit as st
from langgraph_agent import run_game_agent

st.title("🕹️ 游戏生成助手")

user_input = st.text_area("请输入你的游戏想法：", height=150)
mode = st.radio("模式选择", ["new", "modify"])
project_dir = "projects/my_game"

if st.button("生成代码"):
    if user_input:
        with st.spinner("正在生成代码，请稍候..."):
            result = run_game_agent(project_dir, user_input, mode)
            st.code(result, language="python")
    else:
        st.warning("请先输入游戏需求！")
