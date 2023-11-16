from django import forms
from django.db.models import Q

from listings.models import MassageFor, Feature
from tantrakazan.utils import Locator


class PersonDataForm(forms.Form):
    first_name = forms.CharField(label='Имя', required=False, widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', required=False, widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Фамилия'}))
    gender = forms.NullBooleanField(label='Пол', widget=forms.Select(attrs={'class': 'form__input'},
                                                                     choices=(
                                                                         (None, 'Укажите свой пол'), (True, 'Мужчина'),
                                                                         (False, 'Женщина'))))
    birth_date = forms.DateField(label='Дата рождения', required=False,
                                 widget=forms.DateInput(attrs={'type': 'date', 'class': 'form__input'}))
    height = forms.IntegerField(required=False, label='Рост', widget=forms.NumberInput(attrs={'class': 'form__input'}))
    weight = forms.IntegerField(required=False, label='Вес', widget=forms.NumberInput(attrs={'class': 'form__input'}))


class SpecialistDataForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['massage_for'].choices = MassageFor.objects.values_list('pk', 'massage_for')

    massage_for = forms.MultipleChoiceField(label='Для кого вы делаете массаж',
                                            required=False,
                                            widget=forms.CheckboxSelectMultiple(),
                                            )
    practice_start_date = forms.DateField(label='Дата начала практики', required=False,
                                          widget=forms.DateInput(
                                              attrs={'type': 'date', 'class': 'form__input'}))

    home_price = forms.IntegerField(label='Цена базовой программы дома, ₽',
                                    widget=forms.NumberInput(attrs={'class': 'form__input'}))
    on_site_price = forms.IntegerField(label='Цена базовой программы с выездом, ₽',
                                       widget=forms.NumberInput(attrs={'class': 'form__input'}))


class AboutForm(forms.Form):
    description = forms.CharField(required=False, label='О себе', widget=forms.TextInput(
        attrs={'class': 'form__input--textarea mb--30'}))


class ContactDataForm(forms.Form):
    address = forms.CharField(required=False, label='Адрес', widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Адрес: Улица, д. ХХ', 'id': 'addressInput'}))
    phone_number = forms.CharField(required=False, label='Телефон', widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Телефон'}))
    telegram_profile = forms.CharField(required=False, label='Телеграм', widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Телеграм'}))
    instagram_profile = forms.CharField(required=False, label='Инстаграм', widget=forms.TextInput(
        attrs={'class': 'form__input', 'placeholder': 'Инстаграм'}))

    def clean(self):
        cleaned_data = super().clean()
        address = cleaned_data['address']
        if address:
            raw_address = 'Казань, ' + cleaned_data['address']
            place = Locator(raw_place=raw_address)
            cleaned_data['address'] = place.location
            cleaned_data['latitude'] = place.location.point.latitude
            cleaned_data['longitude'] = place.location.point.longitude
        return cleaned_data


class ActivateProfileForm(forms.Form):
    is_profile_active = forms.BooleanField(required=False)


price_range = {'low': (1000, 3000), 'medium': (3000, 7000), 'high': (7000, 20000)}
ORDERINGS = (('-rating__average', 'Рейтинг'),
             ('min_price', '<i class="fa fa-arrow-up" aria-hidden="true">Цена</i>'),
             ('-min_price', '<i class="fa fa-arrow-down" aria-hidden="true">Цена</i>'),
             ('-therapist_profile__birth_date', '<i class="fa fa-arrow-up" aria-hidden="true">Возраст</i>'),
             ('therapist_profile__birth_date', '<i class="fa fa-arrow-down" aria-hidden="true">Возраст</i>'),
             ('therapist_profile__practice_start_date', 'Опыт'),
             ('-rating__count', 'Количество отзывов'),
             ('-date_joined', 'Сначала новые'))


class SpecialistFilterForm(forms.Form):
    gender = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=[(True, 'Мужчина'), (False, 'Женщина')],
    )

    massage_for = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=MassageFor.objects.values_list('slug', 'massage_for')
        # TODO: так нельзя оставлять. сломается при сносе бд
    )
    price = forms.ChoiceField(required=False,
                              widget=forms.RadioSelect,
                              choices=[(key, f'₽{price_range[key][0]} - ₽{price_range[key][1]}') for key in price_range]
                              )

    order_by = forms.ChoiceField(
        required=False,
        label='',
        widget=forms.Select(attrs={'class': 'product-ordering__select nice-select'}),
        choices=ORDERINGS
    )

    def get_query_params(self):
        query_params = {}
        for key, value in self.cleaned_data.items():
            if value:
                query_params[key] = value
        return query_params

    def filter(self, queryset):
        genders = self.cleaned_data.get('gender') or [True, False]
        massage_for = self.cleaned_data.get('massage_for') or ['for_males', 'for_females', 'for_pairs']
        price = self.cleaned_data.get('price')
        queryset = (queryset.
                    filter(
                            therapist_profile__gender__in=genders,
                            therapist_profile__massage_for__slug__in=massage_for
                            )
                    .distinct())
        if price:
            price_filter = Q(min_price__gte=price_range[price][0], min_price__lte=price_range[price][1])
            queryset = queryset.filter(price_filter)
        ordering = self.cleaned_data.get('order_by')

        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset


class FeaturesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        features = Feature.objects.values_list('id', 'name')
        for massage_for_id, massage_for_name in features:
            field_name = f'feature_{massage_for_id}'
            self.fields[field_name] = forms.BooleanField(
                required=False,
                label=massage_for_name,
                widget=forms.CheckboxInput()
            )


class OrderingForm(forms.Form):
    order_by = forms.ChoiceField(
        label='',
        widget=forms.Select(attrs={'class': 'product-ordering__select nice-select'}),
        choices=ORDERINGS
    )
