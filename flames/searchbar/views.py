from django.shortcuts import render

# Create your views here.
from django.db import connection
from django.http import JsonResponse
from rest_framework.decorators import api_view  
from rest_framework.response import Response
from django.http import HttpResponse, FileResponse
from rest_framework.views import APIView
from .serializers import DownloadDetailsSerializer
from rest_framework import viewsets
from .models import Downloads,data

class DownloadDetailsCreateView(APIView):
    def post(self, request, format=None):
        serializer = DownloadDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



def global_search_by_key(request,query):
       
    with connection.cursor() as cursor:
        words = query.split()
        tsquery = ' | '.join(words)
        cursor.execute("""
            SELECT *
            FROM searchbar_data
               WHERE to_tsvector(searchbar_data."major" || ' ' ||searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor" 
            || ' ' || searchbar_data."grade"|| ' ' || searchbar_data."file_formats"|| ' ' || searchbar_data."type"|| ' ' || searchbar_data."source_description"
            || ' ' || searchbar_data."place_city"|| ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
            || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
            || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr" 
            || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
            || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
             || ' ' || searchbar_data."thumbnail") @@ to_tsquery( %s)
        """, [tsquery])
        rows = cursor.fetchall()
        data = {'data': [{ "id": row[0],
                        'Major': row[1],
                    'Submajor': row[2],
                    'Minor': row[3],
                    'SubMinor': row[4],
                    'Grade': row[5],
                    'File_formats': row[6],
                    'Type': row[7],
                    'Source_Description': row[8],
                    'Place_City': row[9],
                    'Year': row[10],
                    'Publisher': row[11],
                    'Path': row[12],
                    'Collection': row[13],
                    'Collection_type': row[14],
                    'SOI_toposheet_no': row[15],
                    'Data_Resolution': row[16],
                    'Ownership': row[17],
                    'is_processed': row[18],
                    'short_descr': row[19],
                    'descr': row[20],
                    'img_service': row[21],
                    'img_dw': row[22],
                    'map_service': row[23],
                    'map_dw': row[24],
                    'publish_on': row[25],
                    'thumbnail': row[26],
                    'source': row[27]} for row in rows]}
    return JsonResponse(data)
    

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpRequest

def global_search_for_meta_data_by_key(request, query):

    
    
    with connection.cursor() as cursor:
        words = query.split()
        tsquery = ' | '.join(words)
        cursor.execute("""
            SELECT *
            FROM searchbar_data
            WHERE to_tsvector(searchbar_data."major" || ' ' || searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor" 
            || ' ' || searchbar_data."grade" || ' ' || searchbar_data."file_formats" || ' ' || searchbar_data."type" || ' ' || searchbar_data."source_description"
            || ' ' || searchbar_data."place_city" || ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
            || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
            || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr" 
            || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
            || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
            || ' ' || searchbar_data."thumbnail") @@ to_tsquery( %s)
        """, [tsquery])
        rows = cursor.fetchall()
        data = {
            'data': [
                {
                    "id": row[0],
                    'Major': row[1],
                    'Submajor': row[2],
                    'Minor': row[3],
                    'SubMinor': row[4],
                    'Grade': row[5],
                    'File_formats': row[6],
                    'Type': row[7],
                    'Source_Description': row[8],
                    'Place_City': row[9],
                    'Year': row[10],
                    'Publisher': row[11],
                    'Path': row[12],
                    'Collection': row[13],
                    'Collection_type': row[14],
                    'SOI_toposheet_no': row[15],
                    'Data_Resolution': row[16],
                    'Ownership': row[17],
                    'is_processed': row[18],
                    'short_descr': row[19],
                    'descr': row[20],
                    'img_service': row[21],
                    'img_dw': row[22],
                    'map_service': row[23],
                    'map_dw': row[24],
                    'publish_on': row[25],
                    'thumbnail': row[26],
                    'source': row[27]
                } 
                for row in rows
            ]
        }
        
    search_results = {'data': rows}

    return Response(search_results)

    
    


def search_new1(request):
       with connection.cursor() as cursor:
        cursor.execute('''
            SELECT
                CASE
                    
                    WHEN submajor IS NOT NULL THEN 'submajor'
                    WHEN major IS NOT NULL THEN 'major'
                    WHEN minor IS NOT NULL THEN 'minor'
                    WHEN subminor IS NOT NULL THEN 'subminor'
                    ELSE NULL
                END AS head,
                submajor AS subhead,
                COUNT(*) AS count
            FROM
                searchbar_data
            GROUP BY
                head, subhead;
        ''')
        rows = cursor.fetchall()
        print(rows)
        
        data = {}
        for row in rows:
            head = row[0]
            subhead = row[1]
            count = row[2]
            
            if head not in data:
                data[head] = []
                
            data[head].append({'subhead': subhead, 'count': count})
        
        # Duplicate the 'major' data under 'submajor' key
        if 'major' in data and 'submajor' not in data:
            data['submajor'] = data['major']
        
        print(data)
        search_new1()
        return JsonResponse(data)







# def search_side_bar(request):
#    with connection.cursor() as cursor:
#         cursor.execute('''
#         SELECT
#             CASE
#                 WHEN major IS NOT NULL THEN 'major'
#                 WHEN submajor IS NOT NULL THEN 'submajor'
#                 WHEN minor IS NOT NULL THEN 'minor'
#                 WHEN subminor IS NOT NULL THEN 'subminor'
#                 WHEN grade IS NOT NULL THEN 'grade'
#                 WHEN grade IS NOT NULL THEN 'publisher'
#                 WHEN place_city IS NOT NULL THEN 'place_city'
#                 WHEN grade IS NOT NULL THEN 'grade'
#                 WHEN year IS NOT NULL THEN 'year'
#                 ELSE NULL
#             END AS head,
#             submajor AS subhead,
#             COUNT(*) AS count
        # FROM
        #     data
        # GROUP BY
        #     head, subhead;
        # ''')
        # rows = cursor.fetchall()
        # print(rows)

        # data = {}
        # for row in rows:
        #     head = row[0]
        #     subhead = row[1]
        #     count = row[2]

        #     if head not in data:
        #         data[head] = []

        #     data[head].append({'subhead': subhead, 'count': count})

        # # Duplicate the 'major' data under 'submajor' key
        # if 'major' in data and 'submajor' not in data:
        #     data['submajor'] = data['major']

        # # Add 'minor' as a head and return 'minor' under subheads
        # if 'minor' not in data:
        #     data['minor'] = data['major']
        
        # # Add 'minor' as a head and return 'minor' under subheads
        # if 'subminor' not in data:
        #     data['subminor'] = data['major']
        
        # # Add 'minor' as a head and return 'minor' under subheads
        # if 'grade' not in data:
        #     data['grade'] = data['major']
        
        
        # if 'publisher' not in data:
        #     data['publisher'] = data['major']
        
        # if 'place_city' not in data:
        #     data['place_city'] = data['major']
        
        # if 'year' not in data:
        #     data['year'] = data['major']
            

        # print(data)
        # return JsonResponse(data)



@api_view(['GET'])   
def download_image(request):     
    file_name = f'PM.pdf'
    output_path = f'media/PM.pdf'
    if file_name:
        http = 'https' if request.is_secure() else 'http'
        pdf_url = f'{http}://{request.get_host()}/download_data/{file_name}'
    else:
        pdf_url = 'File Not found'
     # give pdf url to download path
    response = pdf_url
