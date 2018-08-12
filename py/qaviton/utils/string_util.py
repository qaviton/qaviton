def find_substring(string, substring, count_start=0, count_stop=0):
    """ find substring with unknown start/finish index
     and return metadata of said string

    :param string: full string (str)
    :param substring: str
    :param count_start: starting index for the search after substring
    :param count_stop: end index for the search after substring
    :return: StringMeta
    """
    # enable reverse counting
    if count_start < 0:
        count_start = len(string) + count_start
    if count_stop < 0:
        count_stop = len(string) + count_stop

    # determine what part of the string to search at
    if count_start < count_stop:
        search_length = count_stop
    else:
        search_length = len(string) - 1

    result = False
    stop_searching_flag = False
    search_start = count_start
    search_stop = search_length

    # start searching from the start point all the way to the search length
    if len(string) >= len(substring):
        for i in range(search_start, search_stop):
            if string[i] == substring[0]:
                if len(substring) == 1:
                    result = True
                    stop_searching_flag = True
                count_start = i
                count_stop = i + 1
                if len(substring) > 1:
                    for b in range(1, len(substring)):
                        if i + b <= search_stop:
                            if string[i + b] != substring[b]:
                                break
                            count_stop += 1
                            if b == len(substring) - 1:
                                result = True
                                stop_searching_flag = True
                                break
                        else:
                            break
                if stop_searching_flag is True:
                    break

    class StringMeta:
        def __init__(self, result, start, stop, next, head, tail, substring, string, search_head, search_tail, search_string):
            """
            :param result: boolean
            :param start: sub_string start index (int)
            :param stop: sub_string last index (int)
            :param next: next index (int)
            :param head: everything before substring (str)
            :param tail: everything after substring (str)
            :param substring: str
            :param string: full string (str)
            :param search_head:
            :param search_tail:
            :param search_string:
            """
            self.result = result
            self.start = start
            self.stop = stop
            self.next = next
            self.head = head
            self.tail = tail
            self.substring = substring
            self.string = string
            self.search_head = search_head
            self.search_tail = search_tail
            self.search_string = search_string

    return StringMeta(
        result=result,
        start=count_start,
        stop=count_stop-1,
        next=count_stop,
        head=string[:count_start],
        tail=string[count_stop:],
        substring=substring,
        string=string,
        search_head=string[search_start:count_start],
        search_tail=string[count_stop:search_stop],
        search_string=string[search_start:search_stop])


def get_string_tail(string, sub_string):
    r = find_substring(string, sub_string)
    if r.result is True:
        return r.tail


def find_string_between_first_two_sub_strings(string, substring1, substring2):
    for i in range(len(string)):
        r = find_substring(string, substring1, i)
        if r.result is True:
            a = r.next
            r = find_substring(string, substring2, a)
            if r.result is True:
                b = r.start
                return string[a:b]
        if i == len(string) - 1:
            return ''


def get_number_from_string(string):
    s = ''
    for c in range(len(string)):
        if string[c].isdecimal():
            s += string[c]
    if len(s) == 0:
        return None
    return int(s)
