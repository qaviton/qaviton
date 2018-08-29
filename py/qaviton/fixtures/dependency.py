import pytest
from qaviton.utils import path
from qaviton.exceptions import DependencyException
from qaviton.utils import filer
from qaviton.utils.operating_system import s


class Depend:
    def __init__(self, request):
        self.request = request
        self.behave_when_dependency_fails = pytest.skip
        self.behave_when_dependency_is_skipped = pytest.skip

    def skip_when_dependency_fails(self):
        self.behave_when_dependency_fails = pytest.skip
        return self

    def fail_when_dependency_fails(self):
        self.behave_when_dependency_fails = pytest.fail
        return self

    def skip_when_dependency_is_skipped(self):
        self.behave_when_dependency_fails = pytest.skip
        return self

    def fail_when_dependency_is_skipped(self):
        self.behave_when_dependency_fails = pytest.fail
        return self

    def on(self, *dependencies):
        for dependency in dependencies:
            if dependency in Dependencies.get_all():
                status = Dependencies.get(dependency)
                if status == '':
                    raise DependencyException("Test dependency {} has not yet finished running.\n"
                                              "please consider using pytest-ordering.\n"
                                              "more info at: https://github.com/ftobia/pytest-ordering"
                                              .format(dependency))
                elif status == '1':
                    self.behave_when_dependency_fails("Test dependency {} failed".format(dependency))
                elif status == '2':
                    self.behave_when_dependency_is_skipped("Test dependency {} skipped".format(dependency))
            else:
                raise DependencyException("Test dependency {} is either missing or miss-ordered.\n"
                                          "In the miss-ordered case please consider reordering your tests "
                                          "with pytest-ordering.\n"
                                          "more info at: https://github.com/ftobia/pytest-ordering"
                                          .format(dependency))

    def on_pattern(self, *dependency_patterns):
        for pattern in dependency_patterns:
            pattern_found = False
            for dependency in Dependencies.get_all():
                if pattern in dependency or pattern == dependency:
                    pattern_found = True
                    status = Dependencies.get(dependency)
                    if status == '':
                        raise DependencyException("Test dependency {} has not yet finished running.\n"
                                                  "please consider using pytest-ordering.\n"
                                                  "more info at: https://github.com/ftobia/pytest-ordering".
                                                  format(dependency))
                    elif status == '1':
                        self.behave_when_dependency_fails("Test dependency {} failed".format(dependency))
                    elif status == '2':
                        self.behave_when_dependency_is_skipped("Test dependency {} skipped".format(dependency))
            if pattern_found is False:
                raise DependencyException(
                    "Test dependency with pattern {} is either missing or miss-ordered.\n"
                    "In the miss-ordered case please consider reordering your tests with pytest-ordering.\n"
                    "more info at: https://github.com/ftobia/pytest-ordering"
                    .format(pattern))

    def on_parameterized(self, *dependencies):
        for pattern in dependencies:
            pattern_found = False
            for dependency in Dependencies.get_all():
                if pattern == dependency.split("[")[0]:
                    pattern_found = True
                    status = Dependencies.get(dependency)
                    if status == '':
                        raise DependencyException("Test dependency {} has not yet finished running.\n"
                                                  "please consider using pytest-ordering.\n"
                                                  "more info at: https://github.com/ftobia/pytest-ordering".
                                                  format(dependency))
                    elif status == '1':
                        self.behave_when_dependency_fails("Test dependency {} failed".format(dependency))
                    elif status == '2':
                        self.behave_when_dependency_is_skipped("Test dependency {} skipped".format(dependency))
            if pattern_found is False:
                raise DependencyException(
                    "Test dependency with pattern {}[ is either missing or miss-ordered.\n"
                    "In the miss-ordered case please consider reordering your tests with pytest-ordering.\n"
                    "more info at: https://github.com/ftobia/pytest-ordering"
                    .format(pattern))


class Dependencies:
    dep = path.of(__file__)('../../tests/dependencies')

    @staticmethod
    def add(name):
        filer.create_file(Dependencies.dep+s+name)

    @staticmethod
    def get(name):
        with open(Dependencies.dep+s+name) as f:
            return f.read()

    @staticmethod
    def get_all():
        return filer.get_dir_files(Dependencies.dep)

    @staticmethod
    def set(name, status):
        with open(Dependencies.dep + s + name, 'w+') as f:
            f.write(status)

    @staticmethod
    def add_and_set(name, status):
        Dependencies.add(name)
        with open(Dependencies.dep + s + name, 'w+') as f:
            f.write(status)


@pytest.fixture()
def dependency(request):
    Dependencies.add(request.node.name)
    yield
    if request.node.rep_setup.failed:
        Dependencies.set(request.node.name, '1')
    elif request.node.rep_setup.skipped:
        Dependencies.set(request.node.name, '2')
    else:
        if request.node.rep_call.failed:
            Dependencies.set(request.node.name, '1')
        elif request.node.rep_call.skipped:
            Dependencies.set(request.node.name, '2')
        else:
            Dependencies.set(request.node.name, '0')


@pytest.fixture()
def depend(request):
    return Depend(request)
