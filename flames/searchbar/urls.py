from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from .views import DownloadDetailsCreateView
from .views import (global_search_by_key,search_side_bar,download_image,
                download_im,main_section_data,sb_collection,sb_minor,sb_subminor,sb_grade,sb_publisher,
                sb_place,sb_year,main_section_data_meta_data,sb_subcollection,
                global_search_for_meta_data_by_key,pagination_of_global_search,
                pagination_if_main_search,get_meta_data_with_pagination,DetailsViewSet)

router = routers.SimpleRouter()

router.register('adddetails', DetailsViewSet)

urlpatterns = [
    path('', include(router.urls)), 
    path('global_search_by_key/<str:query>', views.global_search_by_key, name='search'),#/
    path('getside_searchdata/', views.search_side_bar, name='columnsearch'),
    path('Downloadim/<str:file_name>',download_im),
    path('download_data/',download_image),
    path('main_section_data/',main_section_data),   #/
    path('sb_collection/', sb_collection, name='sb_collection'),
    path('sb_minor/', sb_minor, name='sb_minor_pagination'), #/
    path('sb_subminor/', sb_subminor, name='sb_subminor'),   #/
    path('sb_grade/', sb_grade, name='sb_grade'),  #/
    path('sb_publisher/', sb_publisher, name='sb_publisher'), #/
    path('sb_place/', sb_place, name='sb_place'),  #/
    path('sb_year/', sb_year, name='sb_year'),  #/
    path('meta_data/<str:query>', main_section_data_meta_data, name='main_section_data_meta_data'),
    path('sb_subcollection/', sb_subcollection, name='sb_subcollection'), #/


    path('global_search_by_meta_key/<str:query>', views.global_search_for_meta_data_by_key, name='global_search_for_meta_data_by_key'),

    path('download_details/', DownloadDetailsCreateView.as_view(), name='download-details-create'),
   # path('sb_collection/<?selectedItems={value1}>',sb_collection),

   path('pagination_global_search_by_query/<str:query>/',pagination_of_global_search), #/
   path('pagination_main_search/',pagination_if_main_search),  #/
   path('meta_data_for_pagination/<str:query>/', get_meta_data_with_pagination, name='get_meta_data_with_pagination'), #/
   
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


