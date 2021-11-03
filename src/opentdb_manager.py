import requests
import time
import html

class otdb:

    def __init__(self):
        self.time_token = time.time()
        self.session_token = self.get_session_token()
        self.categories = self.get_categories()

    def get_session_token(self):
        url = "https://opentdb.com/api_token.php?command=request"
        reply = requests.get(url)
        reply = reply.json()

        if reply["response_code"] == 0:
            return reply["token"]
        else:
            return None

    def reset_session_token(self):
        url = f"https://opentdb.com/api_token.php?command=reset&token={self.session_token}"
        reply = requests.post(url)
        reply = reply.json()

        if reply["response_code"] == (0 or 4):
            return reply["token"]
        else:
            return None

    def get_categories(self):
        url = "https://opentdb.com/api_category.php"
        reply = requests.get(url)
        reply = reply.json()

        categories = {}

        for x in reply["trivia_categories"]:
            categories[x["name"]] = x["id"]

        return categories

    def make_utf_8(self,quiz_list):
        new_quiz_list = []

        for quiz in quiz_list:
            dict_quiz = quiz.copy()
            dict_quiz["question"] = html.unescape(quiz.get("question"))
            dict_quiz["correct_answer"] = html.unescape(quiz.get("correct_answer"))
            new_incorrect_answers =[]
            for x in quiz["incorrect_answers"]:
                new_incorrect_answers.append(html.unescape(x))
            dict_quiz["incorrect_answers"] = new_incorrect_answers
            new_quiz_list.append(dict_quiz)


        return new_quiz_list


    def get_quiz(self, amount=None, category=None, difficulty=None, type=None):
        if time.time() - self.time_token > 20000:
            self.session_token = self.get_session_token()

        if amount is None:
            amount = "1"
        elif isinstance(amount, int) and 0 < amount <= 50:
            amount = str(amount)
        else:
            raise Exception(f"{str(amount)} is not a valid value for amount")

        if category is None:
            pass
        elif isinstance(category, int) and category in self.categories.values():
            category = str(category)
        else:
            raise Exception(f"{str(category)} is not a valid value for category")

        if difficulty is None:
            pass
        elif isinstance(difficulty, str) and difficulty in {"easy", "medium", "hard"}:
            pass
        else:
            raise Exception(f"{difficulty} is not a valid value for difficulty")

        if type is None:
            pass
        elif isinstance(type, str) and type in  {"multiple", "boolean"}:
            pass
        else:
            raise Exception(f"{type} is not a valid value for type")

        url = f"https://opentdb.com/api.php?amount={amount}"

        if category is not None:
            url += f"&category={category}"

        if difficulty is not None:
            url += f"&difficulty={difficulty}"

        if type is not None:
            url += f"&type={type}"

        url += f"&token={self.session_token}"

        reply = requests.post(url)
        reply = reply.json()



        if reply["response_code"] == 0:
            quiz = reply["results"]
        elif reply["response_code"] == 1:
            self.session_token = self.get_session_token()
            raise Exception("requested more questions than available")
        elif reply["response_code"] == 2:
            return None
        elif reply["response_code"] == 3:
            self.session_token = self.get_session_token()
            raise Exception("session token unknown")
        elif reply["response_code"] == 4:
            self.session_token = self.reset_session_token()
            raise Exception("requested more questions than available or already received already all questions")

        quiz = self.make_utf_8(quiz)

        return quiz




