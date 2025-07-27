import streamlit as st
import time
import difflib
import uuid
from datetime import datetime

# 初始化session_state
if 'conversations' not in st.session_state:
    st.session_state.conversations = {}

if 'current_conversation' not in st.session_state:
    st.session_state.current_conversation = None


# 生成模拟代码差异的函数
def generate_code_diff(old_code, new_code):
    diff = difflib.unified_diff(
        old_code.splitlines(keepends=True),
        new_code.splitlines(keepends=True),
        fromfile='old.py',
        tofile='new.py',
        n=3
    )
    return ''.join(diff)


# 模拟模型响应函数
def get_model_response(user_input):
    # 模拟思考时间
    time.sleep(1)

    # 模拟模型响应
    responses = [
        "我理解你的需求，下面是修改后的代码：",
        "根据你的要求，我对代码进行了以下优化：",
        "我改进了代码的可读性和性能：",
        "下面是针对你需求的代码实现："
    ]

    # 模拟代码变化
    code_examples = [
        ("""def calculate_sum(a, b):
    return a + b""",
         """def calculate_sum(a, b):
    # 计算两个数的和
    return a + b"""),

        ("""for i in range(10):
    print(i)""",
         """# 打印0到9的数字
for num in range(10):
    print(num)"""),

        ("""data = load_data()
process(data)""",
         """# 加载并处理数据
data = load_data()
processed_data = process(data)"""),

        ("""def old_function():
    # 旧实现
    return result""",
         """def new_function():
    # 优化后的实现
    optimized_result = better_algorithm()
    return optimized_result""")
    ]

    old_code, new_code = code_examples[len(user_input) % len(code_examples)]
    code_diff = generate_code_diff(old_code, new_code)

    return f"{responses[len(user_input) % len(responses)]}\n\n```diff\n{code_diff}\n```"


# 创建新对话
def create_new_conversation():
    conv_id = str(uuid.uuid4())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    title = f"对话 {len(st.session_state.conversations) + 1} - {timestamp}"

    st.session_state.conversations[conv_id] = {
        'id': conv_id,
        'title': title,
        'messages': [],
        'code_diffs': []
    }
    st.session_state.current_conversation = conv_id
    return conv_id


# 页面布局
st.set_page_config(layout="wide", page_title="AI 代码助手", page_icon="💬")
st.title("💬 AI 代码助手")

# 创建三列布局
left_col, middle_col, right_col = st.columns([1, 2, 2])

# 左侧栏 - 对话管理
with left_col:
    st.subheader("对话管理")

    # 新建对话按钮
    if st.button("➕ 新建对话", use_container_width=True):
        create_new_conversation()

    st.divider()

    # 历史对话列表
    st.subheader("历史对话")
    if not st.session_state.conversations:
        st.info("没有历史对话")
    else:
        for conv_id, conv in reversed(list(st.session_state.conversations.items())):
            if st.button(conv['title'], key=f"conv_{conv_id}",
                         use_container_width=True,
                         type="primary" if conv_id == st.session_state.current_conversation else "secondary"):
                st.session_state.current_conversation = conv_id

# 中间栏 - 聊天界面
with middle_col:
    st.subheader("对话内容")

    if st.session_state.current_conversation:
        conversation = st.session_state.conversations[st.session_state.current_conversation]

        # 显示聊天记录
        chat_container = st.container(height=500)
        with chat_container:
            for msg in conversation['messages']:
                if msg['role'] == 'user':
                    with st.chat_message("user", avatar="👤"):
                        st.write(msg['content'])
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(msg['content'])

        # 用户输入
        user_input = st.chat_input("输入你的提示词...", key="chat_input")

        if user_input:
            # 添加用户消息
            conversation['messages'].append({
                'role': 'user',
                'content': user_input,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })

            # 获取模型响应
            model_response = get_model_response(user_input)

            # 添加模型响应
            conversation['messages'].append({
                'role': 'assistant',
                'content': model_response,
                'timestamp': datetime.now().strftime("%H:%M:%S")
            })

            # 提取并存储代码差异
            if "```diff" in model_response:
                diff_start = model_response.find("```diff") + 7
                diff_end = model_response.find("```", diff_start)
                code_diff = model_response[diff_start:diff_end].strip()
                conversation['code_diffs'].append(code_diff)

            # 刷新页面显示最新消息
            st.rerun()
    else:
        st.info("请创建一个新对话或选择一个历史对话")

# 右侧栏 - 代码变化展示
with right_col:
    st.subheader("代码变化")

    if st.session_state.current_conversation:
        conversation = st.session_state.conversations[st.session_state.current_conversation]

        if not conversation['code_diffs']:
            st.info("暂无代码变化")
        else:
            # 使用标签页展示不同版本的代码变化
            tabs = st.tabs([f"修改 #{i + 1}" for i in range(len(conversation['code_diffs']))])

            for i, tab in enumerate(tabs):
                with tab:
                    st.caption(f"版本 {i + 1} - 基于对话: {conversation['messages'][i * 2]['content'][:30]}...")
                    st.code(conversation['code_diffs'][i], language='diff')
    else:
        st.info("请创建一个新对话或选择一个历史对话")

# 添加一些样式美化
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stChatMessage {
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 12px;
    }
    [data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 8px 8px 0 0;
    }
</style>
""", unsafe_allow_html=True)