import os

first_last_d = dict()


def read_files():
    for file in os.listdir("public"):
        if file.endswith(".txt"):
            with open(os.path.join("public", file), encoding="utf8") as fp:
                line = fp.readline()
                while line:
                    sentence = line.strip()
                    if sentence:
                        if sentence[0].isalpha() and sentence[-1].isalpha():
                            first_last = sentence[0] + sentence[-1]
                            first_last = first_last.lower()
                            if not first_last_d.get(first_last):
                                first_last_d[first_last] = sentence
                        if len(first_last_d) == 676:  #26*26
                            return
                    line = fp.readline()


def get_sentence(name_pokemon):
    res = first_last_d.get(name_pokemon[0] + name_pokemon[-1])
    if res:
        return {"sentence": res}
    return {"status": "not exist sentence"}
