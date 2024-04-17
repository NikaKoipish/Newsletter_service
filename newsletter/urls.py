from django.urls import path
# from newsletter.views import pass
from newsletter.apps import NewsletterConfig
app_name = NewsletterConfig.name
urlpatterns = [
    # path('contacts/', index_contacts, name="index_contacts"),
    # path('', ProductListView.as_view(), name="index_home"),
    # path('<int:pk>/catalog/', ProductDetailView.as_view(), name="product"),

]