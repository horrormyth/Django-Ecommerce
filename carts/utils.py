""" All the utilities function goes here """


def round_and_format_with_2decimal(value):
    result = round(value, 2)
    return '%.2f' % result
