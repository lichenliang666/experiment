
我打算使用Python（3.11版本）编写个由大模型驱动的Agent。
核心功能是根据用户的输入创建游戏项目并编写代码。
当用户说新建个名叫xx游戏时会自动创建游戏项目目录。
游戏框架使用pygame库，并使用pyproject.toml文件来管理项目依赖。
使用 uv 管理项目的依赖。
并根据用户的描述编写游戏代码，并保存到指定的目录下。
这个Agent使用LangGraph框架调用LLM和Mcp工具或langchain的工具。
在这个程序中使用langchain_community.agent_toolkits下的
FileManagementToolkit工具用来把LLM写的代码直接保存在working_directory目录下。
希望这个程序可以自动创建一个游戏项目，并自动生成游戏的代码。
使用 langgraph 中的 create_react_agent 创建 Agent。
为了这个Agent能够更好的工作，请我写好描述这个Agent的prompt。
下面是我已经编写的一些代码，请参考这些代码的，帮我写个完整的Agent代码。
代码如下：
```python
from langchain_deepseek import ChatDeepSeek
from langchain_community.agent_toolkits import FileManagementToolkit
from langgraph.prebuilt import create_react_agent
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
working_directory = os.path.join(current_dir, "working_directory")
toolkit = FileManagementToolkit(
    root_dir=str(working_directory.name)
)
copy_file, file_delete, file_search, move_file, read_file, write_file, list_directory = toolkit.get_tools()
tools = [
    copy_file, file_delete, file_search, move_file, read_file, write_file, list_directory
]
llm = ChatDeepSeek(
    model="deepseek-chat",  # DeepSeek 模型名称
    temperature=0.5,  # 温度参数，控制生成结果的随机性
    max_retries=2,  # 最大重试次数
    api_key=os.environ["DEEPSEEK_API_KEY"]  # 替换为你的 DeepSeek API 密钥
)

agent = create_react_agent(
    model=llm,
    tools=tools
)

def main():
    print("this is coder agent of game!")

if __name__ == "__main__":
    main()

```


















