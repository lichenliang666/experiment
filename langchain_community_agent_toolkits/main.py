
from langchain_deepseek import ChatDeepSeek
from langchain_community.agent_toolkits import FileManagementToolkit
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
working_directory = os.path.join(current_dir, "working_directory")
toolkit = FileManagementToolkit(
    root_dir=str(working_directory.name)
)
copy_file, file_delete, file_search, move_file, read_file, write_file, list_directory = toolkit.get_tools()
llm = ChatDeepSeek(
    model="deepseek-chat",  # DeepSeek 模型名称
    temperature=0.5,  # 温度参数，控制生成结果的随机性
    timeout=50,  # 请求超时时间
    max_retries=2,  # 最大重试次数
    api_key=os.environ["DEEPSEEK_API_KEY"]  # 替换为你的 DeepSeek API 密钥
)

def main():
    print("this is coder agent of game!")

if __name__ == "__main__":
    main()

