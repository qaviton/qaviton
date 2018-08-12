from qaviton.utils.string_util import find_string_between_first_two_sub_strings, find_substring, get_number_from_string


def test_string_util():
    string = "dfgfdh FGFHFH fgrkkjhbgvcxc 00050000000701"
    substring = "0005"

    s1 = find_string_between_first_two_sub_strings(string, 'FGH', '007')
    assert s1 == ''
    s1 = find_string_between_first_two_sub_strings(string, 'FGF', '007')
    assert s1 == 'HFH fgrkkjhbgvcxc 000500000' # BUG
    r = find_substring(string, substring)
    n = get_number_from_string(r.substring)
    assert n == 5
