def lists(data):
    """ organize lists

        example:

        from qaviton.utils import organize

        organize_list = [(1,),(1,2,3),(1,2),(1,2,3,4)]
        print(organize.dicts(organize_list))

        will return:

        [[1, 1, 1, 1],[1, 1, 1, 2],[1, 1, 1, 3],[1, 1, 1, 4],[1, 1, 2, 1],[1, 1, 2, 2],
         [1, 1, 2, 3],[1, 1, 2, 4],[1, 1, 3, 1],[1, 1, 3, 2],[1, 1, 3, 3],[1, 1, 3, 4],
         [1, 2, 1, 1],[1, 2, 1, 2],[1, 2, 1, 3],[1, 2, 1, 4],[1, 2, 2, 1],[1, 2, 2, 2],
         [1, 2, 2, 3],[1, 2, 2, 4],[1, 2, 3, 1],[1, 2, 3, 2],[1, 2, 3, 3],[1, 2, 3, 4]]

    :type data: []
    :rtype: []
    """
    try:
        data.sort(key=len)

        all_possibilities = 1
        for i in range(len(data)):
            all_possibilities *= len(data[i])

        organized_data = [[] for _ in range(all_possibilities)]

        looper = all_possibilities
        for data_list in data:
            looper /= len(data_list)
            d = 0
            while d < all_possibilities:
                for i in data_list:
                    for _ in range(int(looper)):
                        organized_data[d].append(i)
                        d += 1
        return organized_data
    except ZeroDivisionError as e:
        raise ZeroDivisionError("empty lists are not allowed") from e


def dicts(data):
    """ organize named lists

        example:

        from qaviton.utils import organize

        organize_dict = {"a":(1,),"b":(1,2,3),"c":(1,2),"d":(1,2,3,4)}
        print(organize.dicts(organize_dict))
        will return:

        [{"a":1, "b":1, "c":1, "d":1},{"a":1, "b":1, "c":1, "d":2},{"a":1, "b":1, "c":1, "d":3},
         {"a":1, "b":1, "c":1, "d":4},{"a":1, "b":1, "c":2, "d":1},{"a":1, "b":1, "c":2, "d":2},
         {"a":1, "b":1, "c":2, "d":3},{"a":1, "b":1, "c":2, "d":4},{"a":1, "b":2, "c":1, "d":1},
         {"a":1, "b":2, "c":1, "d":2},{"a":1, "b":2, "c":1, "d":3},{"a":1, "b":2, "c":1, "d":4},
         {"a":1, "b":2, "c":2, "d":1},{"a":1, "b":2, "c":2, "d":2},{"a":1, "b":2, "c":2, "d":3},
         {"a":1, "b":2, "c":2, "d":4},{"a":1, "b":3, "c":1, "d":1},{"a":1, "b":3, "c":1, "d":2},
         {"a":1, "b":3, "c":1, "d":3},{"a":1, "b":3, "c":1, "d":4},{"a":1, "b":3, "c":2, "d":1},
         {"a":1, "b":3, "c":2, "d":2},{"a":1, "b":4, "c":2, "d":3},{"a":1, "b":3, "c":2, "d":4}]

    :type data: {[]}
    :rtype: [{}]
    """
    try:
        all_possibilities = 1
        for k in data:
            all_possibilities *= len(data[k])

        organized_data = []
        for _ in range(all_possibilities):
            organized_data.append({})
            for k in data:
                organized_data[-1][k] = []

        looper = all_possibilities
        for k in sorted(data, key=lambda k: len(data[k])):
            looper /= len(data[k])
            d = 0
            while d < all_possibilities:
                for i in data[k]:
                    for _ in range(int(looper)):
                        organized_data[d][k].append(i)
                        d += 1
        return organized_data
    except ZeroDivisionError as e:
        raise ZeroDivisionError("empty lists are not allowed") from e