#return Response(response)
    return Response(response)

def download_im(request, file_name):
    file_path = f"media/{file_name}"
   # with codecs.open(file_path, 'r',encoding="utf8",errors='ignore') as f:            
    response = FileResponse(open(file_path,'rb'))
    #response = FileResponse(file_data, as_attachment=True,                              
    return response


@api_view(['GET'])
def main_section_data(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT *
            FROM searchbar_data
            ORDER BY (searchbar_data."created_date" IS NULL),searchbar_data."created_date" DESC
        """)
        rows = cursor.fetchall()
        data = {'data': [{'Major': row[0],  'Submajor': row[1],'Minor': row[2],
                'SubMinor': row[3],'Grade': row[4],'File_formats': row[5],'Type': row[6],
                'Source_Description': row[7],'Place_City': row[8],'Year': row[9],
                'Publisher': row[10],'Path': row[11],'Collection': row[12],'Collection_type': row[13],
                'SOI_toposheet_no':row[14],'Data_Resolution': row[15],'Ownership': row[16],
                'is_processed': row[17],'short_descr': row[18],'descr': row[21],'img_service': row[22],
                'img_dw': row[22],'map_service': row[24],'map_dw': row[24],'publish_on': row[25],
                'thumbnail': row[26],'source': row[27],'created_date': row[28]} for row in rows]}
    return JsonResponse(data)




def search_side_bar(request):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT 'major' AS type, COALESCE(major) AS subhead, COUNT(*) AS count
            FROM searchbar_data
            WHERE major IS NOT NULL
            AND major <> ''
            GROUP BY COALESCE(major)
            UNION ALL
            
            SELECT 'submajor' AS type, COALESCE(submajor) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
            WHERE major IS NOT NULL
            AND submajor <> ''
            GROUP BY COALESCE(submajor)
            UNION ALL
            
            SELECT 'minor' AS type, COALESCE(minor) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
			WHERE minor IS NOT NULL
            AND minor <> ''
            GROUP BY COALESCE(minor)
            UNION ALL
            
            SELECT 'subminor' AS type, COALESCE(subminor) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
			WHERE subminor IS NOT NULL
            AND subminor <> ''
            GROUP BY COALESCE(subminor)
            UNION ALL
            
            SELECT 'grade' AS type, COALESCE(grade) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
			WHERE grade IS NOT NULL
            AND grade <> ''
            GROUP BY COALESCE(grade)
            UNION ALL
            
            
            SELECT 'publisher' AS type, COALESCE(publisher) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
			WHERE publisher IS NOT NULL
            AND publisher <> ''
            GROUP BY COALESCE(publisher)
            UNION ALL
            
            SELECT 'place_city' AS type, COALESCE(place_city) AS subhead, COUNT(*) AS count
            FROM searchbar_data 
			WHERE place_city IS NOT NULL
            AND place_city <> ''
            GROUP BY COALESCE(place_city)
            UNION ALL
            
            SELECT 'year' AS type, COALESCE(year) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
			WHERE year IS NOT NULL
            AND year <> ''
            GROUP BY COALESCE(year)
           
        ''')
        rows = cursor.fetchall()
        data = {
            'major': [],
            'submajor': [],
             'minor': [],
             'subminor': [],
             'grade':[],
             'publisher':[],
             'place_city':[],
             'year':[]
        }
        
        for row in rows:
            item = {
                'subhead': row[1],
                'count': row[2]
            }
            
            if row[0] == 'major':
                data['major'].append(item)
            elif row[0] == 'submajor':
                data['submajor'].append(item)
            elif row[0] == 'minor':
                data['minor'].append(item)
            elif row[0] == 'subminor':
                data['subminor'].append(item)
            elif row[0] == 'grade':
                data['grade'].append(item)
            elif row[0] == 'publisher':
                data['publisher'].append(item)
            elif row[0] == 'place_city':
                data['place_city'].append(item)
            elif row[0] == 'year':
                data['year'].append(item)
            
        
        return JsonResponse(data)



def sb_collection(request):
    query_params = request.GET.getlist('selectedItems')
    key_list = [param.replace('%20', ' ') for param in query_params]
    print("  @ DATA FOR KEY_LIST @",key_list)
    limit = int(request.GET.get('limit', 10))  # Default limit is 10
    offset = int(request.GET.get('offset', 0))  # Default offset is 0

    query = """
        SELECT *
        FROM searchbar_data """

    count_query = """
        SELECT COUNT(*)
        FROM searchbar_data """

    conditions = []
    for key in key_list:
        conditions.append("""to_tsvector(searchbar_data."id"|| ' ' ||searchbar_data."major" || ' ' ||searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor"
            || ' ' || searchbar_data."grade"|| ' ' || searchbar_data."file_formats"|| ' ' || searchbar_data."type"|| ' ' || searchbar_data."source_description"
            || ' ' || searchbar_data."place_city"|| ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
            || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
            || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr"
            || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
            || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
            || ' ' || searchbar_data."thumbnail") @@ plainto_tsquery(%s)""")

    if conditions:
        query += " WHERE " + " OR ".join(conditions)
        count_query += " WHERE " + " OR ".join(conditions)

    query += f" LIMIT {limit} OFFSET {offset}"

    with connection.cursor() as cursor:
        # Execute the main query
        cursor.execute(query, key_list)
        rows = cursor.fetchall()
        print(" print data for cultural heritage",rows)
        data = {
            'data': [
               {    'id': row[0],
                    'Major': row[1],
                    'Submajor': row[2],
                    'Minor': row[3],
                    'SubMinor': row[4],
                    'Grade': row[5],
                    'File_formats': row[6],
                    'Type': row[7],
                    'Source_Description': row[8],
                    'Place_City': row[9],
                    'Year': row[10],
                    'Publisher': row[11],
                    'Path': row[11],
                    'Collection': row[12],
                    'Collection_type': row[13],
                    'SOI_toposheet_no': row[14],
                    'Data_Resolution': row[15],
                    'Ownership': row[16],
                    'is_processed': row[17],
                    'short_descr': row[18],
                    'descr': row[21],
                    'img_service': row[20],
                    'img_dw': row[22],
                    'map_service': row[24],
                    'map_dw': row[23],
                    'publish_on': row[24],
                    'thumbnail': row[25],
                    'source': row[28],
                    'created_date': row[30]
                }
                for row in rows
            ]
        }
# Execute the count query to get the total count of matching records
        cursor.execute(count_query, key_list)
        count = cursor.fetchone()[0]
        data['count'] = count

       

    return JsonResponse(data)

    return JsonResponse(data)

# def sb_collection(request):
#     query_params = request.GET.getlist('selectedItems')
#     key_list = [param.replace('%20', ' ') for param in query_params]
#     print("  @ DATA FOR KEY_LIST @", key_list)
#     limit = int(request.GET.get('limit', 10))  # Default limit is 10
#     offset = int(request.GET.get('offset', 0))  # Default offset is 0

#     query = """
#         SELECT *
#         FROM data 
#     """

#     count_query = """
#         SELECT COUNT(*)
#         FROM data 
#     """

#     conditions = []
#     for key in key_list:
#         conditions.append("""to_tsvector(data."major" || ' ' || data."submajor" || ' ' || data."minor" || ' ' || data."subminor"
#             || ' ' || data."grade" || ' ' || data."file_formats" || ' ' || data."type" || ' ' || data."source_description"
#             || ' ' || data."place_city" || ' ' || data."year" || ' ' || data."publisher" || ' ' || data."path"
#             || ' ' || data."collection" || ' ' || data."collection_type" || ' ' || data."soi_toposheet_no" || ' ' || data."data_resolution"
#             || ' ' || data."ownership" || ' ' || data."is_processed" || ' ' || data."short_descr"
#             || ' ' || data."descr" || ' ' || data."img_service" || ' ' || data."img_dw"
#             || ' ' || data."map_service" || ' ' || data."map_dw" || ' ' || data."publish_on"
#             || ' ' || data."thumbnail") @@ plainto_tsquery(%s)""")

#     if conditions:
#         query += " WHERE " + " OR ".join(conditions)
#         count_query += " WHERE " + " OR ".join(conditions)

#     query += f" LIMIT {limit} OFFSET {offset}"

#     with connection.cursor() as cursor:
#         # Execute the main query
#         cursor.execute(query, key_list)
#         rows = cursor.fetchall()
#         print("Print data for Cultural Heritage:", rows)
        
#         data = {
#             'data': [
#                 {
#                     'Major': row[1],              # Corrected index from 1 to 0
#                     'Submajor': row[1],           # Corrected index from 1 to 0
#                     'Minor': row[2],
#                     'SubMinor': row[3],
#                     'Grade': row[4],
#                     'File_formats': row[5],
#                     'Type': row[6],
#                     'Source_Description': row[7],
#                     'Place_City': row[8],         # Corrected index from 9 to 8
#                     'Year': row[9],               # Corrected index from 10 to 9
#                     'Publisher': row[10],         # Corrected index from 11 to 10
#                     'Path': row[11],
#                     'Collection': row[12],
#                     'Collection_type': row[13],
#                     'SOI_toposheet_no': row[14],
#                     'Data_Resolution': row[15],
#                     'Ownership': row[16],
#                     'is_processed': row[17],
#                     'short_descr': row[18],
#                     'descr': row[19],             # Corrected index from 21 to 19
#                     'img_service': row[20],
#                     'img_dw': row[21],            # Corrected index from 22 to 21
#                     'map_service': row[22],       # Corrected index from 24 to 22
#                     'map_dw': row[23],            # Corrected index from 23 to 22
#                     'publish_on': row[24],        # Corrected index from 24 to 22
#                     'thumbnail': row[25],
#                     'source': row[26],            # Corrected index from 28 to 26
#                     'created_date': row[27]       # Corrected index from 29 to 27
#                 }
#                 for row in rows
#             ]
#         }

#         # Execute the count query to get the total count of matching records
#         cursor.execute(count_query, key_list)
#         count = cursor.fetchone()[0]
#         data['count'] = count

#     return JsonResponse(data)




    
                          
                            
                            
                            

        
                    



def sb_minor(request):
    query_params = request.GET.getlist('selectedItems')
    key_list = [param.replace('%20', ' ') for param in query_params]

    limit = int(request.GET.get('limit', 10))
    offset = int(request.GET.get('offset', 0))

    query = """
        SELECT *
        FROM searchbar_data"""

    count_query = """
        SELECT COUNT(*)
        FROM searchbar_data"""

    conditions = []
    for key in key_list:
        conditions.append("""to_tsvector(searchbar_data."id" || ' ' ||searchbar_data."major" || ' ' ||searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor"
            || ' ' || searchbar_data."grade"|| ' ' || searchbar_data."file_formats"|| ' ' || searchbar_data."type"|| ' ' || searchbar_data."source_description"
            || ' ' || searchbar_data."place_city"|| ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
            || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
            || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr"
            || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
            || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
            || ' ' || searchbar_data."thumbnail") @@ plainto_tsquery(%s)""")

    if conditions:
        query += " WHERE " + " OR ".join(conditions)
        count_query += " WHERE " + " OR ".join(conditions)

    query += f" LIMIT {limit} OFFSET {offset}"
    with connection.cursor() as cursor:
        cursor.execute(query, key_list)
        rows = cursor.fetchall()
        data = {'data': [{
                    'id':row[0],
                    'Major': row[1],
                    'Submajor': row[1],
                    'Minor': row[2],
                    'SubMinor': row[3],
                    'Grade': row[4],
                    'File_formats': row[5],
                    'Type': row[6],
                    'Source_Description': row[7],
                    'Place_City': row[9],
                    'Year': row[10],
                    'Publisher': row[11],
                    'Path': row[11],
                    'Collection': row[12],
                    'Collection_type': row[13],
                    'SOI_toposheet_no': row[14],
                    'Data_Resolution': row[15],
                    'Ownership': row[16],
                    'is_processed': row[17],
                    'short_descr': row[18],
                    'descr': row[21],
                    'img_service': row[20],
                    'img_dw': row[22],
                    'map_service': row[24],
                    'map_dw': row[23],
                    'publish_on': row[24],
                    'thumbnail': row[25],
                    'source': row[28],
                    'created_date': row[29]
                }
                for row in rows]}

        cursor.execute(count_query, key_list)
        count = cursor.fetchone()[0]
        data['count'] = count

    return JsonResponse(data)

def sb_subminor(request):
    query_params = request.GET.getlist('selectedItems')
    key_list = [param.replace('%20', ' ') for param in query_params]

    limit = int(request.GET.get('limit', 10))
    offset = int(request.GET.get('offset', 0))

    query = """
        SELECT *
        FROM searchbar_data
        WHERE 1=1 """

    count_query = """
        SELECT COUNT(*)
        FROM searchbar_data
        WHERE 1=1 """

    conditions = []
    for key in key_list:
        conditions.append("""to_tsvector(searchbar_data."id" || ' ' ||searchbar_data."major" || ' ' ||searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor"
            || ' ' || searchbar_data."grade"|| ' ' || searchbar_data."file_formats"|| ' ' || searchbar_data."type"|| ' ' || searchbar_data."source_description"
            || ' ' || searchbar_data."place_city"|| ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
            || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
            || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr"
            || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
            || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
            || ' ' || searchbar_data."thumbnail") @@ plainto_tsquery(%s)""")

    if conditions:
        query += " AND (" + " OR ".join(conditions) + ")"
        count_query += " AND (" + " OR ".join(conditions) + ")"

    query += f" LIMIT {limit} OFFSET {offset}"

    with connection.cursor() as cursor:
        cursor.execute(query, key_list)
        rows = cursor.fetchall()

        data = {
            'data': [
                {
                     'id':row[0],
                    'Major': row[1],
                    'Submajor': row[1],
                    'Minor': row[2],
                    'SubMinor': row[3],
                    'Grade': row[4],
                    'File_formats': row[5],
                    'Type': row[6],
                    'Source_Description': row[7],
                    'Place_City': row[9],
                    'Year': row[10],
                    'Publisher': row[11],
                    'Path': row[11],
                    'Collection': row[12],
                    'Collection_type': row[13],
                    'SOI_toposheet_no': row[14],
                    'Data_Resolution': row[15],
                    'Ownership': row[16],
                    'is_processed': row[17],
                    'short_descr': row[18],
                    'descr': row[21],
                    'img_service': row[20],
                    'img_dw': row[22],
                    'map_service': row[24],
                    'map_dw': row[23],
                    'publish_on': row[24],
                    'thumbnail': row[25],
                    'source': row[28],
                    'created_date': row[29]
                }
                for row in rows
            ]
        }

        cursor.execute(count_query, key_list)
        count = cursor.fetchone()[0]
        data['count'] = count

    return JsonResponse(data)


def sb_grade(request):
    query_params = request.GET.getlist('selectedItems')
    key_list = [param.replace('%20', ' ') for param in query_params]

    limit = request.GET.get('limit', 10)  # Default limit is 10 if not provided
    offset = request.GET.get('offset', 0)  # Default offset is 0 if not provided

    query = """
        SELECT *
        FROM searchbar_data """

    count_query = """
        SELECT COUNT(*)
        FROM searchbar_data """

    conditions = []
    for key in key_list:
        conditions.append("""to_tsvector(searchbar_data."id" || ' ' ||searchbar_data."major" || ' ' ||searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor"
            || ' ' || searchbar_data."grade"|| ' ' || searchbar_data."file_formats"|| ' ' || searchbar_data."type"|| ' ' || searchbar_data."source_description"
            || ' ' || searchbar_data."place_city"|| ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
            || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
            || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr"
            || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
            || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
            || ' ' || searchbar_data."thumbnail") @@ plainto_tsquery(%s)""")

    if conditions:
        query += " WHERE " + " OR ".join(conditions)
        count_query += " WHERE " + " OR ".join(conditions)

    query += f" LIMIT {limit} OFFSET {offset}"

    with connection.cursor() as cursor:
        cursor.execute(query, key_list)
        rows = cursor.fetchall()

        data = {
            'data': [
                {
                      'id':row[0],
                    'Major': row[1],
                    'Submajor': row[1],
                    'Minor': row[2],
                    'SubMinor': row[3],
                    'Grade': row[4],
                    'File_formats': row[5],
                    'Type': row[6],
                    'Source_Description': row[7],
                    'Place_City': row[9],
                    'Year': row[10],
                    'Publisher': row[11],
                    'Path': row[11],
                    'Collection': row[12],
                    'Collection_type': row[13],
                    'SOI_toposheet_no': row[14],
                    'Data_Resolution': row[15],
                    'Ownership': row[16],
                    'is_processed': row[17],
                    'short_descr': row[18],
                    'descr': row[21],
                    'img_service': row[20],
                    'img_dw': row[22],
                    'map_service': row[24],
                    'map_dw': row[23],
                    'publish_on': row[24],
                    'thumbnail': row[25],
                    'source': row[28],
                    'created_date': row[29]
                }
                for row in rows
            ]
        }

        cursor.execute(count_query, key_list)
        count = cursor.fetchone()[0]
        data['count'] = count

    return JsonResponse(data)


def sb_publisher(request):
    query_params = request.GET.getlist('selectedItems')
    key_list = [param.replace('%20', ' ') for param in query_params]

    query = """
        SELECT *
        FROM searchbar_data """

    count_query = """
        SELECT COUNT(*)
        FROM searchbar_data """

    conditions = []
    for key in key_list:
        conditions.append("""to_tsvector(searchbar_data."id" || ' ' ||searchbar_data."major" || ' ' ||searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor"
    || ' ' || searchbar_data."grade"|| ' ' || searchbar_data."file_formats"|| ' ' || searchbar_data."type"|| ' ' || searchbar_data."source_description"
    || ' ' || searchbar_data."place_city"|| ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
    || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
    || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr"
    || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
    || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
    || ' ' || searchbar_data."thumbnail") @@ plainto_tsquery(%s)""")

    if conditions:
        query += " WHERE (" + " OR ".join(conditions) + ")"
        count_query += " WHERE (" + " OR ".join(conditions) + ")"

    # Add LIMIT and OFFSET based on request parameters
    limit = int(request.GET.get('limit', 10))
    offset = int(request.GET.get('offset', 0))
    query += f"\nLIMIT {limit} OFFSET {offset}"

    with connection.cursor() as cursor:
        cursor.execute(query, key_list)
        rows = cursor.fetchall()

        data = {
            'data': [
               {
                    'id':row[0],
                    'Major': row[1],
                    'Submajor': row[1],
                    'Minor': row[2],
                    'SubMinor': row[3],
                    'Grade': row[4],
                    'File_formats': row[5],
                    'Type': row[6],
                    'Source_Description': row[7],
                    'Place_City': row[9],
                    'Year': row[10],
                    'Publisher': row[11],
                    'Path': row[11],
                    'Collection': row[12],
                    'Collection_type': row[13],
                    'SOI_toposheet_no': row[14],
                    'Data_Resolution': row[15],
                    'Ownership': row[16],
                    'is_processed': row[17],
                    'short_descr': row[18],
                    'descr': row[21],
                    'img_service': row[20],
                    'img_dw': row[22],
                    'map_service': row[24],
                    'map_dw': row[23],
                    'publish_on': row[24],
                    'thumbnail': row[25],
                    'source': row[28],
                    'created_date': row[29]
                }
                for row in rows
            ]
        }

        cursor.execute(count_query, key_list)
        count = cursor.fetchone()[0]
        data['count'] = count

    return JsonResponse(data)

def sb_place(request):
    query_params = request.GET.getlist('selectedItems')
    key_list = [param.replace('%20', ' ') for param in query_params]

    query = """
        SELECT *
        FROM searchbar_data """

    count_query = """
        SELECT COUNT(*)
        FROM searchbar_data """

    conditions = []
    for key in key_list:
        conditions.append("""to_tsvector(searchbar_data."id" || ' ' ||searchbar_data."major" || ' ' ||searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor"
            || ' ' || searchbar_data."grade"|| ' ' || searchbar_data."file_formats"|| ' ' || searchbar_data."type"|| ' ' || searchbar_data."source_description"
            || ' ' || searchbar_data."place_city"|| ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
            || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
            || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr"
            || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
            || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
            || ' ' || searchbar_data."thumbnail") @@ plainto_tsquery(%s)""")

    if conditions:
        query += " WHERE (" + " OR ".join(conditions) + ")"
        count_query += " WHERE (" + " OR ".join(conditions) + ")"

    # Add LIMIT and OFFSET based on request parameters
    limit = int(request.GET.get('limit', 10))
    offset = int(request.GET.get('offset', 0))
    query += f"\nLIMIT {limit} OFFSET {offset}"

    with connection.cursor() as cursor:
        cursor.execute(query, key_list)
        rows = cursor.fetchall()

        data = {
            'data': [
               {
                   'id':row[0],
                    'Major': row[1],
                    'Submajor': row[1],
                    'Minor': row[2],
                    'SubMinor': row[3],
                    'Grade': row[4],
                    'File_formats': row[5],
                    'Type': row[6],
                    'Source_Description': row[7],
                    'Place_City': row[9],
                    'Year': row[10],
                    'Publisher': row[11],
                    'Path': row[11],
                    'Collection': row[12],
                    'Collection_type': row[13],
                    'SOI_toposheet_no': row[14],
                    'Data_Resolution': row[15],
                    'Ownership': row[16],
                    'is_processed': row[17],
                    'short_descr': row[18],
                    'descr': row[21],
                    'img_service': row[20],
                    'img_dw': row[22],
                    'map_service': row[24],
                    'map_dw': row[23],
                    'publish_on': row[24],
                    'thumbnail': row[25],
                    'source': row[28],
                    'created_date': row[29]
                }
                for row in rows
            ]
        }
        

        cursor.execute(count_query, key_list)
        count = cursor.fetchone()[0]
        data['count'] = count

    return JsonResponse(data)


def sb_year(request):
    query_params = request.GET.getlist('selectedItems')
    key_list = [param.replace('%20', ' ') for param in query_params]

    limit = int(request.GET.get('limit', 10))
    offset = int(request.GET.get('offset', 0))
    query = """
        SELECT *
        FROM searchbar_data """

    count_query = """
        SELECT COUNT(*)
        FROM searchbar_data """

    conditions = []
    for key in key_list:
        conditions.append("""to_tsvector(to_tsvector(searchbar_data."id" || ' ' ||searchbar_data."major" || ' ' ||searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor"
            || ' ' || searchbar_data."grade"|| ' ' || searchbar_data."file_formats"|| ' ' || searchbar_data."type"|| ' ' || searchbar_data."source_description"
            || ' ' || searchbar_data."place_city"|| ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
            || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
            || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr"
            || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
            || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
            || ' ' || searchbar_data."thumbnail") @@ plainto_tsquery(%s)""")

    if conditions:
        query += " WHERE " + " OR ".join(conditions)
        count_query += " WHERE " + " OR ".join(conditions)

    # Add LIMIT and OFFSET based on request parameters
    query += f" LIMIT {limit} OFFSET {offset}"

    with connection.cursor() as cursor:
        cursor.execute(query, key_list)
        rows = cursor.fetchall()

        data = {
            'data': [{
                    'id':row[0],
                    'Major': row[1],
                    'Submajor': row[1],
                    'Minor': row[2],
                    'SubMinor': row[3],
                    'Grade': row[4],
                    'File_formats': row[5],
                    'Type': row[6],
                    'Source_Description': row[7],
                    'Place_City': row[9],
                    'Year': row[10],
                    'Publisher': row[11],
                    'Path': row[11],
                    'Collection': row[12],
                    'Collection_type': row[13],
                    'SOI_toposheet_no': row[14],
                    'Data_Resolution': row[15],
                    'Ownership': row[16],
                    'is_processed': row[17],
                    'short_descr': row[18],
                    'descr': row[21],
                    'img_service': row[20],
                    'img_dw': row[22],
                    'map_service': row[24],
                    'map_dw': row[23],
                    'publish_on': row[24],
                    'thumbnail': row[25],
                    'source': row[28],
                    'created_date': row[29]
                }
                for row in rows]
        }

        cursor.execute(count_query, key_list)
        count = cursor.fetchone()[0]
        data['count'] = count

    return JsonResponse(data)


import json


from django.http import JsonResponse
import json

from django.http import JsonResponse
import json

def main_section_data_meta_data(request):
    query = request.GET.get('query', '')  # Get the search query from the request

    # Call the global_search_by_key function to get the search results
    search_results_bytes = global_search_by_key(request, query)

    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT 'major' AS type, COALESCE(major) AS subhead, COUNT(*) AS count
            FROM searchbar_data
            WHERE major IS NOT NULL
            AND major <> ''
            GROUP BY COALESCE(major)
            UNION ALL
            SELECT 'submajor' AS type, COALESCE(submajor) AS subhead, COUNT(*) AS count 
            FROM data 
            WHERE major IS NOT NULL
            AND submajor <> ''
            GROUP BY COALESCE(submajor)
        ''')
        rows = cursor.fetchall()
        side_bar_data = {
            'major': [],
            'submajor': [],
        }

        for row in rows:
            item = {
                'subhead': row[1],
                'count': row[2]
            }
            if row[0] == 'major':
                side_bar_data['major'].append(item)
            elif row[0] == 'submajor':
                side_bar_data['submajor'].append(item)

    search_results_serializable = [
        {
            'Major': row[0],
            'Submajor': row[1],
            'Minor': row[2],
            'SubMinor': row[3],
            'Grade': row[4],
            'File_formats': row[5],
            'Type': row[6],
            'Source_Description': row[7],
            'Place_City': row[8],
            'Year': row[9]
        }
        for row in search_results_bytes
    ]

    data = {
        'search_results': search_results_serializable,
        'side_bar_data': side_bar_data
    }

    return JsonResponse(data)


def sb_subcollection(request):
    query_params = request.GET.getlist('selectedItems')
    key_list = [param.replace('%20', ' ') for param in query_params]

    limit = int(request.GET.get('limit', 10))  # Default limit is 10
    offset = int(request.GET.get('offset', 0))  # Default offset is 0

    query = """
        SELECT *
        FROM searchbar_data """

    count_query = """
        SELECT COUNT(*)
        FROM searchbar_data """

    conditions = []
    for key in key_list:
        conditions.append("""to_tsvector(searchbar_data."major" || ' ' ||searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor"
            || ' ' || searchbar_data."grade"|| ' ' || searchbar_data."file_formats"|| ' ' || searchbar_data."type"|| ' ' || searchbar_data."source_description"
            || ' ' || searchbar_data."place_city"|| ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
            || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
            || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr"
            || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
            || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
            || ' ' || searchbar_data."thumbnail") @@ plainto_tsquery(%s)""")

    if conditions:
        query += " WHERE " + " OR ".join(conditions)
        count_query += " WHERE " + " OR ".join(conditions)

    query += f" LIMIT {limit} OFFSET {offset}"

    with connection.cursor() as cursor:
        cursor.execute(query, key_list)
        rows = cursor.fetchall()

        data = {
            'data': [
                {   'id':row[0],
                    'Major': row[1],
                    'Submajor': row[1],
                    'Minor': row[2],
                    'SubMinor': row[3],
                    'Grade': row[4],
                    'File_formats': row[5],
                    'Type': row[6],
                    'Source_Description': row[7],
                    'Place_City': row[9],
                    'Year': row[10],
                    'Publisher': row[11],
                    'Path': row[11],
                    'Collection': row[12],
                    'Collection_type': row[13],
                    'SOI_toposheet_no': row[14],
                    'Data_Resolution': row[15],
                    'Ownership': row[16],
                    'is_processed': row[17],
                    'short_descr': row[18],
                    'descr': row[21],
                    'img_service': row[20],
                    'img_dw': row[22],
                    'map_service': row[24],
                    'map_dw': row[23],
                    'publish_on': row[24],
                    'thumbnail': row[25],
                    'source': row[28],
                    'created_date': row[29]
                }
                
                for row in rows
        
            ]
        }

        cursor.execute(count_query, key_list)
        count = cursor.fetchone()[0]
        data['count'] = count

    return JsonResponse(data)



@api_view(['GET'])
def main_section_data_meta_data(request, query):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT
                COALESCE(major) AS Major,
                COALESCE(submajor) AS Submajor,
                COALESCE(minor) AS Minor,
                COALESCE(subminor) AS SubMinor,
                COALESCE(grade) AS Grade,
                COALESCE(file_formats) AS File_Formats,
                COALESCE(type) AS Type,
                COALESCE(source_description) AS Source_Description,
                COALESCE(place_city) AS Place_City,
                COALESCE(year) AS Year,
                COALESCE(publisher) AS Publisher,
                COALESCE(path) AS Path,
                COALESCE(collection) AS Collection,
                COALESCE(collection_type) AS Collection_Type,
                COALESCE(soi_toposheet_no) AS SOI_TopoSheet_No,
                COALESCE(data_resolution) AS Data_Resolution,
                COALESCE(ownership) AS Ownership,
                COALESCE(is_processed) AS Is_Processed,
                COALESCE(short_descr) AS Short_Descr,
                COALESCE(descr) AS Descr,
                COALESCE(img_service) AS Img_Service,
                COALESCE(img_dw) AS Img_DW,
                COALESCE(map_service) AS Map_Service,
                COALESCE(map_dw) AS Map_DW,
                COALESCE(publish_on) AS Publish_On,
                COALESCE(thumbnail) AS Thumbnail,
                COALESCE(source) AS Source,
                COUNT(*) AS Count
            FROM searchbar_data
            WHERE
                major IS NOT NULL AND major <> '' OR
                submajor IS NOT NULL AND submajor <> '' OR
                minor IS NOT NULL AND minor <> '' OR
                subminor IS NOT NULL AND subminor <> '' OR
                grade IS NOT NULL AND grade <> '' OR
                file_formats IS NOT NULL AND file_formats <> '' OR
                type IS NOT NULL AND type <> '' OR
                source_description IS NOT NULL AND source_description <> '' OR
                place_city IS NOT NULL AND place_city <> '' OR
                year IS NOT NULL AND year <> '' OR
                publisher IS NOT NULL AND publisher <> '' OR
                path IS NOT NULL AND path <> '' OR
                collection IS NOT NULL AND collection <> '' OR
                collection_type IS NOT NULL AND collection_type <> '' OR
                soi_toposheet_no IS NOT NULL AND soi_toposheet_no <> '' OR
                data_resolution IS NOT NULL AND data_resolution <> '' OR
                ownership IS NOT NULL AND ownership <> '' OR
                is_processed IS NOT NULL AND is_processed <> '' OR
                short_descr IS NOT NULL AND short_descr <> '' OR
                descr IS NOT NULL AND descr <> '' OR
                img_service IS NOT NULL AND img_service <> '' OR
                img_dw IS NOT NULL AND img_dw <> '' OR
                map_service IS NOT NULL AND map_service <> '' OR
                map_dw IS NOT NULL AND map_dw <> '' OR
                publish_on IS NOT NULL AND publish_on <> '' OR
                thumbnail IS NOT NULL AND thumbnail <> '' OR
                source IS NOT NULL AND source <> '' 
            GROUP BY
                Major,
                Submajor,
                Minor,
                SubMinor,
                Grade,
                File_Formats,
                Type,
                Source_Description,
                Place_City,
                Year,
                Publisher,
                Path,
                Collection,
                Collection_Type,
                SOI_TopoSheet_No,
                Data_Resolution,
                Ownership,
                Is_Processed,
                Short_Descr,
                Descr,
                Img_Service,
                Img_DW,
                Map_Service,
                Map_DW,
                Publish_On,
                Thumbnail,
                Source
        ''')
        rows = cursor.fetchall()
        
        data = {'data': [
            {
                'Major': row[0],
                'Submajor': row[1],
                'Minor': row[2],
                'SubMinor': row[3],
                'Grade': row[4],
                'File_Formats': row[5],
                'Type': row[6],
                'Source_Description': row[7],
                'Place_City': row[8],
                'Year': row[9],
                'Publisher': row[10],
                'Path': row[11],
                'Collection': row[12],
                'Collection_Type': row[13],
                'SOI_TopoSheet_No': row[14],
                'Data_Resolution': row[15],
                'Ownership': row[16],
                'Is_Processed': row[17],
                'Short_Descr': row[18],
                'Descr': row[19],
                'Img_Service': row[20],
                'Img_DW': row[21],
                'Map_Service': row[22],
                'Map_DW': row[23],
                'Publish_On': row[24],
                'Thumbnail': row[25],
                'Source': row[26],
                'Count': row[27]
            }
            for row in rows
        ]}
        
        # Get subheads and counts
        subheads = {
            'Major': len(set(row[0] for row in rows)),
            'Submajor': len(set(row[1] for row in rows)),
            'Minor': len(set(row[2] for row in rows)),
            'SubMinor': len(set(row[3] for row in rows)),
            'Grade': len(set(row[4] for row in rows)),
            'File_Formats': len(set(row[5] for row in rows)),
            'Type': len(set(row[6] for row in rows)),
            'Source_Description': len(set(row[7] for row in rows)),
            'Place_City': len(set(row[8] for row in rows)),
            'Year': len(set(row[9] for row in rows)),
            'Publisher': len(set(row[10] for row in rows)),
            'Path': len(set(row[11] for row in rows)),
            'Collection': len(set(row[12] for row in rows)),
            'Collection_Type': len(set(row[13] for row in rows)),
            'SOI_TopoSheet_No': len(set(row[14] for row in rows)),
            'Data_Resolution': len(set(row[15] for row in rows)),
            'Ownership': len(set(row[16] for row in rows)),
            'Is_Processed': len(set(row[17] for row in rows)),
            'Short_Descr': len(set(row[18] for row in rows)),
            'Descr': len(set(row[19] for row in rows)),
            'Img_Service': len(set(row[20] for row in rows)),
            'Img_DW': len(set(row[21] for row in rows)),
            'Map_Service': len(set(row[22] for row in rows)),
            'Map_DW': len(set(row[23] for row in rows)),
            'Publish_On': len(set(row[24] for row in rows)),
            'Thumbnail': len(set(row[25] for row in rows)),
            'Source': len(set(row[26] for row in rows))
        }
        
        response = {
            'ms_data': data,
            'sb_data': subheads
        }
        
        return JsonResponse(response)



















