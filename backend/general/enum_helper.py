from django.utils.decorators import classproperty
from django.utils.translation import ugettext_lazy as _

from enum import Enum, unique


class BaseEnum(Enum):
    @classmethod
    def choices(cls):
        choices = list()
        for item in cls:
            choices.append((item.value, _(item.descriptive_name)))
        return tuple(choices)

    # string the name
    def __str__(self):
        return self.name

    # int the value
    def __int__(self):
        return self.value

    @classproperty
    def valid_values(cls):
        choices = list()
        for item in cls:
            choices.append(item.value)
        return tuple(choices)

    @property
    def descriptive_name(self):
        return self.name.replace('_', ' ').title()

    @classproperty
    def choices_dict(cls):
        choices = {}
        for item in cls:
            choices[item.value] = _(item.descriptive_name)
        return choices


@unique
class UserType(BaseEnum):
    ADMIN = 'A'
    RIDER = 'R'
    DRIVER = 'D'


@unique
class VerifyOTPType(BaseEnum):
    SIGNUP = 'SIGNUP'
    PASSWORD_RESET = 'PASSWORD_RESET'
