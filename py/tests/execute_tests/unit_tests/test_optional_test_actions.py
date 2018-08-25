import pytest
from qaviton.utils.optional_test_action import Optional
from qaviton.utils import condition
from qaviton.utils import unique_id


@pytest.mark.parametrize('n', [0] * 20, ids=unique_id.id)
def test_optional(n):
    class Cat:
        def __init__(self, name):
            self.name = name
            self.optional = Optional()

        def meow(self):
            return self.name + ': meowww..'

        def growl(self):
            return self.name + ': KSSSSssss...'

        def jump(self, msg):
            return self.name + ': has jumped from {}'.format(msg)

        def fight_a_watermelon(self):
            r = [self.name + ': met a watermelon and decided to attack']
            for i in range(self.optional.number(chance=(3, 5))):
                if self.optional(chance=(1, 4)):
                    r.append(self.jump("a sudden blind attack"))
                elif self.optional(chance=(2, 5)):
                    r.append(self.meow())
                if self.optional(chance=(3, 4)):
                    r.append(self.growl())
                elif self.optional():
                    r.append(self.meow())
            return r

    perry = Cat('Perri')
    actions = perry.fight_a_watermelon()

    assert "Perri: met a watermelon and decided to attack" == actions[0]
    if len(actions) > 1:
        assert condition.any_in_any(("Perri: meowww..", "Perri: KSSSSssss...", "Perri: has jumped from a sudden blind attack"), actions)
