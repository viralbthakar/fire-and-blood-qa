# import tensorflow as tf
# from datasets import load_dataset
# from transformers import AutoTokenizer
# from transformers import DefaultDataCollator
# from transformers import AutoModelForQuestionAnswering, TrainingArguments, Trainer
# from transformers import create_optimizer
# from transformers import TFAutoModelForQuestionAnswering, TFDistilBertForQuestionAnswering

# squad = load_dataset("squad", split="train[:5000]")
# squad = squad.train_test_split(test_size=0.2)
# print(squad["train"][0])

# tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")


# def preprocess_function(examples):
#     questions = [q.strip() for q in examples["question"]]
#     inputs = tokenizer(
#         questions,
#         examples["context"],
#         max_length=384,
#         truncation="only_second",
#         return_offsets_mapping=True,
#         padding="max_length",
#     )

#     offset_mapping = inputs.pop("offset_mapping")
#     answers = examples["answers"]
#     start_positions = []
#     end_positions = []

#     for i, offset in enumerate(offset_mapping):
#         answer = answers[i]
#         start_char = answer["answer_start"][0]
#         end_char = answer["answer_start"][0] + len(answer["text"][0])
#         sequence_ids = inputs.sequence_ids(i)

#         # Find the start and end of the context
#         idx = 0
#         while sequence_ids[idx] != 1:
#             idx += 1
#         context_start = idx
#         while sequence_ids[idx] == 1:
#             idx += 1
#         context_end = idx - 1

#         # If the answer is not fully inside the context, label it (0, 0)
#         if offset[context_start][0] > end_char or offset[context_end][1] < start_char:
#             start_positions.append(0)
#             end_positions.append(0)
#         else:
#             # Otherwise it's the start and end token positions
#             idx = context_start
#             while idx <= context_end and offset[idx][0] <= start_char:
#                 idx += 1
#             start_positions.append(idx - 1)

#             idx = context_end
#             while idx >= context_start and offset[idx][1] >= end_char:
#                 idx -= 1
#             end_positions.append(idx + 1)

#     inputs["start_positions"] = start_positions
#     inputs["end_positions"] = end_positions
#     return inputs


# tokenized_squad = squad.map(
#     preprocess_function, batched=True, remove_columns=squad["train"].column_names)

# data_collator = DefaultDataCollator(return_tensors="tf")

# batch_size = 16
# num_epochs = 2
# total_train_steps = (len(tokenized_squad["train"]) // batch_size) * num_epochs
# optimizer, schedule = create_optimizer(
#     init_lr=2e-5,
#     num_warmup_steps=0,
#     num_train_steps=total_train_steps,
# )


# model = TFDistilBertForQuestionAnswering.from_pretrained(
#     "distilbert-base-uncased")

# tf_train_set = model.prepare_tf_dataset(
#     tokenized_squad["train"],
#     shuffle=True,
#     batch_size=16,
#     collate_fn=data_collator,
# )

# tf_validation_set = model.prepare_tf_dataset(
#     tokenized_squad["test"],
#     shuffle=False,
#     batch_size=16,
#     collate_fn=data_collator,
# )


# model.compile(optimizer=optimizer)
# model.fit(x=tf_train_set, validation_data=tf_validation_set, epochs=3)


# from transformers import pipeline
# question_answerer = pipeline(
#     "question-answering", model="distilbert-base-cased-distilled-squad")

# question = "How many programming languages does BLOOM support?"
# context = "BLOOM has 176 billion parameters and can generate text in 46 languages natural languages and 13 programming languages."

# print(question_answerer(question=question, context=context))


import tensorflow as tf
import pandas as pd
import datasets
from datasets import load_dataset
from transformers import AutoTokenizer
from transformers import DefaultDataCollator
from transformers import AutoModelForQuestionAnswering, TrainingArguments, Trainer
from transformers import create_optimizer
from transformers import TFAutoModelForQuestionAnswering, TFDistilBertForQuestionAnswering

