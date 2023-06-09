from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название страны')
    fullname = models.CharField(max_length=255, default='', verbose_name='Полное название страны')
    english = models.CharField(max_length=64, default='', verbose_name='Название страны на английском')
    id_country = models.CharField(max_length=2, default='', verbose_name='id страны, двухбуквенная система ISO Alpha2')
    country_code3 = models.CharField(max_length=3, default='', verbose_name='id страны, трёхбуквенная система ISO Alpha3')
    iso = models.IntegerField(default=0, verbose_name='Код  страны ISO numeric, трёхцифровая система')
    telcod = models.IntegerField(default=0, verbose_name='Телефонный код')
    telcod_len = models.IntegerField(default=0, verbose_name='Длина номера телефона')
    location = models.CharField(max_length=10, default='', verbose_name='Часть света')
    capital = models.CharField(max_length=255, default='', verbose_name='Столица')
    mcc = models.IntegerField(default=0, verbose_name='Код страны телефонных операторов')
    lang = models.CharField(max_length=64, default='', verbose_name='Оснвной язык')
    langcod = models.CharField(max_length=12, default='', verbose_name='Код языка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Занеесено в БД')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Страна(ы)'
        verbose_name_plural = 'Страны'
        ordering = ['-created_at']


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT, verbose_name='Страна')
    name = models.CharField(max_length=64, verbose_name='Название города')
    area = models.IntegerField(default=0, verbose_name='Область')
    telcod = models.CharField(max_length=10, default='', verbose_name='Телефонные коды')
    latitude = models.CharField(max_length=15, null=True, blank=True, verbose_name='Широта')
    longitude = models.CharField(max_length=15, null=True, blank=True, verbose_name='Долгота')
    time_zone = models.IntegerField(default=0, verbose_name='Часовой пояс')
    tz = models.CharField(max_length=64, verbose_name='Часовой пояс, буквенное обозначение')
    english = models.CharField(max_length=64, blank=True, verbose_name='Название города на английском')
    rajon = models.IntegerField(default=0, verbose_name='Район области')
    sub_rajon = models.IntegerField(default=0, verbose_name='Подрайон в райне')
    iso = models.CharField(max_length=3, verbose_name='id города, трёхбуквенная система ISO Alpha3')
    vid = models.IntegerField(default=0, verbose_name='1-город, 2-поселок, 3-село, 4-деревня, 5-станица, 6-хутор')
    post = models.CharField(max_length=256, default='', verbose_name='Почтовый код')
    wiki = models.CharField(max_length=1024, default='', verbose_name='Cсылка на wikipedia без https://')
    full_english = models.CharField(max_length=100, verbose_name='Название города на английском')
    full_name = models.CharField(max_length=100, verbose_name='Полное название города')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Занеесено в БД')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Город(а)'
        verbose_name_plural = 'Города'
        ordering = ['-created_at']
