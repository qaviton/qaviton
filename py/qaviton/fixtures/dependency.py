import pytest
from qaviton.exceptions import DependencyException
from qaviton.utils import filer
from qaviton.utils.operating_system import s


class Dependencies:
    path = None

    running = ''
    passed = '0'
    failed = '1'
    skipped = '2'

    @staticmethod
    def set_path(path):
        Dependencies.path = path

    @staticmethod
    def add(name):
        filer.create_file(Dependencies.path + s + name)

    @staticmethod
    def get(name):
        with open(Dependencies.path + s + name) as f:
            return f.read()

    @staticmethod
    def get_all():
        return filer.get_dir_files(Dependencies.path)

    @staticmethod
    def set(name, status):
        with open(Dependencies.path + s + name, 'w+') as f:
            f.write(str(status))

    @staticmethod
    def rename(name, new_name):
        filer.rename_file(Dependencies.path + s + name, Dependencies.path + s + new_name)

    @staticmethod
    def add_and_set(name, status):
        Dependencies.add(name)
        Dependencies.set(name, status)

    @staticmethod
    def remove(name):
        filer.delete_file(Dependencies.path + s + name)

    @staticmethod
    def remove_all():
        filer.delete_all_files(Dependencies.path)


class Depend:
    dependencies = Dependencies

    def __init__(self):
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

                if status == Dependencies.running:
                    raise DependencyException("Test dependency {} has not yet finished running.\n"
                                              "please consider using pytest-ordering.\n"
                                              "more info at: https://github.com/ftobia/pytest-ordering"
                                              .format(dependency))

                elif status == Dependencies.failed:
                    self.behave_when_dependency_fails("Test dependency {} failed".format(dependency))

                elif status == Dependencies.skipped:
                    self.behave_when_dependency_is_skipped("Test dependency {} skipped".format(dependency))

            else:
                raise DependencyException(
                    "Test dependency {} is either missing or miss-ordered.\n"
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

                    if status == Dependencies.running:
                        raise DependencyException("Test dependency {} has not yet finished running.\n"
                                                  "please consider using pytest-ordering.\n"
                                                  "more info at: https://github.com/ftobia/pytest-ordering".
                                                  format(dependency))

                    elif status == Dependencies.failed:
                        self.behave_when_dependency_fails("Test dependency {} failed".format(dependency))

                    elif status == Dependencies.skipped:
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

                    if status == Dependencies.running:
                        raise DependencyException("Test dependency {} has not yet finished running.\n"
                                                  "please consider using pytest-ordering.\n"
                                                  "more info at: https://github.com/ftobia/pytest-ordering".
                                                  format(dependency))

                    elif status == Dependencies.failed:
                        self.behave_when_dependency_fails("Test dependency {} failed".format(dependency))

                    elif status == Dependencies.skipped:
                        self.behave_when_dependency_is_skipped("Test dependency {} skipped".format(dependency))

            if pattern_found is False:
                raise DependencyException(
                    "Test dependency with pattern {}[ is either missing or miss-ordered.\n"
                    "In the miss-ordered case please consider reordering your tests with pytest-ordering.\n"
                    "more info at: https://github.com/ftobia/pytest-ordering"
                    .format(pattern))


class Dependency:
    dependencies = Dependencies

    def __init__(self, name):
        self.name = name
        Dependencies.add(name)
        self.depend = Depend()

    def set(self, name):
        Dependencies.rename(self.name, name)
        self.name = name
        return self

    def get(self):
        return self.name


@pytest.fixture()
def dependency(request):
    dep = Dependency(request.node.name)
    yield dep
    if request.node.rep_setup.failed:
        Dependencies.set(dep.name, Dependencies.failed)
    elif request.node.rep_setup.skipped:
        Dependencies.set(dep.name, Dependencies.skipped)
    else:
        if request.node.rep_call.failed:
            Dependencies.set(dep.name, Dependencies.failed)
        elif request.node.rep_call.skipped:
            Dependencies.set(dep.name, Dependencies.skipped)
        else:
            Dependencies.set(dep.name, Dependencies.passed)


@pytest.fixture()
def dependencies():
    return Dependencies


@pytest.fixture()
def depend():
    return Depend()