squad = load_dataset("squad", split="train[:5000]")
squad = squad.train_test_split(test_size=0.2)
print(squad["train"][0])

QAC_data = pd.read_csv("../data/qa-data/NER/Caraxes.csv")


def squadify(QAC_data):
    QAC_dict = {}
    QAC_dict["context"] = list(QAC_data.to_dict()["context"].values())
    QAC_dict["question"] = list(QAC_data.to_dict()["questions"].values())
    QAC_dict["id"] = [str(x) for x in range(len(QAC_data))]
    QAC_dict["title"] = [
        "FireAndBlood for x in " for x in range(len(QAC_data))]
    QAC_dict["answers"] = []
    for id, answer in enumerate(list(QAC_data["answers"].values)):
        answer_start = QAC_dict["context"][id].find(answer.split(" ")[0])
        answer_obs = {"text": [answer], "answer_start": [answer_start]}
        QAC_dict["answers"].append(answer_obs)
    return QAC_dict


squad = datasets.Dataset.from_pandas(pd.DataFrame(data=squadify(QAC_data)))
train_data, validation_data = squad.train_test_split(test_size=0.1).values()
squad = datasets.DatasetDict({"train": train_data, "test": validation_data})
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")


def preprocess_function(examples):
    questions = [q.strip() for q in examples["question"]]
    inputs = tokenizer(
        questions,
        examples["context"],
        max_length=384,
        truncation="only_second",
        return_offsets_mapping=True,
        padding="max_length",
    )

    offset_mapping = inputs.pop("offset_mapping")
    answers = examples["answers"]
    start_positions = []
    end_positions = []

    for i, offset in enumerate(offset_mapping):
        answer = answers[i]
        start_char = answer["answer_start"][0]
        end_char = answer["answer_start"][0] + len(answer["text"][0])
        sequence_ids = inputs.sequence_ids(i)

        # Find the start and end of the context
        idx = 0
        while sequence_ids[idx] != 1:
            idx += 1
        context_start = idx
        while sequence_ids[idx] == 1:
            idx += 1
        context_end = idx - 1

        # If the answer is not fully inside the context, label it (0, 0)
        if offset[context_start][0] > end_char or offset[context_end][1] < start_char:
            start_positions.append(0)
            end_positions.append(0)
        else:
            # Otherwise it's the start and end token positions
            idx = context_start
            while idx <= context_end and offset[idx][0] <= start_char:
                idx += 1
            start_positions.append(idx - 1)

            idx = context_end
            while idx >= context_start and offset[idx][1] >= end_char:
                idx -= 1
            end_positions.append(idx + 1)

    inputs["start_positions"] = start_positions
    inputs["end_positions"] = end_positions
    return inputs


tokenized_squad = squad.map(
    preprocess_function, batched=True, remove_columns=squad["train"].column_names)

data_collator = DefaultDataCollator(return_tensors="tf")

batch_size = 16
num_epochs = 2
total_train_steps = (len(tokenized_squad["train"]) // batch_size) * num_epochs
optimizer, schedule = create_optimizer(
    init_lr=2e-5,
    num_warmup_steps=0,
    num_train_steps=total_train_steps,
)


model = TFDistilBertForQuestionAnswering.from_pretrained(
    "distilbert-base-uncased")

tf_train_set = model.prepare_tf_dataset(
    tokenized_squad["train"],
    shuffle=True,
    batch_size=16,
    collate_fn=data_collator,
)

tf_validation_set = model.prepare_tf_dataset(
    tokenized_squad["test"],
    shuffle=False,
    batch_size=16,
    collate_fn=data_collator,
)


model.compile(optimizer=optimizer)
model.fit(x=tf_train_set, validation_data=tf_validation_set, epochs=3)


# from transformers import pipeline
# question_answerer = pipeline(
#     "question-answering", model="distilbert-base-cased-distilled-squad")

# question = "How many programming languages does BLOOM support?"
# context = "BLOOM has 176 billion parameters and can generate text in 46 languages natural languages and 13 programming languages."

# print(question_answerer(question=question, context=context))
