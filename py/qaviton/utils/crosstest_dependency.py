import pytest


def dependencies(parametrize, names=None, depends=None, xfail=None, xfail_reason=''):
    r = []
    if xfail is None:
        if names is None and depends is None:
            for param in parametrize:
                r.append(pytest.mark.dependency()(param))

        elif names is not None and depends is None:
            for i in range(len(parametrize)):
                r.append(pytest.mark.dependency(name=names[i])(parametrize[i]))

        elif names is None and depends is not None:
            for param in parametrize:
                r.append(pytest.mark.dependency(depends=depends)(param))

        else:
            for i in range(len(parametrize)):
                r.append(pytest.mark.dependency(name=names[i], depends=depends)(parametrize[i]))
        return r

    elif xfail is True:
        if names is None and depends is None:
            for param in parametrize:
                r.append(pytest.mark.dependency()(pytest.mark.xfail(param, reason=xfail_reason)))

        elif names is not None and depends is None:
            for i in range(len(parametrize)):
                r.append(pytest.mark.dependency(name=names[i])(pytest.mark.xfail(parametrize[i], reason=xfail_reason)))

        elif names is None and depends is not None:
            for param in parametrize:
                r.append(pytest.mark.dependency(depends=depends)(pytest.mark.xfail(param, reason=xfail_reason)))

        else:
            for i in range(len(parametrize)):
                r.append(pytest.mark.dependency(name=names[i], depends=depends)(
                    pytest.mark.xfail(parametrize[i], reason=xfail_reason)))
        return r

    else:
        if names is None and depends is None:
            for i in range(len(parametrize)):
                if i in xfail:
                    r.append(pytest.mark.dependency()(pytest.mark.xfail(parametrize[i], reason=xfail_reason)))
                else:
                    r.append(pytest.mark.dependency()(parametrize[i]))

        elif names is not None and depends is None:
            for i in range(len(parametrize)):
                if i in xfail:
                    r.append(
                        pytest.mark.dependency(name=names[i])(pytest.mark.xfail(parametrize[i], reason=xfail_reason)))
                else:
                    r.append(pytest.mark.dependency(name=names[i])(parametrize[i]))

        elif names is None and depends is not None:
            for i in range(len(parametrize)):
                if i in xfail:
                    r.append(
                        pytest.mark.dependency(depends=depends)(pytest.mark.xfail(parametrize[i], reason=xfail_reason)))
                else:
                    r.append(pytest.mark.dependency(depends=depends)(parametrize[i]))

        else:
            for i in range(len(parametrize)):
                if i in xfail:
                    r.append(pytest.mark.dependency(name=names[i], depends=depends)(
                        pytest.mark.xfail(parametrize[i], reason=xfail_reason)))
                else:
                    r.append(pytest.mark.dependency(name=names[i], depends=depends)(parametrize[i]))
        return r