def search_data_new(request, query):
    with connection.cursor() as cursor:
        words = query.split()
        tsquery = ' | '.join(words)
        cursor.execute("""
            SELECT *
            FROM searchbar_data
            WHERE to_tsvector(searchbar_data."id" || ' ' ||searchbar_data."major" || ' ' || searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor" 
            || ' ' || searchbar_data."grade"|| ' ' || searchbar_data."file_formats"|| ' ' || searchbar_data."type"|| ' ' || searchbar_data."source_description"
            || ' ' || searchbar_data."place_city"|| ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
            || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
            || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr" 
            || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
            || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
            || ' ' || searchbar_data."thumbnail") @@ to_tsquery(%s)
        """, [tsquery])
        rows = cursor.fetchall()
        search_results = {'data': [{ 'id':row[0],
                    'Major': row[1],
                    'Submajor': row[1],
                    'Minor': row[2],
                    'SubMinor': row[3],
                    'Grade': row[4],
                    'File_formats': row[5],
                    'Type': row[6],
                    'Source_Description': row[7],
                    'Place_City': row[9],
                    'Year': row[10],
                    'Publisher': row[11],
                    'Path': row[11],
                    'Collection': row[12],
                    'Collection_type': row[13],
                    'SOI_toposheet_no': row[14],
                    'Data_Resolution': row[15],
                    'Ownership': row[16],
                    'is_processed': row[17],
                    'short_descr': row[18],
                    'descr': row[21],
                    'img_service': row[20],
                    'img_dw': row[22],
                    'map_service': row[24],
                    'map_dw': row[23],
                    'publish_on': row[24],
                    'thumbnail': row[25],
                    'source': row[28],
                    'created_date': row[29]} for row in rows]}
    
    return search_results


