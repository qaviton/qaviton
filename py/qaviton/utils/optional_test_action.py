import random
from qaviton.utils.random_util import random_number


class Optional:
    """ use this object to insert random behavior on none mandatory operations for exploratory testing.
        example:

            class Cat:
                def __init__(self, name):
                    self.name = name
                    self.optional = Optional()

                def meow(self):
                    print(self.name + ': meowww..')

                def growl(self):
                    print(self.name + ': KSSSSssss...')

                def jump(self, msg):
                    print(self.name + ': has jumped from {}'.format(msg))

                def fight_a_watermelon(self):
                    print(self.name + ': met a watermelon and decided to attack')
                    for i in range(self.optional.number(chance=(3, 5))):
                        if self.optional(chance=(1, 4)):
                            self.jump("a sudden blind attack")
                        elif self.optional(chance=(2, 5)):
                            self.meow()
                        if self.optional(chance=(3, 4)):
                            self.growl()
                        elif self.optional():
                            self.meow()

            perry = Cat('Perri') # by the way she was my favorite cat
            perry.fight_a_watermelon()
    """

    def __init__(self, chance=(1, 2), optional_state=True, mandatory=False):
        self.chance = chance
        self.optional_state = optional_state
        self.mandatory = mandatory

    def __call__(self, chance=None, optional_state=None, mandatory=None):
        """
        call this object to run an optional command
        :param chance: tuple of int pair: (1, 2) -> 1:2
        :type chance: (int, int)
        :param optional_state: boolean
        :param mandatory: boolean
        :return: boolean
        """
        if mandatory is None:
            mandatory = self.mandatory
        if mandatory is True:
            return True

        if optional_state is None:
            optional_state = self.optional_state
        if optional_state is False:
            return False

        if chance is None:
            chance = self.chance
        if chance == 0:
            return False

        if optional_state is True:
            if random.random() < chance[0]/chance[1]:
                return True
            else:
                return False
        return False

    def number(self, chance=None, optional_state=None, mandatory=None):
        """ optionally return a random number from chance
        if option is dismissed return value is 0
        if option is mandatory return value is either 1 or highest value
        :param chance: tuple of int pair: (1, 2) -> 1:2
        :type chance: (int, int)
        :param optional_state: boolean
        :param mandatory: boolean
        :rtype: int
        """
        if mandatory is None:
            mandatory = self.mandatory

        if optional_state is None:
            optional_state = self.optional_state
        elif optional_state is False:
            if mandatory is True:
                optional_state = True
            else:
                return 0

        if chance is None:
            chance = self.chance
        if chance[1] == 0:
            if mandatory is True:
                return 1
            else:
                return 0

        if optional_state is True:
            if mandatory is True:
                return chance[1]
            else:
                return random_number(*chance)
        return 0
