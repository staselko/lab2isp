class Task1:
    def __init__(self):
        self.text_dict = dict() 
        self.is_analysed = False
        return

    def run_task(self):
        print("Set text:")
        self.set_text(input())
        print("Do you want to set k, n?\n Yes/Other input")
        answer = input()
        if answer == "Yes":
            k = input()
            if k.isnumeric():
               k = int(k)
            else:
                k = 10 
            n = input()
            if n.isnumeric():
               n = int(n)
            else:
                n = 4
        self.analyse(k, n)
        return

    def set_text(self, text):
        self.text = text
        return

    def analyse(self, k=10, n=4):
        sentences = self.__split_in_sentences(self.__format_text(self.text, "\r\t\n"), ".?!")
        sentence_dict = {"word_count":[], "text":[], "length":0}
        for sentence in sentences:
            counter = 0
            formated_sentence = self.__format_text(sentence, "{\\}|<>#^,.!&?[]():;\'\"-*@\n\t\r")
            formated_sentence = formated_sentence.lower()
            for word in formated_sentence.split(" "):
                if word == '':
                    continue
                else:
                    counter += 1
            sentence_dict["text"].append(sentence)
            sentence_dict["word_count"].append(counter)
            sentence_dict["length"] = len(sentences)
        self.text_dict.update({"sentences":sentence_dict})
        self.word_statistic()
        self.is_analysed = True
        print("words in average: {}".format(sum(sentence_dict["word_count"]) / sentence_dict["length"]))
        print("words in median: {}".format(sorted(sentence_dict["word_count"])[sentence_dict["length"] // 2]))
        for i in range(sentence_dict["length"]):
            print("Word amount: {word_amount} | Sentence: {sentence}".format(word_amount=self.text_dict["sentences"]["word_count"][i], sentence=self.text_dict["sentences"]["text"][i]))
        self.symbol_sequence_rate(k, n)
        return

    def word_statistic(self):
        word_dict = {}
        formated_text = self.__format_text(self.text, "{\\}|<>#^,.!&?():;\'\"-*@\n\t\r")
        formated_text = formated_text.lower()
        for word in formated_text.split(" "):
            if word == '':
                continue
            else:
                if word_dict.get(word) != None:
                    word_dict[word] += 1
                else:
                    word_dict.update({word:1})
        self.text_dict.update({"words":word_dict})
        print(word_dict)
        return 

    def symbol_sequence_rate(self, k=10, n=4):
        if self.is_analysed == False:
            raise ValueError("Text preprocessing expected before")
        hashed_dict = {}
        hashed_dict.clear()
        for word in self.text_dict["words"].keys():
            if len(word) < n or not word.isalpha():
                continue
            sliced_hashes = [self.__hash_word(word[i:n + i]) for i in range(len(word) - n + 1)]
            for hash_val in sliced_hashes:
                if hashed_dict.get(hash_val) != None:
                    hashed_dict[hash_val] += 1*self.text_dict["words"][word]
                else:
                    hashed_dict.update({hash_val:self.text_dict["words"][word]})
        hashed_dict = dict(sorted(hashed_dict.items(), key=lambda item: -item[1]))
        print("{} most recent {}-grams".format(k, n))
        print([(self.__decode_word(key, n), hashed_dict[key]) for key in list(hashed_dict.keys())[0:k]])    
        return

    def __hash_word(self, word):
        hash_val = 0
        idx = 0
        for sym in word:
            hash_val |= (ord(sym) - ord('a')) << 5*idx
            idx += 1
        return hash_val

    def __decode_word(self, hash_val, length):
        return "".join([chr(((hash_val >> 5*idx) & 31) + ord('a')) for idx in range(length)])

    def __format_text(self, text, sym_ignored):
        result = text
        for sym in sym_ignored:
            result = result.replace(sym, "")
        return result

    def __split_in_sentences(self, text, sep_list):
        sentence_sequence = [text]
        for sep in sep_list:
            subsequences = []
            temp_sequence = []
            for sentence in sentence_sequence:
                subsequences.append(sentence.split(sep + " "))
            for seq in subsequences:
                temp_sequence += seq
            sentence_sequence = temp_sequence
        return sentence_sequence