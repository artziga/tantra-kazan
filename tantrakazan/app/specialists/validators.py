from django.core.exceptions import ValidationError


def validate_phone_number(value: str):
    print(value, 2)
    signs_to_remove = (' ', '-')
    for s in signs_to_remove:
        value = value.replace(s, '')
    print(value)
    if value.startswith('+7'):
        if len(value) == 12:
            return
    elif value.startswith('8'):
        if len(value) == 11:
            return
    else:
        raise ValidationError('Введите верный номер')
    raise ValidationError('Неверны формат номера')
