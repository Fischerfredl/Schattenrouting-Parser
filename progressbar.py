import sys


def progress(i, i_max):
    sys.stdout.write('\r')
    sys.stdout.write("[%-40s] %d%%" % ('=' * int((i/float(i_max))*40), (i / float(i_max) * 100)))
    sys.stdout.flush()
    if i == i_max:
        sys.stdout.write('\n')
    return