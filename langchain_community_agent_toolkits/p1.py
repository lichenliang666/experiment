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


async def modify_main_py(user_instruction: str, llm, agent_executor, config: RunnableConfig) -> str:
    file_path = "working_directory/xx_game/main.py"

    # 读取当前 main.py 的内容
    read_result = await agent_executor.ainvoke({
        "input": f"请读取以下文件内容：{file_path}"
    }, config=config)

    current_code = read_result.get("output", "")

    # 构造 LLM prompt
    prompt = (
        f"以下是一个 pygame 编写的 Python 游戏代码（main.py 文件）：\n\n"
        f"{current_code}\n\n"
        f"用户提出如下修改建议：{user_instruction}\n\n"
        f"请你根据这些建议，修改这段代码并输出完整修改后的代码。"
    )

    # 直接调用 LLM，不走 agent_executor
    from langchain_core.messages import HumanMessage
    llm_result = await llm.ainvoke([HumanMessage(content=prompt)], config=config)
    modified_code = llm_result.content

    # 写入文件
    write_result = await agent_executor.ainvoke({
        "input": f"请将以下内容写入 {file_path} 文件中：\n\n{modified_code}"
    }, config=config)

    return "游戏已修改完成。"


# ------------------------ LangGraph Agent ------------------------

# 初始化 LLM
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    api_key=os.environ["DEEPSEEK_API_KEY"]
)

# 自定义提示词
prompt = """
你是一个 pygame 游戏开发助手。

你具备以下能力：
1. 创建新游戏项目，使用 init_game_project 工具。
2. 为项目生成 main.py，使用 generate_main_py 工具。
3. 读取文件使用 read_file，修改后保存使用 write_file。
4. 用户说“在 xx 游戏中添加 xx 功能”，你应先使用 read_file 读取 main.py，
   再在原有代码的基础上插入新的 pygame 功能，最后使用 write_file 写回文件。
5. 文件路径必须以 working_directory 开头，并对应用户提到的项目名目录。

不要编写注释解释代码，仅输出实际修改内容。
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
        result = graph.invoke({"messages": [{"role": "user", "content": user_input}]}, config=RunnableConfig())
        last = result["messages"][-1]
        print(f"\n🤖 Agent 回复:\n{last.content}\n")


if __name__ == "__main__":
    main()
