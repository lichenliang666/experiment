import os
from typing import TypedDict, List

from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent

# 初始化工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))
working_directory = os.path.join(current_dir, "working_directory")
os.makedirs(working_directory, exist_ok=True)

# ------------------------ 工具定义 ------------------------

# 文件管理工具
toolkit = FileManagementToolkit(root_dir=working_directory)
copy_file, file_delete, file_search, move_file, read_file, write_file, list_directory = toolkit.get_tools()
tools = [copy_file, file_delete, file_search, move_file, read_file, write_file, list_directory]


# 项目初始化工具
@tool
def init_game_project(project_name: str) -> str:
    """初始化一个新的游戏项目，包括目录结构和 pyproject.toml 文件"""
    project_dir = os.path.join(working_directory, project_name)
    os.makedirs(project_dir, exist_ok=True)

    pyproject = f"""[project]
name = "{project_name}"
version = "0.1.0"
dependencies = ["pygame"]

[tool.uv]
"""

    with open(os.path.join(project_dir, "pyproject.toml"), "w", encoding="utf-8") as f:
        f.write(pyproject)

    return f"{project_name} 项目已创建，路径：{project_dir}"


tools.append(init_game_project)


# 生成 main.py 文件工具
@tool
def generate_main_py(project_name: str) -> str:
    """为指定项目生成一个基本的 pygame main.py 文件"""
    code = '''import pygame
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("My Game")
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))  # 深灰背景
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
'''
    file_path = os.path.join(working_directory, project_name, "main.py")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)

    return f"main.py 已生成：{file_path}"


tools.append(generate_main_py)

# ------------------------ LangGraph Agent ------------------------

# 初始化 LLM
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.5,
    api_key=os.environ["DEEPSEEK_API_KEY"]
)

# 自定义提示词
prompt = """
你是一个 pygame 游戏项目助手，擅长帮助用户创建基于 pygame 的 2D 游戏项目。

你必须：
1. 当用户说“创建一个名为 xxx 的游戏”时，调用 init_game_project 工具。
2. 然后立即调用 generate_main_py 工具，为该项目生成 main.py 游戏入口文件。
3. 所有项目文件必须写入 working_directory 下的子目录中。
"""

# 创建 Agent
agent = create_react_agent(
    model=llm,
    tools=tools,
    prompt=prompt
)


# ------------------------ LangGraph 流程定义 ------------------------

class AgentState(TypedDict):
    messages: List[dict]


builder = StateGraph(AgentState)
builder.add_node("agent", agent)
builder.set_entry_point("agent")
builder.add_edge("agent", END)

graph = builder.compile()


# ------------------------ 主程序 ------------------------

def main():
    print("🎮 游戏生成 Agent 已启动，输入 'exit' 退出。")
    while True:
        user_input = input(">>> ")
        if user_input.strip().lower() in {"exit", "quit"}:
            break
        result = graph.invoke({
            "messages": [{"role": "user", "content": user_input}]
        }, config=RunnableConfig())
        last = result["messages"][-1]
        print(f"\n🤖 Agent 回复:\n{last.content}\n")


if __name__ == "__main__":
    main()
