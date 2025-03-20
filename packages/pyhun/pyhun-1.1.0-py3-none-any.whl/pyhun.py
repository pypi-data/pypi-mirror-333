from enum import Enum, auto
from datetime import date


class Phoneme(Enum):
    HIGH = auto()
    LOW = auto()


def get_phoneme_for_day(day: int):
    assert 1 <= day <= 31, 'there can be 31 days in a month'

    if day % 10 == 0:
        if day == 10:
            return Phoneme.HIGH
        return Phoneme.LOW

    if day % 10 in [3, 6, 8]:
        return Phoneme.LOW

    if day == 2:
        return Phoneme.LOW

    return Phoneme.HIGH


def get_human_date(raw_date: date):
    months = {
        1: 'január',
        2: 'február',
        3: 'március',
        4: 'április',
        5: 'május',
        6: 'június',
        7: 'július',
        8: 'augusztus',
        9: 'szeptember',
        10: 'október',
        11: 'november',
        12: 'december',
    }

    return f'{raw_date.year}. {months[raw_date.month]} {raw_date.day}.'


def get_human_date_with_on(raw_date: date):
    endings = {
        Phoneme.HIGH: 'én',
        Phoneme.LOW: 'án',
    }

    human_date = get_human_date(raw_date)[:-1]
    ending = endings[get_phoneme_for_day(raw_date.day)]

    return f'{human_date}-{ending}'


def get_human_date_with_from(raw_date: date):
    endings = {
        Phoneme.HIGH: 'től',
        Phoneme.LOW: 'tól',
    }

    human_date = get_human_date(raw_date)[:-1]
    ending = endings[get_phoneme_for_day(raw_date.day)]

    return f'{human_date}-{ending}'


def get_human_date_with_of(raw_date: date):
    human_date = get_human_date(raw_date)[:-1]

    return f'{human_date}-i'


def get_number_with_letters_under_thousand(number_as_string: str):
    hundreds = {
        '0': '',
        '1': 'száz',
        '2': 'kétszáz',
        '3': 'háromszáz',
        '4': 'négyszáz',
        '5': 'ötszáz',
        '6': 'hatszáz',
        '7': 'hétszáz',
        '8': 'nyolcszáz',
        '9': 'kilencszáz',
    }

    tens = {
        '0': '',
        '1': 'tizen',
        '2': 'huszon',
        '3': 'harminc',
        '4': 'negyven',
        '5': 'ötven',
        '6': 'hatvan',
        '7': 'hetven',
        '8': 'nyolcvan',
        '9': 'kilencven',
    }

    tens_standalone = {
        '0': '',
        '1': 'tíz',
        '2': 'húsz',
        '3': 'harminc',
        '4': 'negyven',
        '5': 'ötven',
        '6': 'hatvan',
        '7': 'hetven',
        '8': 'nyolcvan',
        '9': 'kilencven',
    }

    ones = {
        '0': '',
        '1': 'egy',
        '2': 'két',
        '3': 'három',
        '4': 'négy',
        '5': 'öt',
        '6': 'hat',
        '7': 'hét',
        '8': 'nyolc',
        '9': 'kilenc',
    }

    number_with_letters = ''

    if len(number_as_string) >= 3:
        number_with_letters += hundreds[number_as_string[-3]]
    if len(number_as_string) >= 2:
        number_with_letters += tens[number_as_string[-2]] \
            if number_as_string[-1] != '0' else \
            tens_standalone[number_as_string[-2]]
    number_with_letters += ones[number_as_string[-1]]

    return number_with_letters


def get_number_with_letters(number: int):
    assert 0 <= number, 'number should be positive'

    if number == 0:
        return 'nulla'

    number_as_string = str(number)
    number_length = len(number_as_string)

    assert number_length <= 9, 'number should contain maximum 9 digits'

    powers = {
        0: '',
        3: 'ezer',
        6: 'millió',
    }

    parts = []

    for i in range(0, number_length, 3):
        start = max(0, number_length-i-3)
        end = number_length-i
        number_part = number_as_string[start:end]
        if i != 0 and number_part == '1':
            number_with_letters_part = ''
        else:
            number_with_letters_part = get_number_with_letters_under_thousand(number_part)
        number_with_letters_part += powers[i]
        if number_with_letters_part:
            parts.append(number_with_letters_part)

    parts.reverse()

    if len(parts) == 1 or (len(parts) == 2 and number < 2000):
        return ''.join(parts)

    return '-'.join(parts)
