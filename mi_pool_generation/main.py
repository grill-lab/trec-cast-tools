from pathlib import Path
import pandas as pd
import json
import random
from string_grouper import group_similar_strings

valid_question_directory = Path("files/valid_questions")
invalid_question_directory = Path("files/invalid_questions")
columns = [
    "Answer.question1",
    "Answer.question2",
    "Answer.question3",
    "Answer.question4",
    "Answer.question5",
    "Answer.question6"
]

# collect valid questions
valid_questions = []
for question_file in valid_question_directory.iterdir():
    batch = pd.read_csv(question_file)
    for column in columns:
        valid_questions.extend(batch[column].to_list())

# Remove null values
valid_questions_df = pd.DataFrame(valid_questions, columns=["Questions"])
valid_questions_df.dropna(inplace=True)

# Deduplicate
valid_questions_df[['group rep ID', 'group rep']] = \
    group_similar_strings(
        valid_questions_df['Questions'],
        min_similarity=0.8)

# ------------------------ #
# collect invalid questions
invalid_questions = []
for question_file in invalid_question_directory.iterdir():
    batch = pd.read_csv(question_file)
    for column in columns:
        invalid_questions.extend(batch[column].to_list())

# Remove null values
invalid_questions_df = pd.DataFrame(invalid_questions, columns=["Questions"])
invalid_questions_df.dropna(inplace=True)

# Deduplicate
invalid_questions_df[['group rep ID', 'group rep']] = \
    group_similar_strings(
        invalid_questions_df['Questions'],
        min_similarity=0.8)

# valid_questions_df.to_csv("test.csv")

cleaned_valid_questions = list(valid_questions_df['group rep'].unique())
random.shuffle(cleaned_valid_questions)
cleaned_valid_questions = [{
    "question_id": f"Q{str(index+1).rjust(4, '0')}",
    "question": question
} for index, question in enumerate(cleaned_valid_questions)]
cleaned_valid_questions_len = len(cleaned_valid_questions)

cleaned_invalid_questions = list(invalid_questions_df['group rep'].unique())
random.shuffle(cleaned_invalid_questions)
cleaned_invalid_questions = [{
    "question_id": f"Q{str(index+1+cleaned_valid_questions_len).rjust(4, '0')}",
    "question": question
} for index, question in enumerate(cleaned_invalid_questions)]

with open("2022_mixed_initiative_question_pool.json", "w") as question_pool_file:
    json.dump(cleaned_valid_questions + cleaned_invalid_questions,
              question_pool_file, indent=4, ensure_ascii=False)