def sync_loop(iter1, iter2):
    """let's say you have 2 iterators that go hand to hand, but wait!...
    one of them is a little short on the spot.
    what to do?
    sync-em! run 1 and get the index of the other as well, when the short one is over just re run it from the start.
    works on indexed iterators only
    """
    if len(iter1) > len(iter2):
        big, small = iter1, iter2
    else:
        big, small = iter2, iter1

    i2 = len(small)-1
    for i in range(len(big)):
        if i > i2:
            i2 += len(small)
        if big == iter1:
            yield big[i], small[i-i2+len(small)-1]
        else:
            yield small[i - i2 + len(small) - 1], big[i]
