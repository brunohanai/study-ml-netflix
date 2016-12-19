def split_and_adjust(text, separator=','):
    result = []

    for term in text.split(separator):
        result.append(term.strip().replace(' ', '').replace('-', ''))

    return ' '.join(result)

