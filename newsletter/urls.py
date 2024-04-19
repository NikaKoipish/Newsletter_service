from django.urls import path
from newsletter.views import Mail
from newsletter.views import MailListView
from newsletter.apps import NewsletterConfig
app_name = NewsletterConfig.name
urlpatterns = [
    # path('contacts/', index_contacts, name="index_contacts"),
    path('', MailListView.as_view(), name="mail_list"),
    # path('<int:pk>/catalog/', ProductDetailView.as_view(), name="product"),

]