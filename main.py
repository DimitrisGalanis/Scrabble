# coding=utf-8
import json
from myfunctions_module import print_start, guidelines
from classes import SakClass, Human, Game, Computer
from lets import lets


def main() -> None:
    logs = "Empty logs"
    with open('scores.json', 'w') as f_json:
        json.dump(logs, f_json)
    print_start("*")
    human = Human("jimmy")
    computer = Computer()
    sak = SakClass(lets)
    game = Game(human, computer, sak)
    f = True
    while f:
        _input = input("Input: ")
        if _input == "1":
            game.load()
            f = False
        elif _input == "2":
            game.run()
            f = False
        elif _input == "3":
            f = False
            game.end()
        else:
            print("Μη σωστή επιλογή")


if __name__ == '__main__':
    main()
