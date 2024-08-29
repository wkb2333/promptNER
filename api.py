import os
import qianfan
import re
import json
from tqdm import tqdm
from transformers import pipeline

# pipe = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")


os.environ["QIANFAN_ACCESS_KEY"] = "..."
os.environ["QIANFAN_SECRET_KEY"] = "..."

chat_comp = qianfan.ChatCompletion()
# image_to_text = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

def str2json(text) -> json:
    # 使用正则表达式匹配JSON内容
    # json_patterns = r'\{.*?\}'
    # json_objects = re.findall(json_patterns, text, re.DOTALL)

    json_objects = text[7:-3]
    # 解析每个JSON对象并打印
    # print(json_objects)
    json_obj = json.loads(json_objects)
    return json_obj

def get_ner(text, output_file=None):
    # 调用Qianfan API进行实体识别

    with open("prompts/prompt_in_use.txt", "r", encoding="utf-8") as f:
        prompt = f.read()

    resp = chat_comp.do(model="ERNIE-4.0-8K-0329", messages=[{
            "role": "user",
            "content": prompt
        },
        {
            "role": "assistant",
            "content": 'OK, I will help you identify entities in the sentence and show you my chain of thought.'
        },
        {
            "role": "user",
            "content": text
        }
        ])
    ner_json = str2json(resp['body']['result'])

    if output_file != None:
        with open(output_file, "w", encoding="utf-8") as f1:
            json.dump(ner_json, f1, indent=4)

    return ner_json

if __name__ == '__main__':
    # text = "我想买一台苹果手机，价格在1000-2000元之间。"
    # ner_json = get_ner(text)
    # print(ner_json)
    caption = image_to_text("https://ankur3107.github.io/assets/images/image-captioning-example.png")
    print(caption)