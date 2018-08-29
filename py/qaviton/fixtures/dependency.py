import pytest
from qaviton.exceptions import DependencyException


class Depend:
    def __init__(self, dependencies: dict, request):
        self.dependencies = dependencies
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
            if dependency in self.dependencies.keys():
                if self.dependencies[dependency] is None:
                    raise DependencyException("Test dependency {} has not yet finished running.\n"
                                              "please consider using pytest-ordering.\n"
                                              "more info at: https://github.com/ftobia/pytest-ordering"
                                              .format(self.dependencies[dependency]))
                elif self.dependencies[dependency] == 1:
                    self.behave_when_dependency_fails("Test dependency {} failed".format(dependency))
                elif self.dependencies[dependency] == 2:
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
            for dependency in self.dependencies.keys():
                if pattern in dependency or pattern == dependency:
                    pattern_found = True
                    if self.dependencies[dependency] is None:
                        raise DependencyException("Test dependency {} has not yet finished running.\n"
                                                  "please consider using pytest-ordering.\n"
                                                  "more info at: https://github.com/ftobia/pytest-ordering".
                                                  format(self.dependencies[dependency]))
                    elif self.dependencies[dependency] == 1:
                        self.behave_when_dependency_fails("Test dependency {} failed".format(dependency))
                    elif self.dependencies[dependency] == 2:
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
            for dependency in self.dependencies.keys():
                if pattern == dependency.split("[")[0]:
                    pattern_found = True
                    if self.dependencies[dependency] is None:
                        raise DependencyException("Test dependency {} has not yet finished running.\n"
                                                  "please consider using pytest-ordering.\n"
                                                  "more info at: https://github.com/ftobia/pytest-ordering".
                                                  format(self.dependencies[dependency]))
                    elif self.dependencies[dependency] == 1:
                        self.behave_when_dependency_fails("Test dependency {} failed".format(dependency))
                    elif self.dependencies[dependency] == 2:
                        self.behave_when_dependency_is_skipped("Test dependency {} skipped".format(dependency))
            if pattern_found is False:
                raise DependencyException(
                    "Test dependency with pattern {}[ is either missing or miss-ordered.\n"
                    "In the miss-ordered case please consider reordering your tests with pytest-ordering.\n"
                    "more info at: https://github.com/ftobia/pytest-ordering"
                    .format(pattern))


@pytest.fixture(scope='package')
def dependencies():
    return {}


@pytest.fixture()
def dependency(dependencies, request):
    dependencies[request.node.name] = None
    yield
    if request.node.rep_setup.failed:
        dependencies[request.node.name] = 1
    elif request.node.rep_setup.skipped:
        dependencies[request.node.name] = 2
    else:
        if request.node.rep_call.failed:
            dependencies[request.node.name] = 1
        elif request.node.rep_call.skipped:
            dependencies[request.node.name] = 2
        else:
            dependencies[request.node.name] = 0


@pytest.fixture()
def depend(dependencies, request):
    return Depend(dependencies, request)
