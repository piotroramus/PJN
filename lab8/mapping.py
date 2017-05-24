import re


def create_mapping(corpus_file, output_file):
    """ Creates mapping of characters positions between two files:
            - an input corpus as a plain text
            - corpus with stripped (all!) whitespaces
        It has the following structure:
        map[(stripped_start, stripped_end)]: (original_start, original_end)
        This is needed as the Liner2 tool returns positions of the entities in file
        as if there are no whitespaces.
    """

    with open(corpus_file, 'rb') as f:
        content = f.read().decode('utf-8')

    # 'characters' means anything but whitespaces
    characters_positions = list()
    for m in re.finditer(r'[^\s]+', content, flags=re.UNICODE):
        characters_positions.append((m.start(), m.end()))

    with open(output_file, 'w') as out:
        pointer = 0
        for start, end in characters_positions:
            size = end - start
            out.write("{},{},{},{}\n".format(pointer, pointer + size, start, end))
            pointer += size


def load_mapping(map_file):
    mapping = dict()
    with open(map_file, 'r') as f:
        for line in f:
            stripped_start, stripped_end, original_start, original_end = map(int, line.split(','))
            mapping[(stripped_start, stripped_end)] = (original_start, original_end)

    return mapping


def get_original_positions(mapping, start, end):
    for stripped_start, stripped_end in mapping:
        # we do not look for end <= stripped_end - 1 condition
        # because entites can be formed from more than one word
        if start >= stripped_start:
            return mapping[(stripped_start, stripped_end)]
    raise IndexError('Cannot find mapping for ({},{})'.format(start, end))


if __name__ == '__main__':
    corpus_file = 'resources/potop/potop.txt'
    mapping_output = 'resources/potop/stripped_original_mapping.txt'
    create_mapping(corpus_file, mapping_output)
