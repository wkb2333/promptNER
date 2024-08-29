import os
import random

entity_domain = ['conll2003', 'ai', 'literature', 'music', 'politics', 'science']
politics_labels = ['O', 'B-country', 'B-politician', 'I-politician', 'B-election', 'I-election', 'B-person', 'I-person', 'B-organisation', 'I-organisation', 'B-location', 'B-misc', 'I-location', 'I-country', 'I-misc', 'B-politicalparty', 'I-politicalparty', 'B-event', 'I-event']
science_labels = ['O', 'B-scientist', 'I-scientist', 'B-person', 'I-person', 'B-university', 'I-university', 'B-organisation', 'I-organisation', 'B-country', 'I-country', 'B-location', 'I-location', 'B-discipline', 'I-discipline', 'B-enzyme', 'I-enzyme', 'B-protein', 'I-protein', 'B-chemicalelement', 'I-chemicalelement', 'B-chemicalcompound', 'I-chemicalcompound', 'B-astronomicalobject', 'I-astronomicalobject', 'B-academicjournal', 'I-academicjournal', 'B-event', 'I-event', 'B-theory', 'I-theory', 'B-award', 'I-award', 'B-misc', 'I-misc']
music_labels = ['O', 'B-musicgenre', 'I-musicgenre', 'B-song', 'I-song', 'B-band', 'I-band', 'B-album', 'I-album', 'B-musicalartist', 'I-musicalartist', 'B-musicalinstrument', 'I-musicalinstrument', 'B-award', 'I-award', 'B-event', 'I-event', 'B-country', 'I-country', 'B-location', 'I-location', 'B-organisation', 'I-organisation', 'B-person', 'I-person', 'B-misc', 'I-misc']
literature_labels = ["O", "B-book", "I-book", "B-writer", "I-writer", "B-award", "I-award", "B-poem", "I-poem", "B-event", "I-event", "B-magazine", "I-magazine", "B-literarygenre", "I-literarygenre", 'B-country', 'I-country', "B-person", "I-person", "B-location", "I-location", 'B-organisation', 'I-organisation', 'B-misc', 'I-misc']
ai_labels = ["O", "B-field", "I-field", "B-task", "I-task", "B-product", "I-product", "B-algorithm", "I-algorithm", "B-researcher", "I-researcher", "B-metrics", "I-metrics", "B-programlang", "I-programlang", "B-conference", "I-conference", "B-university", "I-university", "B-country", "I-country", "B-person", "I-person", "B-organisation", "I-organisation", "B-location", "I-location", "B-misc", "I-misc"]
domain2labels = {"politics": politics_labels, "science": science_labels, "music": music_labels, "literature": literature_labels, "ai": ai_labels}


def list2str(lst, sep=' '):
    return sep.join(lst)

def in_text(split='train', domain='science'):
    data_path = os.path.join('ner_data', domain, split+'.txt')
    with open(data_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        sentences = []
        sentence = []
        ori_sentence = []
        ori_sentences = []
        entity = []
        last_token = ['', 'O']
        label_category = None
        for line in lines:
            if line == '\n':
                sentences.append(sentence)
                sentence = []
                ori_sentences.append(ori_sentence)
                ori_sentence = []
            else:
                token = line.split()
                if token[1] == 'O':
                    if last_token[1] in domain2labels[domain][1:] and entity:
                        entity.append(f'</{label_category[2:]}>')
                        sentence = sentence + entity
                        entity = []
                    sentence.append(token[0])
                    ori_sentence.append(token[0])
                elif token[1] in domain2labels[domain][1:]:
                    label_category = token[1]
                    if label_category[0] == 'B':
                        if last_token[1][0] == 'B' and entity:
                            entity.append(f'</{last_token[1][2:]}>')
                            sentence = sentence + entity
                            entity = []
                        entity.append(f'<{label_category[2:]}>')
                    entity.append(token[0])
                    ori_sentence.append(token[0])
                last_token = token

    file_name = 'datasets/' + domain + '_' + split + '.txt'

    with open(file_name, 'w', encoding='utf-8') as fw:
        for i in range(len(ori_sentences)):
            fw.write("text: '''" + list2str(ori_sentences[i]) + "'''\n")
        fw.write('\n')
        for i in range(len(ori_sentences)):
            fw.write("identified: '''" + list2str(sentences[i]) + "'''\n")
    print(f"{domain} {split}: {len(sentences)} sentences")
    # with open('test.txt', 'w', encoding='utf-8') as fw:
    #     samples = random.sample(range(len(ori_sentences)), 20)
    #     for i in samples:
    #         fw.write("origin: '''" + list2str(ori_sentences[i]) + "'''\n")
    #     for i in samples:
    #         fw.write("identified: '''" + list2str(sentences[i]) + "'''\n")


def generate_prompt():
    base = "You are an expert in the field of named entity recognition, and you will be given a sentence separated by triple quotation marks, and your task is to perform entity recognition on that sentence.\n# Description\n"
    base += '1. Use "<entity_category></entity_category>" in the sentence to indicate the entity, where "entity_category" needs to be replaced with a specific category.\n'
    base += '2. When no entities can be found, the output is "No entities found".\n'
    base += "3. Each step considers the previously identified entity and, if there is a more appropriate category, replaces it.\n"
    labels =domain2labels[domain][1:]
    label_list = []
    for label in labels:
        label_name = label[2:]
        label_list.append(label_name)
    label_set = set(label_list)
    label_list = list(label_set)
    steps = ''
    n = 1
    for i in range(len(label_set)):
        label_name = label_set.pop()
        steps += f'Step {i+1}: Please identify the {label_name} entity in the sentence, mark as <{label_name}></{label_name}> in the sentence, and replace the previous entity with the new one if there is a more appropriate category.\n'
        n += 1
    steps += f'Step {n}: Please combine all entities and export them in the original sentence.\n'
    with open('prompt2.txt', 'w', encoding='utf-8') as f:
        f.write(base + '\n' + steps)
    print(list2str(label_list, sep=', '))


def generate_data(domain):
    for split in ['train', 'test']:
        in_text(split, domain)

if __name__ == "__main__":
    for domain in entity_domain[1:]:
        generate_data(domain)
    # generate_prompt()