def ordinal(n):
    if 10 < n < 14: return u'%sth' % n
    if n % 10 == 1: return u'%sst' % n
    if n % 10 == 2: return u'%snd' % n
    if n % 10 == 3: return u'%srd' % n
    return u'%sth' % n

