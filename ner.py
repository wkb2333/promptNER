from api import get_ner
import json
from tqdm import tqdm

'''
    This is the main function of the program.
    在api.py中定义了使用百度提供的"ERNIE-4.0-8K-0329"模型进行命名实体识别的函数。
    调用get_ner(text), 传入待识别的文本，返回识别结果（字典）。
'''

save_path = 'output.json'

with open('datasets/science_test.txt', 'r', encoding='utf-8') as f:
    with open(save_path, 'w', encoding='utf-8') as fw:

        outputs = []

        for i in tqdm(range(50)):
            test_text = f.readline()
            result = get_ner(test_text)
            result['id'] = i
            outputs.append(result)

            json.dump(outputs, fw, indent=4)