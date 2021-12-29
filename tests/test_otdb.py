import unittest
import asyncio
from otdb import otdb


class TestOPDB(unittest.TestCase):

    def test_categories(self):
        loop = asyncio.get_event_loop()
        quiz = loop.run_until_complete(otdb())

        for category, num in quiz.categories.items():
            reply = loop.run_until_complete(quiz.get_quiz(category=num))
            self.assertEqual(reply[0]["category"], category)

        with self.assertRaises(Exception) as context:
            loop.run_until_complete(quiz.get_quiz(category=51))
        self.assertTrue("51 is not a valid value for category" in str(context.exception))

    def test_amount(self):
        loop = asyncio.get_event_loop()
        quiz = loop.run_until_complete(otdb())

        async def get_stuff(numbers):
            tasks = (quiz.get_quiz(amount=num) for num in numbers)
            res = await asyncio.gather(*tasks)

            return res

        a = [x for x in range(1, 50)]

        data = loop.run_until_complete(get_stuff(a))

        b = [len(x) for x in data]
        b.sort()

        self.assertEqual(b, a)

        with self.assertRaises(Exception) as context:
            loop.run_until_complete(quiz.get_quiz(amount=0))
        self.assertTrue("0 is not a valid value for amount" in str(context.exception))

        with self.assertRaises(Exception) as context:
            loop.run_until_complete(quiz.get_quiz(amount=51))
        self.assertTrue("51 is not a valid value for amount" in str(context.exception))

    def test_difficulty(self):
        loop = asyncio.get_event_loop()
        quiz = loop.run_until_complete(otdb())

        self.assertEqual(loop.run_until_complete(quiz.get_quiz(difficulty="hard"))[0]["difficulty"], "hard")
        self.assertEqual(loop.run_until_complete(quiz.get_quiz(difficulty="medium"))[0]["difficulty"], "medium")
        self.assertEqual(loop.run_until_complete(quiz.get_quiz(difficulty="easy"))[0]["difficulty"], "easy")

        with self.assertRaises(Exception) as context:
            loop.run_until_complete(quiz.get_quiz(difficulty=51))
        self.assertTrue("51 is not a valid value for difficulty" in str(context.exception))

        with self.assertRaises(Exception) as context:
            loop.run_until_complete(quiz.get_quiz(difficulty="pizza"))
        self.assertTrue("pizza is not a valid value for difficulty" in str(context.exception))

    def test_type(self):
        loop = asyncio.get_event_loop()
        quiz = loop.run_until_complete(otdb())

        self.assertEqual(loop.run_until_complete(quiz.get_quiz(type_quiz="boolean"))[0]["type"], "boolean")
        self.assertEqual(loop.run_until_complete(quiz.get_quiz(type_quiz="multiple"))[0]["type"], "multiple")

        with self.assertRaises(Exception) as context:
            loop.run_until_complete(quiz.get_quiz(type_quiz=51))
        self.assertTrue("51 is not a valid value for type" in str(context.exception))

        with self.assertRaises(Exception) as context:
            loop.run_until_complete(quiz.get_quiz(type_quiz="pizza"))
        self.assertTrue("pizza is not a valid value for type" in str(context.exception))

    def test_errors(self):
        loop = asyncio.get_event_loop()
        quiz = loop.run_until_complete(otdb())

        with self.assertRaises(Exception) as context:
            loop.run_until_complete(quiz.get_quiz(amount=50, category=18, difficulty="hard", type_quiz="boolean"))
        self.assertTrue("requested more questions than available" in str(context.exception))

        with self.assertRaises(Exception) as context:
            quiz.session_token = "hgdfjghfhjvjr6t"
            loop.run_until_complete(quiz.get_quiz())
        self.assertTrue("session token unknown" in str(context.exception))

        with self.assertRaises(Exception) as context:
            loop.run_until_complete(quiz.get_quiz(amount=25, category=18, difficulty="hard", type_quiz="boolean"))
            loop.run_until_complete(quiz.get_quiz(amount=25, category=18, difficulty="hard", type_quiz="boolean"))
            loop.run_until_complete(quiz.get_quiz(amount=25, category=18, difficulty="hard", type_quiz="boolean"))
        self.assertTrue("requested more questions than available or already received already all questions" in str(
            context.exception))

        quiz.time_token -= 20000
        loop.run_until_complete(quiz.get_quiz())


if __name__ == '__main__':
    unittest.main()
