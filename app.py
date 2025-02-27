import streamlit as st
# from google.cloud import vision  # 如果需要使用 Google Cloud Vision API
import os
from datetime import datetime
from pathlib import Path
import json
from openai import OpenAI

# import certifi
# os.environ['REQUESTS_CA_BUNDLE'] = ''
# os.environ['SSL_CERT_FILE'] = certifi.where()

from test2 import save_pdf

# os.environ["http_proxy"] = "http://localhost:80"
# os.environ["https_proxy"] = "http://localhost:80"

st.set_page_config(page_title="赛学科技AI助学",page_icon=":books:")

# 本地存储文件路
HISTORY_FILE = "conversation_history.json"

# 初始化对话历史记录
def load_history():
    """从本地文件加载对话历史记录"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    """将对话历史记录保存到本地文件"""
    if len(history)>10:
        history = history[0:10]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = load_history()



#################################################################################################

##千帆大模型
# # 设置API密钥
# import qianfan
# API_KEY = "L6Z7L2vqntbCOIxKhpNkz6sx"
# SECRET_KEY = "0IdXnuyElXjnRVagyodLmqMn4vL7jlB5"
# os.environ["QIANFAN_AK"] = API_KEY
# os.environ["QIANFAN_SK"] = SECRET_KEY


## DeepSeek
# 设置API密钥

DSapikey="sk-9f4bd55f1fde4089a109ba6a9dfb61e1"
client_DeepSeek = OpenAI(api_key=DSapikey, base_url="https://api.deepseek.com")


## Kimi(Moonshot)_vision
client_Kimi_vision = OpenAI(
    api_key="sk-LtiQZ51RYK17OI0WVYEaCUlMgRkyuWdxZpitcUOCpDXdfDc8", # <--在这里将 MOONSHOT_API_KEY 替换为你从 Kimi 开放平台申请的 API Key
    base_url="https://api.moonshot.cn/v1", # <-- 将 base_url 从 https://api.openai.com/v1 替换为 https://api.moonshot.cn/v1
)


## ChatGPT
# 设置API密钥
# os.environ["http_proxy"] = "http://localhost:7890"
# os.environ["https_proxy"] = "http://localhost:7890"
CGapikey = "93hO5ysDDUo3Em0I7NJplgwlpqWxDZggRlKYRozu5fOpejF5jNGqjHEyAM0wR1kvzk_K6bGiCyT3BlbkFJ4FLVTt74oL0vuEpWTp4iqp5LM4nJdUOzLZXyLzjNcteQO8s4iB7F86ajIW7dThPn6dtlEv9kMA"
client_ChatGPT = OpenAI(api_key=CGapikey)


## 阿里云百炼
ALiapikey = "sk-22c3dccf71ae4abf9c8d142d688dbc0b"
# 阿里云调用DeepSeek
client_Ali_DS = OpenAI(
    api_key=ALiapikey,  # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)


## Google Cloud
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path-to-your-google-cloud-credentials.json"  # 设置 Google Cloud 凭证

##################################################################调用函数
def analysis_DeepSeek(prompt,user):
    completion = client_DeepSeek.chat.completions.create(model="deepseek-chat",messages=[{"role": "system", "content": prompt},{"role": "user", "content": user}],stream=True)
    reasoning_content = ""
    content = ""
    placeholder = st.empty()
    for chunk in completion:
        # if chunk.choices[0].delta.reasoning_content:
        #     reasoning_content += chunk.choices[0].delta.reasoning_content
        # else:
        content += chunk.choices[0].delta.content
        placeholder.empty()
        placeholder.markdown(content)
        # st.markdown(chunk.choices[0].delta.content)
    return content

def analysis_Kimi(prompt,user):
    completion = client_Kimi_vision.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": user},
        ],
        temperature=0.3,
        stream=True
        )
    content = ""
    placeholder = st.empty()
    for chunk in completion:
        if chunk.choices[0].delta.content:
            content += chunk.choices[0].delta.content
            placeholder.empty()
            placeholder.markdown(content)
    return content

def analysis_Ali_DS(prompt,user):
    completion = client_Ali_DS.chat.completions.create(
        model="deepseek-v3",
        messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": user},
        ],
        stream=True
        )
    content = ""
    placeholder = st.empty()
    for chunk in completion:
        content += chunk.choices[0].delta.content
        placeholder.empty()
        placeholder.markdown(content)
    return content

def analysis_ChatGPT(prompt,user):
    completion = client_ChatGPT.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": prompt},
        {"role": "user", "content": user},
        ],
        stream=True
        )
    content = ""
    placeholder = st.empty()
    for chunk in completion:
        content += chunk.choices[0].delta.content
        placeholder.empty()
        placeholder.markdown(content)
    return content

# def analysis_QianFan(prompt,user):
#     response = client_DeepSeek.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
#         temperature=0.7,
#         max_tokens=1024,
#         top_p=1,
#         frequency_penalty=0,
#         presence_penalty=0,
#     )

def AI_shibie(filepath):
    if "Kimi" == 'Kimi':
        ShowState = st.empty()
        ShowState.markdown('### 正在识别...')
        file_object = client_Kimi_vision.files.create(file=Path(file_path), purpose="file-extract")
        file_content = client_Kimi_vision.files.content(file_id=file_object.id).text
        ShowState.empty()
        ShowState.write(file_content)
        return file_content
    
###########################################################################################3
OutPut_Template1 = """生成一个结构化的报告。报告的输出需要遵循以下格式：
1. **学员基本信息**：
   - 姓名：
   - 年龄：
   - 学科：
   
