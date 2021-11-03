import sys
import signal

from otdb.opentdb_manager import otdb
def cleanup(*args):
    print("The program is stopping")
    sys.exit(0)


def main():
    quiz = otdb()
    print("hi ")
    reply = quiz.get_quiz(amount=10)
    print(reply)
    # reply = quiz.get_quiz(amount=1, category=18, difficulty="hard", type="multiple")
    # print(reply)
    # reply = quiz.get_quiz(amount=1, category=18, difficulty="hard", type="multiple")
    # print(reply)
    # reply = quiz.get_quiz(amount=1, category=18, difficulty="hard", type="multiple")
    # print(reply)
    # reply = quiz.get_quiz(amount=1, category=18, difficulty="hard", type="multiple")
    # print(reply)
    # reply = quiz.get_quiz(amount=1, category=18, difficulty="hard", type="multiple")
    # print(reply)
    # reply = quiz.get_quiz(amount=1, category=18, difficulty="hard", type="multiple")
    # print(reply)
    # reply = quiz.get_quiz(amount=1, category=18, difficulty="hard", type="multiple")
    # print(reply)
    # reply = quiz.get_quiz(amount=1, category=18, difficulty="hard", type="multiple")
    # print(reply)









if __name__ == '__main__':
    signal.signal(signal.SIGINT, cleanup)
    try:
        main()
    except KeyboardInterrupt:
        cleanup()
