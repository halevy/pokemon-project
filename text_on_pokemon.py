import os
import read_pdf_file
first_last_d = dict()


def insert_sentence_to_dict(sentence):
    if sentence:
        if sentence[0].isalpha() and sentence[-1].isalpha():
            first_last = sentence[0] + sentence[-1]
            first_last = first_last.lower()
            if not first_last_d.get(first_last):
                first_last_d[first_last] = sentence


def read_book():
    count = 2
    sentences = read_pdf_file.convert_pdf_to_txt('book.pdf')
    sentences = sentences[sentences.index("#1:"):]
    while sentences:
        try:
            index = sentences.index("#" + str(count) + ":")

            sentence = sentences[:index]
            try:
                sentence = sentence[:- sentence[::-1].index('.') -1]
            except ValueError:
                pass
            if '\n' in sentence:
                sentence = sentence.replace('\n', '')
            sentence = sentence[len(str(count)) + 3:]
            insert_sentence_to_dict(sentence)
            sentences = sentences[index:]
            count += 1
        except ValueError:
            break



def get_tip_of_pokemon(name_pokemon):
    res = first_last_d.get(name_pokemon[0] + name_pokemon[-1])
    if res:
        return {"The pokemon tip": res}
    for key in first_last_d.keys():
        if key[0] == name_pokemon[0]:
            return {"The pokemon tip": first_last_d[key]}
    for key in first_last_d.keys():
        if key[-1] == name_pokemon[-1]:
            return {"The pokemon tip": first_last_d[key]}
    return {"status": "not exist tip"}
