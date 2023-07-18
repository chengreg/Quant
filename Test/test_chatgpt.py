# -*- coding: utf-8 -*-
# @Time    : 2023/7/18 17:59
# @Author  : Chen GangQiang
# @Email   : uoaoo@163.com
# @File    : test_chatgpt.py
# @Software: PyCharm

import os
import openai

openai.api_key = "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"

start_sequence = "\nA:"
restart_sequence = "\n\nQ: "

while 1:

    prompt = input(restart_sequence)

    if prompt == "quit":
        break
    else:
        try:
            response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=0, max_tokens=100,
                                                top_p=1, frequency_penalty=0, presence_penalty=0)
            print(start_sequence, response["choices"][0]["text"].strip())
        except Exception as err:
            print(err)