#!/usr/bin/env python3
import argparse
import datetime
import random

THIS_YEAR = 'This Year:'
LAST_YEAR = 'Last Year:'
TWO_YEARS = '2 Years Ago:'

class Participant:
    def __init__(self, name, giving_to=None, gave_to=None):
        self.name = name
        self.giving_to = giving_to
        if gave_to is None:
            self.gave_to = []
        else:
            self.gave_to = gave_to

    def can_give_to(self, other):
        return self.name != other and \
            self.giving_to == None and \
            other not in self.gave_to

    def __str__(self):
        return '{} is giving to {}, and has given to {}'.format(
            self.name, self.giving_to, self.gave_to)


def parse_past_exchanges(filename):
    members = {}
    file = open(filename, 'r')
    names = file.readline().strip().split(',')
    for name in names:
        members[name] = Participant(name)
    
    file.readline()
    file.readline()
    for i in range(len(members)):
        pair = file.readline().split('->')
        members[pair[0]].gave_to.append(pair[1].strip())

    file.readline()
    file.readline()
    for i in range(len(members)):
        pair = file.readline().split('->')
        members[pair[0]].gave_to.append(pair[1].strip())

    return members

def is_valid_ordering(names):
    for i in range(len(names)):
        giver = names[i]
        j = (i + 1) % len(names)
        if not members[giver].can_give_to(names[j]):
            return False
    return True

def draw_names(names):
    givers = names.copy()
    random.shuffle(givers)
    shuffle_count = 0
    while not is_valid_ordering(givers):
        random.shuffle(givers)
        shuffle_count += 1
    print('had to shuffle {} times'.format(shuffle_count))
    return givers

def generate_gift_exchange(members, output):
    names = list(members.keys())
    drawn_names = draw_names(names)
    for i in range(len(drawn_names)):
        j = (i+1) % len(drawn_names)
        giver = drawn_names[i]
        recipient = drawn_names[j]
        members[giver].giving_to = recipient

    if output is None:
        output = 'exchange-{}.gex'.format(datetime.datetime.now().year)
    
    with open(output, 'w') as f:
        f.write('{}\n\n'.format(','.join(names)))
        f.write('{}\n'.format(THIS_YEAR))
        for member in members.values():
            f.write('{}->{}\n'.format(member.name, member.giving_to))

        f.write('\n{}\n'.format(LAST_YEAR))
        for member in members.values():
            f.write('{}->{}\n'.format(member.name, member.gave_to[0]))

        f.write('\n{}\n'.format(TWO_YEARS))
        for member in members.values():
            f.write('{}->{}\n'.format(member.name, member.gave_to[1]))

        f.close()

    for member in members.values():
        print(member)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', required=True,
                        help='Gift exchange input file.')
    parser.add_argument('-o', '--output', required=False,
                        help='Gift exchange output file.')
    args = parser.parse_args()
    members = parse_past_exchanges(args.input)
    generate_gift_exchange(members, args.output)