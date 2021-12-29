from typing import Optional, TypedDict

import asyncio
import aiohttp
import time
import html

o_str = Optional[str]
o_int = Optional[int]

Quiz_Type = TypedDict('Quiz_Type',
                      {'category': str, 'correct_answer': str, 'difficulty': str, 'incorrect_answers': list[str],
                       'question': str, 'type': str})

Categories_Type = TypedDict('Categories_Type', {'id': int, 'name': str})

Quiz_Type_List = list[Quiz_Type]

API_RESPONSE = TypedDict('API_RESPONSE',
                         {'response_code': int, 'response_message': str, 'token': str, 'results': Quiz_Type_List,
                          'trivia_categories': list[Categories_Type]}, total=False)


class OTBD_Wrapper:

    async def init(self) -> None:
        """
        This function exist because, __init__ constructor is not async.
        :return: None
        """
        self.time_token = time.time()
        self.session_token: str = await self.get_session_token()
        self.categories: dict[str, int] = await self.get_categories()

    async def make_get_request(self, url: str) -> API_RESPONSE:
        """
        Makes async get request to opentdb.com and returns the api response.
        :param url: a url (string)
        :return: API_RESPONSE
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    r: API_RESPONSE = await response.json()
                    return r
                else:
                    raise Exception(f"HTML status_code:{response.status}")

    async def get_session_token(self) -> str:
        """
        gets a token from opentdb.com so you don't receive the same quiz over and over again.

        :return: api token (string)
        """
        url = "https://opentdb.com/api_token.php?command=request"

        response = await self.make_get_request(url)
        if response["response_code"] == 0:
            return response["token"]
        else:
            raise Exception(f"response_code:{response['response_code']}")

    async def reset_session_token(self) -> str:
        """
        resets the api token so you can receive 'new' (old) quizzes.

        :return: api token (string)
        """
        url = f"https://opentdb.com/api_token.php?command=reset&token={self.session_token}"

        response = await self.make_get_request(url)

        if response["response_code"] in (0, 4):
            return response["token"]
        else:
            raise Exception(f"response_code:{response['response_code']}")

    async def get_categories(self) -> dict[str, int]:
        """
        gets all all list of alls categories

        :return: a dict with all categories and their number
        """
        url = "https://opentdb.com/api_category.php"

        response: API_RESPONSE = await self.make_get_request(url)

        categories: dict[str, int] = {}

        for x in response["trivia_categories"]:
            categories[x["name"]] = x["id"]

        return categories

    def make_utf_8(self, quiz_list: Quiz_Type_List) -> Quiz_Type_List:
        """
        unescapes html4

        :param quiz_list: a list of quizzes
        :return: a list of quizzes but unescaped
        """

        new_quiz_list: Quiz_Type_List = []

        for quiz in quiz_list:
            dict_quiz = quiz.copy()
            dict_quiz["question"] = html.unescape(quiz["question"])
            dict_quiz["correct_answer"] = html.unescape(quiz["correct_answer"])
            new_incorrect_answers = []
            for x in quiz["incorrect_answers"]:
                new_incorrect_answers.append(html.unescape(x))
            dict_quiz["incorrect_answers"] = new_incorrect_answers
            new_quiz_list.append(dict_quiz)

        return new_quiz_list

    async def get_quiz(self, amount: o_int = None, category: o_int = None, difficulty: o_str = None,
                       type_quiz: o_str = None) -> Quiz_Type_List:
        """

        :param amount: 0<int<=50
        :param category: int (a list of possible numbers in self.categories)
        :param difficulty: string ("easy" or "medium" or "hard")
        :param type_quiz: string ("multiple" or "boolean")
        :return: Quiz_Type_List
        """

        """check the input"""

        if need_new_token := (time.time() - self.time_token > 20000):
            get_new_token = asyncio.create_task(self.get_session_token())

        if amount is None:
            str_amount = "1"
        elif isinstance(amount, int) and 0 < amount <= 50:
            str_amount = str(amount)
        else:
            raise ValueError(f"{str(amount)} is not a valid value for amount")

        if category is None:
            pass
        elif isinstance(category, int) and category in self.categories.values():
            str_category = str(category)
        else:
            raise ValueError(f"{str(category)} is not a valid value for category")

        if difficulty is None:
            pass
        elif isinstance(difficulty, str) and difficulty in {"easy", "medium", "hard"}:
            pass
        else:
            raise ValueError(f"{difficulty} is not a valid value for difficulty")

        if type_quiz is None:
            pass
        elif isinstance(type_quiz, str) and type_quiz in {"multiple", "boolean"}:
            pass
        else:
            raise ValueError(f"{type_quiz} is not a valid value for type")

        """Creating the url"""

        url = f"https://opentdb.com/api.php?amount={str_amount}"

        if category is not None:
            url += f"&category={str_category}"

        if difficulty is not None:
            url += f"&difficulty={difficulty}"

        if type_quiz is not None:
            url += f"&type={type_quiz}"

        if need_new_token:
            self.session_token = await get_new_token

        url += f"&token={self.session_token}"

        reply = await self.make_get_request(url)

        if reply["response_code"] == 0:
            quiz: Quiz_Type_List = reply["results"]
        elif reply["response_code"] == 1:
            self.session_token = await self.get_session_token()
            raise Exception("requested more questions than available")  # only work if using no token
        elif reply["response_code"] == 2:
            raise Exception(f"Invalid Parameter Contains an invalid parameter. url:{url}")
        elif reply["response_code"] == 3:
            self.session_token = await self.get_session_token()
            raise Exception("session token unknown")
        elif reply["response_code"] == 4:
            self.session_token = await self.reset_session_token()
            raise Exception("requested more questions than available or already received already all questions")

        quiz = self.make_utf_8(quiz)

        return quiz


async def otdb() -> OTBD_Wrapper:
    """
    Returns an instance of OTBD_Wrapper and returns it
    :return: OTBD_Wrapper
    """
    wrapper = OTBD_Wrapper()
    await wrapper.init()
    return wrapper
