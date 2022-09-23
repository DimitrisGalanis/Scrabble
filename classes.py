import json
import random
from lets import lets, letters, checker
from itertools import permutations

words = set()
with open('greek7.txt', 'r', encoding='utf-8') as f:
    for line in f:
        words.add(line.strip('\n'))


class Player:
    __slots__ = "name"
    score = 0

    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def isvalid(word: str) -> bool:
        if word in words:
            return True
        return False

    @staticmethod
    def add_score(word: str):
        for element in word:
            Player.score += lets.get(element)[1]

    def __repr__(self):  # Logging for programmers
        return "Player's name is {}".format(self.name)

    def __str__(self):  # logging for end users
        return "Player's name is {}".format(self.name)


class Human(Player):

    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def __repr__(self):  # Logging for programmers
        return "Human's name is {}".format(self.name)

    def __str__(self):  # logging for end users
        return "Human's name is {}".format(self.name)

    @staticmethod
    def get_input_word():
        word = input("'p' για πάσο ή ΛΕΞΗ: ")
        return word


class Computer(Player):
    c_score = 0

    def __init__(self):
        super().__init__("AI , with Smart Fail Algorithm implemented")

    @staticmethod
    def smart_fail(available_letters: dict, word_numbers_available):
        if word_numbers_available > 3:
            available_letters_list = [*available_letters]  # parse into list

            # all possible combinations
            all_perms = set()
            for i in range(1, 1 + len(available_letters_list)):
                perms = [''.join(p) for p in permutations(available_letters, i)]  # iteration
                all_perms.update(set(perms))  # remove duplicates

            all_perms = all_perms.intersection(words)
            perms_dict = dict.fromkeys(all_perms, 0)
            for i in all_perms:
                score = 0
                for element in i:
                    score += lets.get(element)[1]
                perms_dict[i] = score

            a = sorted(perms_dict.items(), key=lambda x: x[1], reverse=True)

            if len(a) >= 3:
                Computer.c_score += a[2][1]
                print(f'ΛΕΞΗ: {a[2][0]} , ΒΑΘΜΟΣ ΛΕΞΗΣ: {a[2][1]}  και Score Computers = {Computer.c_score}')
            elif len(a) >= 2:
                Computer.c_score += a[1][1]
                print(f'ΛΕΞΗ: {a[1][0]} , ΒΑΘΜΟΣ: {a[1][1]}')
            elif len(a) >= 1:
                Computer.c_score += a[0][1]
                print(f'ΛΕΞΗ: {a[0][0]} , ΒΑΘΜΟΣ: {a[0][1]}')
            else:
                print("No Word Found")

    def __repr__(self):  # Logging for programmers
        return "Computer's name is {}".format(self.name)

    def __str__(self):  # logging for end users
        return "Computer's name is {}".format(self.name)


class SakClass:  # Almost done
    __slots__ = "my_dict"
    letters = 104  # total available letters

    def __init__(self, my_dict=None):
        if my_dict is None:
            self.my_dict = {}  # if there is no dictionary on args
        else:
            self.my_dict = my_dict  # assign mutable dictionary

    def get_letters(self) -> dict:
        player_dict = dict()
        while SakClass.letters > 3 and len(player_dict) < 7:  # looping for 7 letters as long as letters are available
            counter = 0  # pseudo iterator for matching dict
            rant = random.randint(1, 24)
            for key, value in self.my_dict.items():  # matching with dictionary
                counter += 1
                if counter == rant and value[0] > 0:
                    player_dict.update({key: value[1]})
                    value[0] -= 1
                    SakClass.letters -= 1
        return player_dict

    def putback_letters(self, _dict: dict):
        for letter in _dict:
            self.my_dict[letter][0] += 1  # adding 1 στον αριθμό εμφανίσεων
            SakClass.letters += 1  # adding one on leftover letters
        _dict.clear()


class Game:  # Almost Finished
    __slots__ = "human", "computer", "sak"

    def __init__(self, human: Human, computer: Computer, sak: SakClass):
        self.human = human
        self.computer = computer
        self.sak = sak

    @staticmethod
    def dump(data):
        with open('scores.json', 'w') as f_json:
            json.dump(data, f_json)

    @staticmethod
    def load():
        with open('scores.json', 'r') as f_json:
            data = json.load(f_json)
        print(data)

    def setup(self):  # κάνει τις απαραίτητες ενέργειες κατά το ξεκίνημα του παιχνιδιού
        pass

    def run(self):
        # HUMAN TURN
        while self.sak.letters > 3:
            print(f"\n{self.human.name}'s Turn")
            human_letters = self.sak.get_letters()  # returns dictionary
            print(human_letters)
            flag = True
            while flag:
                word = self.human.get_input_word()
                if word == 'p':
                    flag = False
                    self.sak.putback_letters(human_letters)
                    break
                for element in word:
                    if element not in letters and word != 'p':
                        print("Μη αποδεκτά γράμματα , προσπάθησε ξανά")
                        break
                    else:
                        if self.human.isvalid(word) and checker(word, human_letters):
                            flag = False
                            self.human.add_score(word)
                            print(f'Total score: {self.human.score}\n')
                            break
                        else:
                            print("Δεν είναι αποδεκτή η λέξη , προσπάθησε ξανά")
                            break

            # COMPUTER TURN
            print("************************\nComputer's Turn")
            computer_letters = self.sak.get_letters()
            if len(computer_letters) > 3:
                print(computer_letters)
            self.computer.smart_fail(computer_letters, self.sak.letters)

        if self.sak.letters <= 3:
            print("NOT ENOUGH LETTERS")
            print(f"{self.human.name}'s Score = {self.human.score}")
            print(f"Computers' Score = {self.computer.c_score}")
            data_human = str(self.human.name) + "'s" + " Score = " + str(self.human.score)
            data_computer = "Computer's" + " Score = " + str(self.computer.c_score)
            dump_dict = {
                "1": data_human,
                "2": data_computer
            }
            self.dump(dump_dict)

    @staticmethod
    def end():
        quit()
