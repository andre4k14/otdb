### A crappy wrapper for the opentriviadatabase
![Tests](https://github.com/andre4k14/otdb/actions/workflows/tests.yml/badge.svg)


Don't use it.

To install it simply copy the command below.

You need python 3.9 or higher.

```bash
pip3 install "git+https://github.com/andre4k14/otdb.git"
```

## How to use it.

### Parameter for .get_quiz()

|parameter|poss. values|description| 
| :---    | :----:     |:----:     |
| amount    | 1-50          | Optional default = 1 |
| category   | numbers from self.categories| Optional default = random values |
| difficulty| "easy" or "medium" or "hard"         |Optional default = random values|
| type_quiz  | "multiple" or "boolean"          |Optional default = random values|

### Return from .get_quiz() -> Quiz_Type_List

```python
Quiz_Type = TypedDict('Quiz_Type',
                      {'category': str, 'correct_answer': str, 'difficulty': str, 'incorrect_answers': list[str],
                       'question': str, 'type': str})

Quiz_Type_List = list[Quiz_Type]
```

### example

```python
import asyncio
import pprint

from otdb import otdb

loop = asyncio.get_event_loop()
quiz = loop.run_until_complete(otdb())

reply = loop.run_until_complete(quiz.get_quiz(amount=7, category=18, difficulty="hard", type_quiz="multiple"))
pprint.pprint(reply)

""" output =>
        [{'category': 'Science: Computers',
  'correct_answer': '50',
  'difficulty': 'hard',
  'incorrect_answers': ['59', '60', '25'],
  'question': 'How many Hz does the video standard PAL support?',
  'type': 'multiple'},
 {'category': 'Science: Computers',
  'correct_answer': 'Stack',
  'difficulty': 'hard',
  'incorrect_answers': ['Queue', 'Heap', 'Tree'],
  'question': 'Which data structure does FILO apply to?',
  'type': 'multiple'},
 {'category': 'Science: Computers',
  'correct_answer': 'IRC',
  'difficulty': 'hard',
  'incorrect_answers': ['HTTP', 'HTTPS', 'FTP'],
  'question': 'What internet protocol was documented in RFC 1459?',
  'type': 'multiple'},
 {'category': 'Science: Computers',
  'correct_answer': 'Kibibyte',
  'difficulty': 'hard',
  'incorrect_answers': ['Kylobyte', 'Kilobyte', 'Kelobyte'],
  'question': 'What does the International System of Quantities refer 1024 '
              'bytes as?',
  'type': 'multiple'},
 {'category': 'Science: Computers',
  'correct_answer': "A' + B'",
  'difficulty': 'hard',
  'incorrect_answers': ["A'B + B'A", "A'B'", "AB' + AB"],
  'question': "According to DeMorgan's Theorem, the Boolean expression (AB)' "
              'is equivalent to:',
  'type': 'multiple'},
 {'category': 'Science: Computers',
  'correct_answer': 'IMKO-1',
  'difficulty': 'hard',
  'incorrect_answers': ['Pravetz 82', 'Pravetz 8D', 'IZOT 1030'],
  'question': 'What was the name of the first Bulgarian personal computer?',
  'type': 'multiple'},
 {'category': 'Science: Computers',
  'correct_answer': 'Secret sharing scheme',
  'difficulty': 'hard',
  'incorrect_answers': ['Hashing algorithm',
                        'Asymmetric encryption',
                        'Stream cipher'],
  'question': 'Which kind of algorithm is Ron Rivest not famous for creating?',
  'type': 'multiple'}]


"""

reply = loop.run_until_complete(quiz.get_quiz())
pprint.pprint(reply)

"""output =>
[{'category': 'Entertainment: Video Games',
  'correct_answer': '2012',
  'difficulty': 'easy',
  'incorrect_answers': ['2011', '2008', '2013'],
  'question': 'What year was the game Dishonored released?',
  'type': 'multiple'}]
"""

```
