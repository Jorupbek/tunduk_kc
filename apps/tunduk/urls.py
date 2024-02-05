from django.urls import path

from .views import (TundukController,
                    InfocomRequestedList, InfocomRequestedDetail, UnaaRequestedList,
                    UnaaRequestedDetail, MinjystRequestedList, MinjystRequestedDetail,
                    KadastrRequestedDetail, KadastrRequestedList, PersonalInfo, MinSelXozRequestedList,
                    MinSelXozRequestedDetail)

app_name = 'tunduk'

urlpatterns = [
    path('', TundukController.as_view(),
         name='tunduk-controller'),
    path('tunduk-request/', PersonalInfo.as_view(),
         name='tunduk-request'),

    # Инфоком
    path('infocom-list/', InfocomRequestedList.as_view(),
         name='infocom-list'),
    path('infocom-request-detail/<int:year>/<int:month>/<int:pk>/<uuid:uuid>',
         InfocomRequestedDetail.as_view(),
         name='infocom-detail'),
    path('infocom-request/',
         InfocomRequestedDetail.as_view(),
         name='infocom-post'),

    # Унаа
    path('unaa-list/', UnaaRequestedList.as_view(),
         name='unaa-list'),
    path('unaa-detail/<int:year>/<int:month>/<int:pk>/<uuid:uuid>',
         UnaaRequestedDetail.as_view(),
         name='unaa-detail'),
    path('unaa-info/', UnaaRequestedDetail.as_view(),
         name='unaa-post'),

    # Министерство Юстиции
    path('minjyst-list/', MinjystRequestedList.as_view(),
         name='minjyst-list'),
    path('minjyst-detail/<int:year>/<int:month>/<int:pk>/<uuid:uuid>',
         MinjystRequestedDetail.as_view(),
         name='minjyst-detail'),
    path('minjyst-info/', MinjystRequestedDetail.as_view(),
         name='minjyst-post'),

    # Кадастр
    path('kadastr-list/', KadastrRequestedList.as_view(),
         name='kadastr-list'),
    path('kadastr-detail/<int:year>/<int:month>/<int:pk>/<uuid:uuid>',
         KadastrRequestedDetail.as_view(),
         name='kadastr-detail'),
    path('kadastr-info/', KadastrRequestedDetail.as_view(),
         name='kadastr-post'),

    # Мин сель хоз
    path('minselxoz-list/', MinSelXozRequestedList.as_view(),
         name='minselxoz-list'),
    path('minselxoz-detail/<int:year>/<int:month>/<int:pk>/<uuid:uuid>',
         MinSelXozRequestedDetail.as_view(),
         name='minselxoz-detail'),
    path('minselxoz-info/', MinSelXozRequestedDetail.as_view(),
         name='minselxoz-post'),
]
