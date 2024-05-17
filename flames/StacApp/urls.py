from rest_framework import routers

from django.urls import path , include
from .views import StacViewSet,add_item_to_stac,SourceDataViewSet#,SourceDataViewSet,add_item_to_stac
from .views import search_catalog_common_metadata_api
from .views import (search_catalog_metadata_by_key_api,
                    sb_collection,
                    sb_publisher,
                    sb_minor,sb_grade,sb_place,sb_subminor,sb_year,
                    search_side_bar,
                    combined_response,
                    search_catalog_metadata_for_combined_response,
                    sb_subcollection)


router = routers.SimpleRouter()
router.register(r'stac', StacViewSet, basename='stac')
router.register(r'sourcedata', SourceDataViewSet,basename='SourceDataViewSet')
urlpatterns = [
    path('', include(router.urls)),
    path('add_item_to_stac/',add_item_to_stac),
    path('main_section_data/', search_catalog_common_metadata_api, name='search_catalog_common_metadata_api'),
    path('search_catalog_metadata_by_key_api/<str:key_to_search>/',search_catalog_metadata_by_key_api, name='search_catalog_metadata_by_key_api'),
    path('sb_collection/', sb_collection, name='sb_collection'),
    path('sb_subcollection/', sb_subcollection, name='sb_subcollection'),
    path('sb_minor/', sb_minor, name='sb_minor_pagination'), #/
    path('sb_subminor/', sb_subminor, name='sb_subminor'),   #/
    path('sb_grade/', sb_grade, name='sb_grade'),  #/
    path('sb_publisher/', sb_publisher, name='sb_publisher'), #/
    path('sb_place/', sb_place, name='sb_place'),  #/
    path('sb_year/', sb_year, name='sb_year'),  #/
    path('getside_searchdata/', search_side_bar, name='columnsearch'),
    path('meta_data_for_pagination/<str:query>/', combined_response, name='get_meta_data_with_pagination'), #/
    path('meta_data_for_pagination_wrongname/<str:query>/', search_catalog_metadata_for_combined_response, name='sb_year'),  #/
    ]