2. **学习情况**：
   - 最近考试成绩：
   - 近期学习进展：

3. **优势与弱点**：
   - 优势：
   - 弱点：

4. **改进建议**：
   - 提供针对学员弱点的改进建议。
"""
OutPut_Template2 = '''按照以下格式进行输出：

1. **学员基本信息**：
   - 姓名：
   - 年龄：
   - 学科：
   - 学习目标：

2. **学习情况**：
   - 最近考试成绩：
   - 学习进展：
   - 近期任务完成情况：

3. **优势与弱点**：
   - 学科优势：
   - 学科弱点：
   - 性格或学习习惯上的优势：
   - 性格或学习习惯上的弱点：

4. **改进建议**：
   - 针对学科优势：请提供进一步提高优势的建议。
   - 针对学科弱点：请提供改善弱点的具体学习建议。
   - 针对性格和学习习惯的建议：请提供学员在学习过程中可能需要注意的改进点。
'''
###########################################################################################3

## Streamlit 页面标题
st.title("AI助学-赛学科技集成化系统")

style = """
    /* 全局按钮样式 */
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton button:hover {
        background-color: #45a049;
    }

    /* 文本区域样式 */
    .stTextArea textarea {
        font-size: 16px;
        padding: 10px;
        border-radius: 8px;
        border: 1px solid #ddd;
    }
"""

st.markdown("""
<style>
    

    /* 标题样式 */
    .stHeader {
        font-size: 24px;
        font-weight: bold;
        color: rgb(49, 51, 63);
    }

    /* 历史记录容器样式 */
    .history-card {
        background-color: #ffffff;
        border: 2x solid #e0e0e0;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        transition: box-shadow 0.3s ease;
    }
    .history-card:hover {
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }

    /* 时间样式 */
    .history-card .timestamp {
        font-size: 14px;
        color: #666;
        margin-bottom: 8px;
    }

    /* 类型样式 */
    .history-card .type {
        font-size: 16px;
        font-weight: bold;
        color: rgb(49, 51, 63);
        margin-bottom: 8px;
    }

    /* 输入输出样式 */
    .history-card .input-output {
        font-size: 14px;
        color: #333;
        margin-bottom: 8px;
    }
    .history-card .input-output strong {
        color: rgb(49, 51, 63);
    }
</style>
""", unsafe_allow_html=True)

## 侧边栏导航
menu = st.sidebar.selectbox("选择功能", ["学员信息分析", "学习计划安排", "作业批改", "试卷分析", "成长档案生成","对话历史记录"])
menu2 = st.sidebar.selectbox("大模型选择", ["DeepSeek","DeepSeek_V3_Ali", "Kimi", "ChatGPT"])

## AI分析

def AI_analysis(sys_msg,user_msg,model = menu2):
    if model == "DeepSeek":
        response = analysis_DeepSeek(sys_msg,user_msg)
        return response
    elif model == "DeepSeek_V3_Ali":
        # response = analysis_DeepSeek(sys_msg,user_msg)
        response = analysis_Ali_DS(sys_msg,user_msg)
        return response
    # elif model == "文心一言":
    #     response = analysis_QianFan(sys_msg,user_msg)
    #     return response
    elif model == "ChatGPT":
        response = analysis_ChatGPT(sys_msg,user_msg)
        return response
    elif model == "Kimi":
        response = analysis_Kimi(sys_msg,user_msg)
        return response
    

## 学员信息分析 

# st.markdown("""
#     <style>
        
