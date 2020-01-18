import inspect
from enum import EnumMeta, Enum

from django.utils.decorators import classproperty
from django.utils.functional import cached_property


class ChoiceEnumMeta(EnumMeta):
    def __new__(mcls, name, bases, namespace, **kwargs):
        if '__doc__' not in namespace:
            namespace['__doc__'] = cached_property(mcls.__value_doc__)
        return super().__new__(mcls, name, bases, namespace, **kwargs)

    def __repr__(cls):
        return '{classname}({choices})'.format(
            classname=cls.__name__,
            choices=str(cls.items())[1:-1],
        )

    def __value_doc__(cls):
        """
        Inspects your ChoiceEnum class
        taking inline comment near the enum value definition.

        :rtype: str | None
        :return: inline comment
        """
        doc = None

        module = inspect.getmodule(cls)
        lines_list, _ = inspect.getsourcelines(module)

        class_def = 'class {}'.format(cls.__class__.__name__)
        for i, line in enumerate(lines_list):
            if class_def in line:
                lines_list = lines_list[i:]
                break

        value_def = ' {} = {}'.format(cls.name, cls.value)
        for i, line in enumerate(lines_list):
            if value_def in line and '#' in line:
                _, inline_comment = line.split('#')
                doc = inspect.cleandoc(inline_comment)
                break

        return doc


class ChoiceEnum(Enum, metaclass=ChoiceEnumMeta):
    """
    Django models friendly Enum.

    Define your int choice field that's represented as str in the admin:
    ... class Email(models.Email):
    ...     email = models.EmailField()
    ...     email_type = models.IntegerField(
    ...         choices=EmailType.choices, null=True, blank=True)

    Example of usage:
    >>> class EmailType(ChoiceEnum):
    ...     other = 0
    ...     personal = 1    # for home
    ...     corporate = 2   # for work
    ...
    >>> EmailType
    EmailType(('other', 0), ('personal', 1), ('corporate', 2))

    Has dict-like "items" class method:
    >>> EmailType.items()
    [('other', 0), ('personal', 1), ('corporate', 2)]
    >>> dict(EmailType.items())
    {'other': 0, 'personal': 1, 'corporate': 2}

    Has "choices" class property:
    >>> EmailType.choices
    ((0, 'other'), (1, 'personal (for home)'), (2, 'corporate (for work)'))

    Multi type representation:
    >>> int(EmailType.personal)
    1
    >>> str(EmailType.personal)
    'personal'

    Is fully multi-type comparable:
    >>> EmailType.personal == 1
    True
    >>> EmailType.personal == 2
    False
    >>> EmailType.personal == 'personal'
    True
    >>> EmailType.personal == 'corporate'
    False
    >>> EmailType.personal == EmailType.personal
    True
    >>> EmailType.personal == EmailType.corporate
    False

    Takes inline comments as value docs:
    >>> EmailType.personal.__doc__
    'for home'
    >>> EmailType.corporate.__doc__
    'for work'

    """

    @classmethod
    def items(cls):
        items_list = [
            (item.name, item.value)
            for item in cls
        ]
        return items_list

    @classproperty
    def choices(cls):
        choices_tuple = tuple(
            (item.value, repr(item))
            for item in cls
        )
        return choices_tuple

    def __repr__(self):
        if self.__doc__:
            return f'{self.name} ({self.__doc__})'
        return self.name

    def __str__(self):
        return self.name

    def __int__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other
        if isinstance(other, str):
            return self.name == other
        return super().__eq__(other)
