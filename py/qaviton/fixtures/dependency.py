import pytest
from qaviton.exceptions import DependencyException
from qaviton.utils import filer
from qaviton.utils.operating_system import s
from qaviton.utils.random_util import random_number
import time


class Dependencies:
    max_wait_period: int = 600
    min_wait_period: float = 0.1
    max_read_tries: int = max_wait_period * 10

    path = None

    running = ''
    passed = '0'
    failed = '1'
    skipped = '2'

    @staticmethod
    def wait_iterations():
        return int(Dependencies.max_wait_period/Dependencies.min_wait_period)

    @staticmethod
    def set_path(path):
        Dependencies.path = path
        filer.create_directory(path)

    @staticmethod
    def add(name):
        filer.create_file(Dependencies.path + s + name)

    @staticmethod
    def get(name):
        for i in range(Dependencies.max_read_tries):
            try:
                with open(Dependencies.path + s + name) as f:
                    return f.read()
            except Exception as e:
                if i+1 == Dependencies.max_read_tries:
                    raise e
                time.sleep(random_number(1, 1000)*0.0001)

    @staticmethod
    def get_all():
        return filer.get_dir_files(Dependencies.path)

    @staticmethod
    def set(name, status):
        for i in range(Dependencies.max_read_tries):
            try:
                with open(Dependencies.path + s + name, 'w+') as f:
                    f.write(str(status))
                    return
            except Exception as e:
                if i+1 == Dependencies.max_read_tries:
                    raise e
                time.sleep(random_number(1, 1000)*0.0001)

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

            # check if dependency is registered
            for _ in range(Dependencies.wait_iterations()):
                if dependency not in Dependencies.get_all():
                    time.sleep(Dependencies.min_wait_period)
                else:
                    break

            if dependency in Dependencies.get_all():
                status = Dependencies.get(dependency)

                # check if dependency is still running
                for _ in range(Dependencies.wait_iterations()):
                    if status == Dependencies.running:
                        time.sleep(Dependencies.min_wait_period)
                    else:
                        break

                if status == Dependencies.failed:
                    self.behave_when_dependency_fails("Test dependency {} failed".format(dependency))

                elif status == Dependencies.skipped:
                    self.behave_when_dependency_is_skipped("Test dependency {} skipped".format(dependency))

                elif status == Dependencies.running:
                    raise DependencyException(
                        "Test dependency {} has not yet finished running.\n"
                        "please consider using pytest-ordering or increase Dependencies.max_wait_period.\n"
                        "more info at: https://github.com/ftobia/pytest-ordering"
                        .format(dependency))
            else:
                raise DependencyException(
                    "Test dependency {} is either missing or miss-ordered.\n"
                    "In the miss-ordered case please consider reordering your tests with pytest-ordering.\n"
                    "more info at: https://github.com/ftobia/pytest-ordering"
                    .format(dependency))

    def on_pattern(self, *dependency_patterns):
        for pattern in dependency_patterns:
            pattern_found = False
            for dependency in Dependencies.get_all():

                # # check if dependency is registered
                # for _ in range(Dependencies.wait_iterations()):
                #     if pattern not in Dependencies.get_all():
                #         time.sleep(Dependencies.min_wait_period)
                #     else:
                #         break

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
        # Dependencies.add(name)
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