#         .stButton button {
#             background-color: #F33333;
#             color: white;
#             font-size: 16px;
#             padding: 10px 24px;
#             border-radius: 8px;
#             border: none;
#         }
#         .stTextArea textarea {
#             font-size: 16px;
#             padding: 10px;
#         }
#         .stheader {
#             font-size: 10px;
#             font-weight: bold;
#             color: rgb(49, 51, 63);
#         }
#     </style>
#     """, unsafe_allow_html=True)

if menu == "学员信息分析":
    OutputTemplateMenu = st.sidebar.selectbox('选择输出模板',['自由输出','赛学专用模板示例1','赛学专用模板示例2'])
    st.header("学员信息分析")

    col1, col2, col3,col4 = st.columns(4)
    with col1:
        student_name = st.text_input("学员姓名")
    with col2:
        age = st.selectbox("年级", ["初中一年级", "初中二年级", "初中三年级", "高中一年级", "高中二年级","高中三年级"])
    with col3:
        subjects = st.selectbox("学习科目", ["语文", "数学", "英语", "物理", "化学","生物",'地理','历史','政治'])
    with col4:
        recent_scores = st.text_input("最近考试成绩")
    strengths_and_weaknesses = st.text_area("学员基本信息")
    
    if st.button("分析"):

        system_msg = f"你是一名教育机构的高中老师，请根据以下信息对学员的情况进行分析"
        
        if OutputTemplateMenu == '自由输出':
            pass
        elif OutputTemplateMenu == '赛学专用模板示例1':
            system_msg += OutPut_Template1
        elif OutputTemplateMenu == '赛学专用模板示例2':
            system_msg += OutPut_Template2

        user_msg = f"""
                根据以下学员信息生成一份详细的分析报告：
                学员姓名：{student_name}
                年级：{age}
                在本机构补习的科目：{subjects}
                最近考试成绩：{recent_scores}
                学员具体情况：{strengths_and_weaknesses}
                请给出学员的优势、薄弱环节，并根据学员的情况进行详细分析提分策略。
                """

        con_analysis = st.empty()
        con_analysis.markdown('### 正在分析...')

        feedback = AI_analysis(system_msg,user_msg)
        
        con_analysis.empty()
        
        new_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": menu,
                    "system":system_msg,
                    "input": user_msg,
                    "output": feedback
                }
        st.session_state.conversation_history.insert(0,new_entry)
        
        save_history(st.session_state.conversation_history)  # 保存到本地文件

## 学科计划安排 


