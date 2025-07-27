from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_deepseek import ChatDeepSeek
from pathlib import Path
from typing import Literal
import os

# 初始化模型
def get_model():
    return ChatDeepSeek(temperature=0, model="deepseek-chat")

# 初始化工具
def get_tools(project_dir: str):
    root = Path(project_dir)
    root.mkdir(parents=True, exist_ok=True)
    toolkit = FileManagementToolkit(root_dir=root)
    return toolkit.get_tools()

# 创建 Agent
def build_agent(model, tools):
    return create_react_agent(
        model=model,
        tools=tools,
        prompt="你是一个游戏项目生成与修改助手，用户会告诉你他们想要的新游戏内容，或者对已有游戏的修改，你要调用文件工具完成操作。"
    )

# 构建 LangGraph StateGraph
def build_graph(agent):
    builder = StateGraph()
    builder.add_node("agent", agent)
    builder.set_entry_point("agent")
    builder.add_edge("agent", END)
    return builder.compile()

# 主处理逻辑（可以被 run_game_agent 调用）
def generate_or_modify_code(project_dir: str, user_input: str, mode: Literal["new", "modify"]) -> str:
    os.makedirs(project_dir, exist_ok=True)
    model = get_model()
    tools = get_tools(project_dir)
    agent = build_agent(model, tools)
    graph = build_graph(agent)

    messages = [
        HumanMessage(content=f"我想要 {'创建一个新游戏：' if mode == 'new' else '修改这个游戏：'}{user_input}")
    ]

    config = RunnableConfig(configurable={"recursion_limit": 5})
    result = graph.invoke({"messages": messages}, config=config)

    main_path = Path(project_dir) / "main.py"
    if main_path.exists():
        return main_path.read_text(encoding="utf-8")
    else:
        return "main.py 未生成或不存在。"

# 为 app.py 暴露的统一接口
def run_game_agent(project_dir: str, user_input: str, mode: Literal["new", "modify"]) -> str:
    return generate_or_modify_code(project_dir, user_input, mode)

# 示例用法
if __name__ == "__main__":
    result = run_game_agent("projects/test_game", "创建一个有可移动角色的2D游戏", mode="new")
    print(result)
