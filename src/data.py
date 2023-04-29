import requests
from question_model import Question
class QuizData:
    def __init__(self, parameters):
        self.parameters = parameters
        self.question_bank = []
        self.get_questions()

    def get_questions(self):
        response = requests.get(url="https://opentdb.com/api.php", params=self.parameters)
        response.raise_for_status()
        question_data = response.json()["results"]

        for question in question_data:
            question_text = question["question"]
            question_answer = question["correct_answer"]
            new_question = Question(question_text, question_answer)
            self.question_bank.append(new_question)