elif menu == "学习计划安排":
    
    st.header("学习计划安排")

    col21, col22, col23,col24 = st.columns(4)
    with col21:
        currentscore = st.text_input("当前分数")
    with col22:
        targetscore = st.text_input("目标分数")
    with col23:
        age = st.selectbox("年级", ["初中一年级", "初中二年级", "初中三年级", "高中一年级", "高中二年级","高中三年级"])
    with col24:
        menu_T = st.selectbox('计划时间跨度',['天','周','月','半年'])

    col25,col26,col27 = st.columns(3)
    with col25:
        everyweekorNot = st.selectbox("上课频次", ["每周", "隔周"])
    with col26:
        frequency = st.number_input('次数', min_value=0, max_value=20, value=1, step=1)
    with col27:
        duriation = st.number_input("每次时长",max_value=10)

    student_goal = st.text_area("请输入学员的具体信息和目标：")
    weaknesses_info = st.text_area("学员薄弱板块")
    
    

    
    
    # start_time = st.time_input('请选择开始时间', value="now", key=None, help=None, on_change=None, args=None, kwargs=None,disabled=False, label_visibility="visible", step=0:15:00)
    # today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # if user_date:
        # DeltaDay = (today - user_date).days
        # st.write(f"今天与选择的日期之间的天数差是：{delta}天")
    
    if menu_T=='天':
        # start_time = st.time_input("请选择开始时间",value="now",step=30*60)
        # end_time = st.time_input('请选择离校时间', value="now", key=None, help=None, on_change=None, args=None, kwargs=None,disabled=False, label_visibility="visible", step=30*60)
    
        zhouqi = f'请生成一天的学习计划安排，按照小时划分'
    elif menu_T == '周':
        zhouqi = '请生成一周的学习计划安排，按照每天划分'
    elif menu_T == '月':
        zhouqi = '请生成一个月的学习计划安排，按照每周划分'
    elif menu_T == '半年':
        zhouqi = '请生成半年的学习计划安排，按照每月划分'

    

    if st.button("生成计划"):
        mes_temp = ''
        if currentscore:
            mes_temp = mes_temp + f'当前分数：{currentscore}\n'
        if targetscore:
            mes_temp = mes_temp + f'目标分数：{targetscore}\n'
        if  age :
            mes_temp = mes_temp + f'年级：{age}\n'
            
        if  frequency and duriation:
            mes_temp = mes_temp + f'上课频次：{everyweekorNot}{frequency}次，每次时长/小时：{duriation}小时\n'
        if weaknesses_info:
            mes_temp = mes_temp + f'学生的薄弱板块：{weaknesses_info}\n'

        system_msg = f"根据学员的当前进度和学习目标，生成一个合理的学科计划。"

        user_msg = f"""
                计划时间跨度:{zhouqi}
                具体信息和目标：{student_goal}
                """
        user_msg = mes_temp + user_msg
        con_analysis = st.empty()
        con_analysis.markdown('### 正在分析...')

        feedback1 = AI_analysis(system_msg,user_msg)
        con_analysis.empty()
        print(feedback1)
        st.success('计划制定完成，正在生成PDF...')
        pdf_path = r"generated_pdfs/output.pdf"
        save_pdf(feedback1,pdf_path)
        st.success('PDF生成完成')

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()
            
        st.download_button(
            label="下载 PDF 文件",
            data=pdf_bytes,
            file_name="study_plan.pdf",
            mime="application/pdf"
        )

        new_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": menu,
                    "system":system_msg,
                    "input": user_msg,
                    "output": feedback1
                }
        st.session_state.conversation_history.insert(0,new_entry)
        save_history(st.session_state.conversation_history)  # 保存到本地文件




elif menu == "试卷分析":
    st.header("试卷分析")
    HomeworkSubjects = st.selectbox("试卷科目", ["","语文", "数学", "英语", "物理", "化学","生物",'地理','历史','政治'])
    homework = st.text_area("请输入试卷内容：")
    
    uploaded_file = st.file_uploader("上传试卷图片", type=["jpg", "jpeg", "png","pdf"])

    # save_path = os.path.join(SAVE_DIR, uploaded_file.name)
    # with open(save_path, "wb") as f:
    #     f.write(uploaded_file.getbuffer())
    # st.success(f"文件已成功保存到：{save_path}")

    PhotoMsg = ""
    if uploaded_file is not None:
        upload_folder = 'upload'
        file_type = uploaded_file.type
    


        file_path = 'temp'+'.'+file_type.split('/')[-1]

        if not os.path.exists(file_path):
            os.system(r"touch {}".format(file_path))#调用系统命令行来创建文件
        if file_type == 'image/jpeg' or file_type == 'image/png' or file_type == 'image/jpg':
            st.image(uploaded_file, caption="上传的试卷图片", use_column_width=True)
            # 保存图片文件

        
        
        # with open("temp_image.jpg", "wb") as f:
        #     f.write(uploaded_file.getbuffer())

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    if st.button("识别并批改"):
        user_msg = f"请批改以下{HomeworkSubjects}试卷，并给出评分和反馈：{homework}。"
        if uploaded_file is not None:
            file_content = AI_shibie(file_path)
            user_msg += f"试卷照片识别结果为：{file_content}"
        ShowState2 = st.empty()
        system_msg = "请批改下面的试卷，并给出试卷的回答分析及给学员的改正建议"      
        ShowState2.markdown("### 正在批改，请稍等...")
        feedback = AI_analysis(system_msg,user_msg)
        ShowState2.empty()
        new_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": menu,
                    "system":system_msg,
                    "input": user_msg,
                    "output": feedback
                }
        st.session_state.conversation_history.insert(0,new_entry)
        save_history(st.session_state.conversation_history)  # 保存到本地文件