def get_sidebar_data_new(request):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT 'major' AS type, COALESCE(major) AS subhead, COUNT(*) AS count
            FROM searchbar_data
            WHERE major IS NOT NULL
            AND major <> ''
            GROUP BY COALESCE(major)
            UNION ALL

            SELECT 'submajor' AS type, COALESCE(submajor) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
            WHERE major IS NOT NULL
            AND submajor <> ''
            GROUP BY COALESCE(submajor)
            UNION ALL

            SELECT 'minor' AS type, COALESCE(minor) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
            WHERE minor IS NOT NULL
            AND minor <> ''
            GROUP BY COALESCE(minor)
            UNION ALL

            SELECT 'subminor' AS type, COALESCE(subminor) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
            WHERE subminor IS NOT NULL
            AND subminor <> ''
            GROUP BY COALESCE(subminor)
            UNION ALL

            SELECT 'grade' AS type, COALESCE(grade) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
            WHERE grade IS NOT NULL
            AND grade <> ''
            GROUP BY COALESCE(grade)
            UNION ALL


            SELECT 'publisher' AS type, COALESCE(publisher) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
            WHERE publisher IS NOT NULL
            AND publisher <> ''
            GROUP BY COALESCE(publisher)
            UNION ALL

            SELECT 'place_city' AS type, COALESCE(place_city) AS subhead, COUNT(*) AS count
            FROM searchbar_data 
            WHERE place_city IS NOT NULL
            AND place_city <> ''
            GROUP BY COALESCE(place_city)
            UNION ALL

            SELECT 'year' AS type, COALESCE(year) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
            WHERE year IS NOT NULL
            AND year <> ''
            GROUP BY COALESCE(year)

        ''')
        rows = cursor.fetchall()
        sidebar_data = {
            'major': [],
            'submajor': [],
            'minor': [],
            'subminor': [],
            'grade': [],
            'publisher': [],
            'place_city': [],
            'year': []
        }

        for row in rows:
            item = {
                'subhead': row[1],
                'count': row[2]
            }

            if row[0] == 'major':
                sidebar_data['major'].append(item)
            elif row[0] == 'submajor':
                sidebar_data['submajor'].append(item)
            elif row[0] == 'minor':
                sidebar_data['minor'].append(item)
            elif row[0] == 'subminor':
                sidebar_data['subminor'].append(item)
            elif row[0] == 'grade':
                sidebar_data['grade'].append(item)
            elif row[0] == 'publisher':
                sidebar_data['publisher'].append(item)
            elif row[0] == 'place_city':
                sidebar_data['place_city'].append(item)
            elif row[0] == 'year':
                sidebar_data['year'].append(item)

        return sidebar_data


def main_section_data_meta_data(request, query):
   # query = request.GET.get('query')
    search_results = search_data_new(request, query)
    sidebar_data = get_sidebar_data_new(request)
    
    return JsonResponse({'ms_data': search_results, 'sb_data': sidebar_data})




@api_view(['GET'])
def pagination_of_global_search(request, query):
    limit = int(request.GET.get('limit', 10))  # Number of results per page (default: 10)
    offset = int(request.GET.get('offset', 0))
    
    with connection.cursor() as cursor:
        words = query.split()
        tsquery = ' | '.join(words)
        
        # Count query
        cursor.execute("""
            SELECT COUNT(*)
            FROM searchbar_data
            WHERE to_tsvector(searchbar_data."id" || ' ' ||searchbar_data."major" || ' ' || searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor" 
                || ' ' || searchbar_data."grade" || ' ' || searchbar_data."file_formats" || ' ' || searchbar_data."type" || ' ' || searchbar_data."source_description"
                || ' ' || searchbar_data."place_city" || ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
                || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
                || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr" 
                || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
                || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
                || ' ' || searchbar_data."thumbnail") @@ to_tsquery(%(tsquery)s)
        """, {'tsquery': tsquery})
        
        count_result = cursor.fetchone()
        total_count = count_result[0]
        
        # Data query with limit and offset
        cursor.execute("""
            SELECT *
            FROM searchbar_data
            WHERE to_tsvector(searchbar_data."major" || ' ' || searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor" 
                || ' ' || searchbar_data."grade" || ' ' || searchbar_data."file_formats" || ' ' || searchbar_data."type" || ' ' || searchbar_data."source_description"
                || ' ' || searchbar_data."place_city" || ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
                || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
                || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr" 
                || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
                || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
                || ' ' || searchbar_data."thumbnail") @@ to_tsquery(%(tsquery)s)
            LIMIT %(limit)s OFFSET %(offset)s
        """, {'tsquery': tsquery, 'limit': limit, 'offset': offset})
        
        rows = cursor.fetchall()
        
        data = {
            'count': total_count,
            'data': [
                {
                   'id':row[0],
                    'Major': row[1],
                    'Submajor': row[1],
                    'Minor': row[2],
                    'SubMinor': row[3],
                    'Grade': row[4],
                    'File_formats': row[5],
                    'Type': row[6],
                    'Source_Description': row[7],
                    'Place_City': row[9],
                    'Year': row[10],
                    'Publisher': row[11],
                    'Path': row[11],
                    'Collection': row[12],
                    'Collection_type': row[13],
                    'SOI_toposheet_no': row[14],
                    'Data_Resolution': row[15],
                    'Ownership': row[16],
                    'is_processed': row[17],
                    'short_descr': row[18],
                    'descr': row[21],
                    'img_service': row[20],
                    'img_dw': row[22],
                    'map_service': row[24],
                    'map_dw': row[23],
                    'publish_on': row[24],
                    'thumbnail': row[25],
                    'source': row[28],
                    'created_date': row[29]
                }
                for row in rows
            ]
        }
        
        return JsonResponse(data)


def pagination_if_main_search(request):
    limit = int(request.GET.get('limit', 10))  # Number of results per page (default: 10)
    offset = int(request.GET.get('offset', 0))
    
    with connection.cursor() as cursor:
        # Get the total count of rows
        cursor.execute("SELECT COUNT(*) FROM searchbar_data")
        total_count = cursor.fetchone()[0]
        
        # Retrieve the paginated data
        cursor.execute("""
            SELECT *
            FROM searchbar_data
            ORDER BY (searchbar_data."created_date" IS NULL), searchbar_data."created_date" DESC
            LIMIT %s OFFSET %s
        """, [limit, offset])
        rows = cursor.fetchall()
        print(rows)
        data = {
            'data': [
                {   'id': row[0],
                    'Major': row[1],
                    'Submajor': row[1],
                    'Minor': row[2],
                    'SubMinor': row[3],
                    'Grade': row[4],
                    'File_formats': row[5],
                    'Type': row[6],
                    'Source_Description': row[7],
                    'Place_City': row[9],
                    'Year': row[10],
                    'Publisher': row[11],
                    'Path': row[11],
                    'Collection': row[12],
                    'Collection_type': row[13],
                    'SOI_toposheet_no': row[14],
                    'Data_Resolution': row[15],
                    'Ownership': row[16],
                    'is_processed': row[17],
                    'short_descr': row[18],
                    'descr': row[21],
                    'img_service': row[20],
                    'img_dw': row[22],
                    'map_service': row[24],
                    'map_dw': row[23],
                    'publish_on': row[24],
                    'thumbnail': row[25],
                    'source': row[28],
                    'created_date': row[29]
                }
                
                for row in rows
            ],
          
            'count': total_count  # Total count of rows
        }
        
    return JsonResponse(data)





def search_main_data_for_pagination(request, query, limit, offset):
    with connection.cursor() as cursor:
        words = query.split()
        tsquery = ' | '.join(words)

        # Execute the query to fetch the search results
        cursor.execute("""
            SELECT *
            FROM searchbar_data
            WHERE to_tsvector(searchbar_data."id" || ' ' ||searchbar_data."major" || ' ' || searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor" 
            || ' ' || searchbar_data."grade"|| ' ' || searchbar_data."file_formats"|| ' ' || searchbar_data."type"|| ' ' || searchbar_data."source_description"
            || ' ' || searchbar_data."place_city"|| ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
            || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
            || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr" 
            || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
            || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
            || ' ' || searchbar_data."thumbnail") @@ to_tsquery(%s)
            LIMIT %s OFFSET %s
        """, [tsquery, limit, offset])
        rows = cursor.fetchall()

        # Execute the query to fetch the total count of matching rows
        cursor.execute("""
            SELECT COUNT(*)
            FROM searchbar_data
            WHERE to_tsvector(searchbar_data."id" || ' ' ||searchbar_data."major" || ' ' || searchbar_data."submajor" || ' ' || searchbar_data."minor" || ' ' || searchbar_data."subminor" 
            || ' ' || searchbar_data."grade"|| ' ' || searchbar_data."file_formats"|| ' ' || searchbar_data."type"|| ' ' || searchbar_data."source_description"
            || ' ' || searchbar_data."place_city"|| ' ' || searchbar_data."year" || ' ' || searchbar_data."publisher" || ' ' || searchbar_data."path"
            || ' ' || searchbar_data."collection" || ' ' || searchbar_data."collection_type" || ' ' || searchbar_data."soi_toposheet_no" || ' ' || searchbar_data."data_resolution"
            || ' ' || searchbar_data."ownership" || ' ' || searchbar_data."is_processed" || ' ' || searchbar_data."short_descr" 
            || ' ' || searchbar_data."descr" || ' ' || searchbar_data."img_service" || ' ' || searchbar_data."img_dw"
            || ' ' || searchbar_data."map_service" || ' ' || searchbar_data."map_dw" || ' ' || searchbar_data."publish_on"
            || ' ' || searchbar_data."thumbnail") @@ to_tsquery(%s)
        """, [tsquery])
        total_count = cursor.fetchone()[0]

        search_results = {
             'data': [
                {
                    'id':row[0],
                    'Major': row[1],
                    'Submajor': row[1],
                    'Minor': row[2],
                    'SubMinor': row[3],
                    'Grade': row[4],
                    'File_formats': row[5],
                    'Type': row[6],
                    'Source_Description': row[7],
                    'Place_City': row[9],
                    'Year': row[10],
                    'Publisher': row[11],
                    'Path': row[11],
                    'Collection': row[12],
                    'Collection_type': row[13],
                    'SOI_toposheet_no': row[14],
                    'Data_Resolution': row[15],
                    'Ownership': row[16],
                    'is_processed': row[17],
                    'short_descr': row[18],
                    'descr': row[21],
                    'img_service': row[20],
                    'img_dw': row[22],
                    'map_service': row[24],
                    'map_dw': row[23],
                    'publish_on': row[24],
                    'thumbnail': row[25],
                    'source': row[28],
                    
                    'created_date': row[29]
                }
                
                for row in rows
            ],
            'count': total_count
        }

    return search_results

def get_sidebar_data_for_pagination(request):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT 'major' AS type, COALESCE(major) AS subhead, COUNT(*) AS count
            FROM searchbar_data
            WHERE major IS NOT NULL
            AND major <> ''
            GROUP BY COALESCE(major)
            UNION ALL

            SELECT 'submajor' AS type, COALESCE(submajor) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
            WHERE major IS NOT NULL
            AND submajor <> ''
            GROUP BY COALESCE(submajor)
            UNION ALL

            SELECT 'minor' AS type, COALESCE(minor) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
            WHERE minor IS NOT NULL
            AND minor <> ''
            GROUP BY COALESCE(minor)
            UNION ALL

            SELECT 'subminor' AS type, COALESCE(subminor) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
            WHERE subminor IS NOT NULL
            AND subminor <> ''
            GROUP BY COALESCE(subminor)
            UNION ALL

            SELECT 'grade' AS type, COALESCE(grade) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
            WHERE grade IS NOT NULL
            AND grade <> ''
            GROUP BY COALESCE(grade)
            UNION ALL


            SELECT 'publisher' AS type, COALESCE(publisher) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
            WHERE publisher IS NOT NULL
            AND publisher <> ''
            GROUP BY COALESCE(publisher)
            UNION ALL

            SELECT 'place_city' AS type, COALESCE(place_city) AS subhead, COUNT(*) AS count
            FROM searchbar_data 
            WHERE place_city IS NOT NULL
            AND place_city <> ''
            GROUP BY COALESCE(place_city)
            UNION ALL

            SELECT 'year' AS type, COALESCE(year) AS subhead, COUNT(*) AS count 
            FROM searchbar_data 
            WHERE year IS NOT NULL
            AND year <> ''
            GROUP BY COALESCE(year)

        ''')
        rows = cursor.fetchall()
        sidebar_data = {
            'major': [],
            'submajor': [],
            'minor': [],
            'subminor': [],
            'grade': [],
            'publisher': [],
            'place_city': [],
            'year': []
        }

        for row in rows:
            item = {
                'subhead': row[1],
                'count': row[2]
            }

            if row[0] == 'major':
                sidebar_data['major'].append(item)
            elif row[0] == 'submajor':
                sidebar_data['submajor'].append(item)
            elif row[0] == 'minor':
                sidebar_data['minor'].append(item)
            elif row[0] == 'subminor':
                sidebar_data['subminor'].append(item)
            elif row[0] == 'grade':
                sidebar_data['grade'].append(item)
            elif row[0] == 'publisher':
                sidebar_data['publisher'].append(item)
            elif row[0] == 'place_city':
                sidebar_data['place_city'].append(item)
            elif row[0] == 'year':
                sidebar_data['year'].append(item)

        return sidebar_data


def get_meta_data_with_pagination(request, query):
    limit = int(request.GET.get('limit', 10))  # Number of results per page (default: 10)
    offset = int(request.GET.get('offset', 0))
   # query = request.GET.get('query')
    search_results = search_main_data_for_pagination(request, query, limit, offset)
    sidebar_data = get_sidebar_data_for_pagination(request)
    
    return JsonResponse({'ms_data': search_results, 'sb_data': sidebar_data})



class DetailsViewSet(viewsets.ModelViewSet):
    queryset = Downloads.objects.all()
    serializer_class = DownloadDetailsSerializer

    def create(self, request,*args, **kwargs):
            de_data=request.data

            data_id = data.objects.get(id=de_data["data_id"])

            serializer=DownloadDetailsSerializer(data_id,de_data)
            if serializer.is_valid():
                    serializer.save()

                    return Response(serializer.data)
    

    