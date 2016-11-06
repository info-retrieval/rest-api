from django.conf.urls import url

from .views import search_view, HomePageView, document_detail, list_view

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='index-view'),
    url(r'^search', search_view, name='search-view'),
    url(r'^list', list_view, name='list-view'),
    url(r'^document', document_detail, name='document-details')
]
