from django.contrib import admin
from .models import Countries, Cities



class CountriesAdmin(admin.ModelAdmin):
    save_as = True      #позвоялет сохранить состояние введенной ранее новости
    save_on_top = True  #дублирует панель сохранения в вверх
    list_display = ('id', 'name', 'fullname', 'english', 'id_country', 'country_code3', 'iso', 'telcod', 'telcod_len', 'location', 'capital', 'mcc', 'lang', 'langcod', 'time_zone', 'tz', 'created_at')
    list_display_links = ('id', 'name')
    list_editable = ('fullname', 'english', 'id_country', 'country_code3', 'iso', 'telcod', 'telcod_len', 'location', 'capital', 'mcc', 'lang', 'langcod', 'time_zone', 'tz')    #отвечает за возможность редактирования поля прямо в таблице админки 
    search_fileds = ('name', 'fullname',)
    list_filter = ('name', 'fullname', 'id_country', 'country_code3', 'iso', 'created_at')
    readonly_fields = ('created_at',)
    fields = ('name', 'fullname', 'english', 'id_country', 'country_code3', 'iso', 'telcod', 'telcod_len', 'location', 'capital', 'mcc', 'lang', 'langcod', 'time_zone', 'tz', 'created_at')
    # list_select_related = []    #оптимизирует запросы, создавая JOIN'ы

class CitiesAdmin(admin.ModelAdmin):
    save_as = True      #позвоялет сохранить состояние введенной ранее новости
    save_on_top = True  #дублирует панель сохранения в вверх
    list_display = ('id', 'country', 'name', 'area', 'telcod', 'latitude', 'longitude', 'time_zone', 'tz', 'english', 'rajon', 'sub_rajon', 'iso', 'vid', 'post', 'wiki', 'full_english', 'full_name', 'created_at')
    list_display_links = ('id', 'name')
    list_editable = ('country', 'area', 'telcod', 'latitude', 'longitude', 'time_zone', 'tz', 'english', 'rajon', 'sub_rajon', 'iso', 'vid', 'post', 'wiki', 'full_english', 'full_name')    #отвечает за возможность редактирования поля прямо в таблице админки 
    search_fileds = ('name', 'fullname',)
    list_filter = ('name', 'full_name', 'time_zone', 'created_at')
    readonly_fields = ('created_at',)
    fields = ('country', 'name', 'area', 'telcod', 'latitude', 'longitude', 'time_zone', 'tz', 'english', 'rajon', 'sub_rajon', 'iso', 'vid', 'post', 'wiki', 'full_english', 'full_name', 'created_at')


admin.site.register(Countries, CountriesAdmin)
admin.site.register(Cities, CitiesAdmin)   #регистрация приложения в проекте
