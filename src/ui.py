import tkinter as tk
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"

CATEGORIES = [
    "Any category",
    "Science & Nature",
    "Science: Computers",
    "Science: Mathematics",
    "Mythology",
    "Geography",
    "History",
    "Politics",
    "Animals",
    "Vehicles"
]

CATEGORY_IDS = [
    0,
    17,
    18,
    19,
    20,
    22,
    23,
    24,
    27,
    28
]

DIFFICULTY_LEVELS = [
    "Any difficulty",
    "Easy",
    "Medium",
    "Hard"
]

NO_QS = [
    '5',
    '10',
    '15',
    '20',
    '25'
]


class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs) # essentially you inherit from the class directly. this can be done by super but i need to test it out
        self.quiz = {}
        self.title(string="Quizzler")
        self.config(bg=THEME_COLOR)
        self.container = tk.Frame(self, padx=20, pady=20, bg=THEME_COLOR) # the window instance. this is needed to store and display the frames
        self.container.grid(row=0, column=0)
        self.frames = {
            "settings": Settings(parent=self.container, controller=self), #the controller argument lets you retreive any information you need from the object that is passed in as the controller
        }
        self.frames["settings"].grid(row=0, column=0)
        self.show_frame("settings")

    def show_frame(self, ui_area):
        frame = self.frames[ui_area]
        frame.tkraise()

class Settings(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parameters = {"type": "boolean", "amount": 5, }

        self.controller = controller

        self.difficulty_label = tk.Label(self, text="Difficulty:")
        self.difficulty_label.grid(column=0, row=0)
        self.selected_difficulty = tk.StringVar()
        self.selected_difficulty.set(DIFFICULTY_LEVELS[0])
        self.difficulty_select = tk.OptionMenu(self, self.selected_difficulty, *DIFFICULTY_LEVELS)
        self.difficulty_select.grid(column=1, row=0)

        self.category_label = tk.Label(self, text="Category:")
        self.category_label.grid(column=0, row=1)
        self.selected_category = tk.StringVar()
        self.selected_category.set(CATEGORIES[0])
        self.category_select = tk.OptionMenu(self, self.selected_category, *CATEGORIES)
        self.category_select.grid(column=1, row=1)

        self.no_qs_label = tk.Label(self, text="Number of Questions:")
        self.no_qs_label.grid(column=0, row=2)
        self.selected_no_qs = tk.StringVar()
        self.selected_no_qs.set(NO_QS[0])
        self.no_qs = tk.OptionMenu(self, self.selected_no_qs, *NO_QS)
        self.no_qs.grid(column=1, row=2)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_data)
        self.submit_button.grid(column=0, row=3, columnspan=2)

    def submit_data(self):
        controller = self.controller
        category = self.selected_category.get()
        difficulty = self.selected_difficulty.get()
        no_qs = int(self.selected_no_qs.get())

        if category != "Any category":
            selection = CATEGORY_IDS[CATEGORIES.index(category)]
            self.parameters["category"] = selection

        if difficulty != "Any difficulty":
            self.parameters["difficulty"] = difficulty

        self.parameters["amount"] = no_qs
        controller.quiz = QuizBrain(self.parameters)
        controller.frames["quizui"] = QuizUI(parent=controller.container, controller=controller)
        controller.show_frame("quizui")
        self.destroy()





class QuizUI(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg=THEME_COLOR)
        self.controller = controller

        self.quiz_canvas = tk.Canvas(width=300, height=250, bg="white")
        self.question_text = self.quiz_canvas.create_text(150,
                                                          125,
                                                          text="PLACEHOLDER",
                                                          font=("Arial", 20, "italic"),
                                                          width=280)
        self.quiz_canvas.grid(row=1, column=0, columnspan=2, pady=50)

        self.score_tally = tk.Label(text="Score: 0", highlightthickness=0, bg=THEME_COLOR, fg="white")
        self.score_tally.grid(row=0, column=1)

        self.chk_img = tk.PhotoImage(file="./images/true.png")
        self.fls_img = tk.PhotoImage(file="./images/false.png")
        self.chk_btn = tk.Button(image=self.chk_img, highlightthickness=0, command=self.check_answer_true)
        self.chk_btn.grid(column=0, row=2, sticky="w", padx=40, pady=20)
        self.fls_btn = tk.Button(image=self.fls_img, highlightthickness=0, command=self.check_answer_false)
        self.fls_btn.grid(column=1, row=2, sticky="w")

        self.get_next_question()

    def get_next_question(self):
        self.quiz_canvas.config(bg="white")
        if self.controller.quiz.still_has_questions():
            self.chk_btn.config(state="normal")
            self.fls_btn.config(state="normal")
            self.score_tally.config(text=f"Score: {self.controller.quiz.score}")
            next_question = self.controller.quiz.next_question()
            self.quiz_canvas.itemconfig(self.question_text, text=next_question)
        else:
            self.quiz_canvas.itemconfig(self.question_text, text="You have completed the quiz")
            self.chk_btn.config(state="disabled")
            self.fls_btn.config(state="disabled")

    def check_answer_true(self):
        self.chk_btn.config(state="disabled")
        self.fls_btn.config(state="disabled")
        self.give_feedback(self.controller.quiz.check_answer('True'))

    def check_answer_false(self):
        self.chk_btn.config(state="disabled")
        self.fls_btn.config(state="disabled")
        self.give_feedback(self.controller.quiz.check_answer('False'))

    def give_feedback(self, answer):
        if answer:
            self.quiz_canvas.config(bg="green")
        else:
            self.quiz_canvas.config(bg="red")
        self.after(1000, self.get_next_question)

app = App()
app.mainloop()
