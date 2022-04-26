import utils
from StringMatcher import StringMatcher as SequenceMatcher


def ratio(s1, s2):
    s1, s2 = utils.make_type_consistent(s1, s2)

    m = SequenceMatcher(None, s1, s2)
    return utils.intr(100 * m.ratio())