elif menu == "成长档案生成":
    st.header("成长档案生成")
    learning_record = st.text_area("请输入学员的学习记录：")
    
    if st.button("生成档案"):
        system_msg = f"请根据以下学习记录，生成学员的成长档案。"
        
        user_msg = f"""
                学习记录：{learning_record}
                """
        con_analysis = st.empty()
        con_analysis.markdown('### 正在生成...')

        feedback = AI_analysis(system_msg,user_msg)
        
        con_analysis.empty()
        
        new_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": menu,
                    "system":system_msg,
                    "input": user_msg,
                    "output": feedback
                }
        st.session_state.conversation_history.insert(0,new_entry)
        save_history(st.session_state.conversation_history)  # 保存到本地文件

elif menu == "作业批改":
    st.header("作业批改")
    HomeworkSubjects = st.selectbox("作业科目", ["","语文", "数学", "英语", "物理", "化学","生物",'地理','历史','政治'])
    homework = st.text_area("请输入作业内容：")
    
    uploaded_file = st.file_uploader("上传作业图片", type=["jpg", "jpeg", "png","pdf"])
    PhotoMsg = ""

    if uploaded_file is not None:
        upload_folder = 'upload'
        file_type = uploaded_file.type
    


        file_path = 'temp'+'.'+file_type.split('/')[-1]

        if not os.path.exists(file_path):
            os.system(r"touch {}".format(file_path))#调用系统命令行来创建文件
        if file_type == 'image/jpeg' or file_type == 'image/png' or file_type == 'image/jpg':
            st.image(uploaded_file, caption="上传的试卷图片", use_column_width=True)
            # 保存图片文件

        
        
        # with open("temp_image.jpg", "wb") as f:
        #     f.write(uploaded_file.getbuffer())

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
    if st.button("识别并批改"):
        user_msg = f"请批改以下{HomeworkSubjects}作业，并给出评分和反馈：{homework}。"
        if uploaded_file is not None:
            file_content = AI_shibie(file_path)
            user_msg += f"作业照片识别结果为：{file_content}"
        ShowState2 = st.empty()
        system_msg = "请批改下面的作业，并给出作业的回答分析及修改建议"      
        ShowState2.markdown("### 正在批改，请稍等...")
        feedback = AI_analysis(system_msg,user_msg)
        ShowState2.empty()
        new_entry = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": menu,
                    "system":system_msg,
                    "input": user_msg,
                    "output": feedback
                }
        st.session_state.conversation_history.insert(0,new_entry)
        
        save_history(st.session_state.conversation_history)  # 保存到本地文件

elif menu == "对话历史记录":
    st.header("对话历史记录")
    if st.session_state.conversation_history:
        for entry in st.session_state.conversation_history:
            st.markdown(f"""
            <div class="history-card">
                <div class="timestamp">📅 {entry['timestamp']}</div>
                <div class="type">📌 {entry['type']}</div>
                <div class="input-output">
                    <p><strong> 输入：</strong>{entry['input']}</p>
                    <p><strong> 输出：</strong>{entry['output']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.write("暂无对话记录。")
# uploaded_file = st.file_uploader("上传作业图片", type=["jpg", "jpeg", "png"])


    

# if uploaded_file is not None:
#     # 显示上传的图片
#     st.image(uploaded_file, caption="上传的作业图片", use_column_width=True)
#     with open("temp_image.jpg", "wb") as f:
#         f.write(uploaded_file.getbuffer())
#     file_object = client_Kimi_vision.files.create(file=Path("temp_image.jpg"), purpose="file-extract")

#     # 调用 Google Cloud Vision API 提取文本
#     def extract_text_from_image(image_path):
#         client = vision.ImageAnnotatorClient()
#         with open(image_path, "rb") as image_file:
#             content = image_file.read()
#         image = vision.Image(content=content)
#         response = client.text_detection(image=image)
#         texts = response.text_annotations
#         if texts:
#             return texts[0].description  # 返回提取的文本
#         else:
#             return None

#     # 保存上传的图片到临时文件
#     with open("temp_image.jpg", "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     # 提取文本
#     extracted_text = extract_text_from_image("temp_image.jpg")
#     if extracted_text:
#         st.write("提取的作业内容：")
#         st.write(extracted_text)

        

#         # 作业批改
#         if st.button("批改作业"):
#             prompt = f"请批改以下作业，并给出评分和反馈：{extracted_text}"
#             response = openai.Completion.create(
#                 engine="text-davinci-003",  # 或使用 deepseek 的模型
#                 prompt=prompt,
#                 max_tokens=500
#             )
#             st.write("批改结果：")
#             st.write(response.choices[0].text)
#     else:
#         st.write("未能从图片中提取文本，请上传清晰的作业图片。")