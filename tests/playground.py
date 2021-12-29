import sys
import signal

import asyncio
import pprint

from otdb import otdb


def cleanup(*args):
    print("The program is stopping")
    sys.exit(0)


def main():
    loop = asyncio.get_event_loop()

    print("init")
    quiz = loop.run_until_complete(otdb())

    print("categories")
    pprint.pprint(quiz.categories)

    print("get quizzes")

    reply = loop.run_until_complete(quiz.get_quiz(amount=7, category=18, difficulty="hard", type_quiz="multiple"))
    pprint.pprint(reply)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, cleanup)
    try:
        main()
    except KeyboardInterrupt:
        cleanup()
