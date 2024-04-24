from django.apps import AppConfig


class NewsListConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_list'



    def ready(self):
        import news_list.signals
