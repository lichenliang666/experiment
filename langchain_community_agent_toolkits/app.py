import streamlit as st
import os
from pathlib import Path
import shutil

# 选择框架与模板路径映射
FRAMEWORK_TEMPLATES = {
    "pygame": "templates/pygame_main.py",
    "arcade": "templates/arcade_main.py",
}

st.title("🎮 游戏项目生成器")

# 选择框架
framework = st.selectbox("选择游戏框架", list(FRAMEWORK_TEMPLATES.keys()))

# 输入项目名
project_name = st.text_input("输入项目名称", "my_game")

# 生成项目
if st.button("🎉 创建游戏项目"):
    if not project_name:
        st.warning("请输入有效的项目名称")
    else:
        project_dir = Path("generated_projects") / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        # 复制模板文件
        template_path = FRAMEWORK_TEMPLATES[framework]
        target_file = project_dir / "main.py"
        shutil.copy(template_path, target_file)

        st.success(f"项目已创建于：{project_dir.resolve()}")

        # 显示代码内容
        with open(target_file, "r", encoding="utf-8") as f:
            st.code(f.read(), language="python")
