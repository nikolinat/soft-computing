import itertools
import copy

table_cards = [6]
hand_cards = [16, 14]

card_signs = {0: 11, 1: 11, 2: 11, 3: 11, 4: 2, 5: 2, 6: 2, 7: 2, 8: 3, 9: 3, 10: 3, 11: 3, 12: 4, 13: 4, 14: 4,
              15: 4, 16: 5, 17: 5, 18: 5, 19: 5, 20: 6, 21: 6, 22: 6, 23: 6, 24: 7, 25: 7, 26: 7, 27: 7, 28: 8,
              29: 8, 30: 8, 31: 8, 32: 9, 33: 9, 34: 9, 35: 9, 36: 10, 37: 10, 38: 10, 39: 20, 40: 12, 41: 12,
              42: 12, 43: 12, 44: 13, 45: 13, 46: 13, 47: 13, 48: 14, 49: 14, 50: 14, 51: 14}

card_values = {0: 1, 1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 2, 8: 3, 9: 3, 10: 3, 11: 3, 12: 4, 13: 4, 14: 4,
               15: 4, 16: 5, 17: 5, 18: 5, 19: 5, 20: 6, 21: 6, 22: 6, 23: 6, 24: 7, 25: 7, 26: 7, 27: 7, 28: 8,
               29: 8, 30: 8, 31: 8, 32: 9, 33: 9, 34: 9, 35: 9, 36: 10, 37: 10, 38: 10, 39: 20, 40: 12, 41: 12,
               42: 12, 43: 12, 44: 13, 45: 13, 46: 13, 47: 13, 48: 14, 49: 14, 50: 14, 51: 14}

card_priorities = {0: 5, 1: 5, 2: 5, 3: 5, 4: 1, 5: 1, 6: 5, 7: 1, 8: 1, 9: 1, 10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1,
                   16: 1, 17: 1, 18: 1, 19: 1, 20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1,
                   30: 1, 31: 1, 32: 1, 33: 1, 34: 1, 35: 1, 36: 5, 37: 5, 38: 5, 39: 7, 40: 5, 41: 5, 42: 5, 43: 5,
                   44: 5, 45: 5, 46: 5, 47: 5, 48: 5, 49: 5, 50: 5, 51: 5}

dictionary = {}
hand_cards_value = []


def fill_hand_card_values():
    for card in hand_cards:
        hand_cards_value.append(card_signs[card])


def sum_cards(cards):
    sum_el = 0
    for i in range(len(cards)):
        sum_el += card_values[cards[i]]
    return sum_el


def find():
    for i in range(0, len(table_cards) + 1):
        for j in itertools.combinations(table_cards, i):
            cards = list(j)
            if len(cards) == 0:
                continue

            sum_el = sum_cards(cards)
            add_to_dictionary(sum_el, cards)

            if (0 in cards or 1 in cards or 2 in cards or 3 in cards) and (sum_el != 1):
                sum_el += 10
                add_to_dictionary(sum_el, cards)

    return copy.deepcopy(dictionary)


def add_to_dictionary(sum_el, list_of_el):
    if sum_el <= 14:
        if sum_el == 1:
            sum_el = 11

        if sum_el in dictionary.keys():
            dictionary[sum_el].append(list_of_el)
        else:
            dictionary[sum_el] = [list_of_el]


def find_result():
    dictionary_copy = find()

    for key in dictionary.keys():
        if key not in hand_cards_value:
            dictionary_copy.pop(key)

    if not dictionary_copy:
        el, priority = no_moves()
        return el, priority, []

    for key, value in dictionary_copy.items():
        if (len(value)) != 1:
            max_val = 0
            max_el = []
            for i in range(1, len(value) + 1):
                for j in itertools.combinations(value, i):
                    cards = list(j)
                    if not iterative_intersect(cards):
                        continue

                    sum_o = 0
                    for k in cards:
                        sum_o += sum_priorities(k)

                    if sum_o > max_val:
                        max_val = sum_o
                        max_el = cards

            dictionary_copy[key] = [max_el, max_val]
        else:
            dictionary_copy[key] = [value, sum_priorities(value[0])]

    max_val = 0
    max_el = -1
    max_step = []
    for key in dictionary_copy.keys():
        if dictionary_copy[key][1] > max_val or \
                (dictionary_copy[key][1] == max_val and len(dictionary_copy[key][0]) > len(max_step)):

            max_val = dictionary_copy[key][1]
            max_el = key
            max_step = dictionary_copy[key][0]

    return max_el, max_val, max_step


def sum_priorities(list_el):
    el_sum = 0
    for el in list_el:
        el_sum += card_priorities[el]

    return el_sum


def iterative_intersect(cards):
    for j in itertools.combinations(cards, 2):
        intersection_l = list(set.intersection(*map(set, j)))
        if len(intersection_l) != 0:
            return False
    return True


def no_moves():
    min_priority = 100
    min_element = None
    for card in hand_cards:
        if card_priorities[card] < min_priority or \
                (card_priorities[card] == min_priority and card_values[card] < card_values[min_element]):
            min_priority = card_priorities[card]
            min_element = card

    return min_element, min_priority


fill_hand_card_values()
print(find_result())
