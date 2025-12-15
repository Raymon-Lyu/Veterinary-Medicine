import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
from docx import Document
import re
import random
import os

class Question:
    def __init__(self, q_id, text, options, answers):
        self.id = q_id
        self.text = text      # 题目文本
        self.options = options # 选项字典
        self.answers = answers # 正确答案列表

class QuizParser:
    def __init__(self, filepath):
        self.filepath = filepath

    def parse(self):
        if not os.path.exists(self.filepath):
            return None
        
        doc = Document(self.filepath)
        questions = []
        
        current_q_text = ""
        current_options = {}
        current_answers = []
        current_id = None
        
        # --- 正则表达式匹配规则 (增强版) ---
        # 1. 匹配题目开始 
        # 修改：允许数字和标点之间有空格 \s*
        q_start_pattern = re.compile(r'^\s*(\d+)\s*[\.、\)]\s*(.*)')
        
        # 2. 匹配答案挖空
        ans_pattern = re.compile(r'[（\(]\s*([A-Ea-e])\s*[）\)]')
        
        # 3. 匹配选项开始 
        # 修改：增加 [a-e] 小写支持
        opt_start_pattern = re.compile(r'(?:^|\s+)([A-Ea-e])[\.、\)\．]\s*')

        full_text_lines = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
        
        for line in full_text_lines:
            q_match = q_start_pattern.match(line)
            
            if q_match:
                # 保存上一题
                if current_id is not None and current_options:
                    questions.append(Question(current_id, current_q_text, current_options, current_answers))
                
                # 初始化新题
                current_id = q_match.group(1)
                raw_text = q_match.group(2)
                current_options = {}
                current_answers = []
                
                # 处理答案挖空
                found_answers = ans_pattern.findall(raw_text)
                if found_answers:
                    current_answers = [a.upper() for a in found_answers]
                    current_q_text = ans_pattern.sub('（   ）', raw_text)
                else:
                    current_q_text = raw_text

            elif current_id is not None:
                # 匹配选项
                matches = list(opt_start_pattern.finditer(line))
                
                if matches:
                    for i, match in enumerate(matches):
                        opt_key = match.group(1).upper() # 统一转大写
                        start_idx = match.end()
                        if i < len(matches) - 1:
                            end_idx = matches[i+1].start()
                        else:
                            end_idx = len(line)
                        opt_val = line[start_idx:end_idx].strip()
                        current_options[opt_key] = opt_val
                else:
                    # 追加题目描述
                    if not current_options: 
                        current_q_text += "\n" + line
        
        # 保存最后一题
        if current_id is not None and current_options:
            questions.append(Question(current_id, current_q_text, current_options, current_answers))
            
        return questions

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("蛋白质化学复习题答题器")
        self.root.geometry("1000x800")
        
        # 界面配色
        self.color_default = "#f0f0f0"
        self.color_selected = "#cce5ff"
        self.color_correct = "#d4edda"
        self.color_wrong = "#f8d7da"
        self.text_correct = "#155724"
        self.text_wrong = "#721c24"
        
        # 数据初始化
        self.questions = []
        self.question_queue = []
        self.current_question = None
        self.score = 0
        self.total_answered = 0
        self.current_selections = [] # 改为列表以支持顺序
        self.is_submitted = False
        self.wrong_ids = []
        
        self.setup_ui()
        
        # 程序启动后，立即调用选择文件的方法
        self.root.after(100, self.open_file_dialog)

    def setup_ui(self):
        # 顶部信息栏
        self.info_frame = tk.Frame(self.root, pady=10, bg="#e9ecef")
        self.info_frame.pack(fill="x")
        
        # 增加一个手动选择文件的按钮
        self.btn_load_file = tk.Button(self.info_frame, text="📂 选择/切换题库", command=self.open_file_dialog, font=("Arial", 10))
        self.btn_load_file.pack(side="left", padx=20)
        
        self.lbl_progress = tk.Label(self.info_frame, text="请加载题库", font=("Arial", 12), bg="#e9ecef")
        self.lbl_progress.pack(side="left", padx=20)
        
        self.lbl_score = tk.Label(self.info_frame, text="得分: 0", font=("Arial", 12, "bold"), bg="#e9ecef")
        self.lbl_score.pack(side="right", padx=20)
        
        # 题目区域
        self.q_frame = tk.Frame(self.root, padx=20, pady=20)
        self.q_frame.pack(fill="both", expand=True)
        
        self.lbl_question = tk.Label(
            self.q_frame, 
            text="👋 欢迎使用！\n\n请在弹出的窗口中选择您的 Word 题库文件 (.docx)。\n如果没有自动弹出，请点击左上角的“选择/切换题库”按钮。", 
            font=("微软雅黑", 14), 
            wraplength=900, 
            justify="center"
        )
        self.lbl_question.pack(pady=50)
        
        # 选项区域
        self.opt_frame = tk.Frame(self.root, pady=10)
        self.opt_frame.pack(fill="both")
        
        self.option_buttons = {}
        for opt in ['A', 'B', 'C', 'D', 'E']:
            btn = tk.Button(
                self.opt_frame, 
                text=f"{opt}", 
                font=("Arial", 12),
                width=90, 
                height=2,
                anchor="w",
                padx=20,
                bg=self.color_default,
                command=lambda o=opt: self.toggle_option(o)
            )
            self.option_buttons[opt] = btn
            
        # 反馈区域
        self.lbl_feedback = tk.Label(self.root, text="", font=("微软雅黑", 12, "bold"), pady=15)
        self.lbl_feedback.pack()
        
        # 底部控制区
        self.ctrl_frame = tk.Frame(self.root, pady=20)
        self.ctrl_frame.pack(fill="x")
        
        self.btn_submit = tk.Button(self.ctrl_frame, text="提交答案", command=self.submit_answer, state="disabled", font=("Arial", 12, "bold"), bg="#ffc107", fg="black")
        self.btn_submit.pack(side="top", pady=5)
        
        self.btn_next = tk.Button(self.ctrl_frame, text="下一题", command=self.next_question, state="disabled", font=("Arial", 12), bg="#007bff", fg="white")
        self.btn_next.pack(side="top", pady=5)

    def open_file_dialog(self):
        """打开文件选择弹窗"""
        file_path = filedialog.askopenfilename(
            title="请选择包含选择题的 Word 文档",
            filetypes=[("Word Documents", "*.docx")]
        )
        
        if file_path:
            self.load_data(file_path)
        else:
            # 如果用户取消了选择，且当前没有正在进行的题目，提示一下
            if not self.questions:
                self.lbl_question.config(text="⚠️ 未选择文件，无法开始。\n请点击左上角按钮重新选择。")

    def load_data(self, filepath):
        parser = QuizParser(filepath)
        qs = parser.parse()
        
        if not qs:
            messagebox.showerror("读取失败", "文档中未找到题目。\n请确认文档格式：\n1. 题目以数字开头 (如 1. 或 1、)\n2. 包含选项 (如 A. B. )")
            return

        self.questions = qs
        self.restart_game()

    def restart_game(self):
        self.question_queue = self.questions[:]
        random.shuffle(self.question_queue)
        
        self.score = 0
        self.total_answered = 0
        self.wrong_ids = []
        self.update_score_label()
        
        # 清理可能存在的结算界面
        if hasattr(self, 'result_text_area'):
            self.result_text_area.pack_forget()
            self.lbl_final_msg.pack_forget()
            self.btn_restart.pack_forget()
            self.btn_exit.pack_forget()
        
        self.q_frame.pack(fill="both", expand=True)
        self.opt_frame.pack(fill="both")
        self.ctrl_frame.pack(fill="x")
        self.btn_submit.pack(side="top", pady=5)
        self.btn_next.pack(side="top", pady=5)
            
        self.next_question()

    def next_question(self):
        if not self.question_queue:
            self.game_over()
            return
        
        self.current_question = self.question_queue.pop(0)
        self.total_answered += 1
        
        self.current_selections = [] # 重置为空列表
        self.is_submitted = False
        
        self.lbl_progress.config(text=f"进度: {self.total_answered} / {len(self.questions)} (原题号: {self.current_question.id})")
        self.lbl_question.config(text=f"{self.total_answered}. {self.current_question.text}", justify="left")
        self.lbl_feedback.config(text="", bg=self.root.cget("bg"))
        
        self.btn_next.config(state="disabled")
        self.btn_submit.config(state="normal", bg="#ffc107")
        
        # 刷新选项按钮
        for k, btn in self.option_buttons.items():
            btn.pack_forget()
            btn.config(bg=self.color_default, state="normal")
            
        if self.current_question.options:
            sorted_opts = sorted(self.current_question.options.keys())
            for key in sorted_opts:
                text = f"{key}. {self.current_question.options[key]}"
                if key in self.option_buttons:
                    self.option_buttons[key].config(text=text)
                    self.option_buttons[key].pack(pady=5)
        else:
            for key in ['A', 'B', 'C', 'D']:
                self.option_buttons[key].config(text=f"选项 {key}")
                self.option_buttons[key].pack(pady=5)

    def toggle_option(self, key):
        if self.is_submitted: return
        
        btn = self.option_buttons[key]
        if key in self.current_selections:
            # 取消选择，从列表中移除
            self.current_selections.remove(key)
            btn.config(bg=self.color_default)
        else:
            # 添加选择，追加到列表末尾 (保持顺序)
            self.current_selections.append(key)
            btn.config(bg=self.color_selected)
            
        # 实时显示选择顺序
        if self.current_selections:
            seq_str = " -> ".join(self.current_selections)
            self.lbl_feedback.config(text=f"当前已选顺序: {seq_str}", fg="blue")
        else:
            self.lbl_feedback.config(text="")

    def submit_answer(self):
        if self.is_submitted: return
        self.is_submitted = True
        
        correct_list = self.current_question.answers
        user_list = self.current_selections
        
        # 直接比较两个列表，顺序必须完全一致才算对
        is_correct = (user_list == correct_list)
        
        correct_str = " -> ".join(correct_list)
        
        if is_correct:
            self.score += 1
            self.lbl_feedback.config(text=f"回答正确！ 答案是: {correct_str}", fg=self.text_correct)
        else:
            self.wrong_ids.append(self.current_question.id)
            self.lbl_feedback.config(text=f"回答错误。 正确顺序是: {correct_str}", fg=self.text_wrong)
            
        for key, btn in self.option_buttons.items():
            btn.config(state="disabled")
            if key in correct_list:
                btn.config(bg=self.color_correct)
            elif key in user_list and key not in correct_list:
                btn.config(bg=self.color_wrong)

        self.update_score_label()
        self.btn_submit.config(state="disabled", bg="#e0e0e0")
        self.btn_next.config(state="normal")

    def update_score_label(self):
        self.lbl_score.config(text=f"得分: {self.score}")

    def game_over(self):
        self.q_frame.pack_forget()
        self.opt_frame.pack_forget()
        self.btn_submit.pack_forget()
        self.btn_next.pack_forget()
        self.lbl_feedback.config(text="")
        
        self.lbl_final_msg = tk.Label(self.root, text=f"所有题目已答完！\n最终得分: {self.score} / {len(self.questions)}", fg="blue", font=("Arial", 14, "bold"))
        self.lbl_final_msg.pack(pady=20)
        
        if self.wrong_ids:
            wrong_msg = f"您共有 {len(self.wrong_ids)} 道错题。\n以下是错题在原文档中的题号，您可以复制保存："
            lbl_wrong = tk.Label(self.root, text=wrong_msg, font=("Arial", 12))
            lbl_wrong.pack()
            
            self.result_text_area = scrolledtext.ScrolledText(self.root, width=60, height=10, font=("Arial", 12))
            self.result_text_area.pack(pady=10)
            self.result_text_area.insert(tk.END, ", ".join(self.wrong_ids))
            self.result_text_area.config(state='disabled')
        else:
            lbl_perfect = tk.Label(self.root, text="太棒了！您全对了！", font=("Arial", 14), fg="green")
            lbl_perfect.pack(pady=20)
        
        self.btn_restart = tk.Button(self.ctrl_frame, text="重新来一次", command=self.restart_game, font=("Arial", 12), bg="green", fg="white")
        self.btn_restart.pack(pady=5)
        
        self.btn_exit = tk.Button(self.ctrl_frame, text="退出", command=self.root.quit, font=("Arial", 12), bg="red", fg="white")
        self.btn_exit.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()