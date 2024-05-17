from rest_framework import viewsets
from rest_framework.response import Response
from searchbar.models import data
from .serializer import SourceDataSerializer
from shapely.geometry import Polygon, mapping
from datetime import datetime
import os
from pystac import Catalog
from django.http import JsonResponse
from rest_framework.decorators import action
import rasterio
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime
import pystac
import json
from rest_framework.pagination import PageNumberPagination
import os
import pytz
import datetime as dt


class StacViewSet(viewsets.ViewSet):
    def list(self, request, *args, **kwargs):
        # = Catalog.from_file("./example-catalog/catalog.json")
        catalog = Catalog.from_file("./flames/stac-catalog")
        return Response(f"Stac App: {catalog.title}")

    def retrieve(self, request, *args, **kwargs):
        catalog = Catalog(
            id="tutorial-catalog",
            description="This catalog is a basic demonstration catalog utilizing a scene from SpaceNet 5.",
        )
        catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)
        return Response(f"Stac Created: {catalog.title}")



# Function to add stac item in catalog added item is added in stac_catalog folder
@api_view(['POST'])
def add_item_to_stac(request):
    #raster_path = "C:\\Users\\DELL\\Downloads\\480-360-sample.tiff"
    
    # assume that in request.data we got request
    data = request.data  
    print("**********",data)
    img_download_url = request.data.get("img_download_url", "")
    with rasterio.open(img_download_url) as r:
        bbox, footprint = get_bbox_and_footprint(img_download_url)

        image_name = os.path.split(img_download_url)[-1]
        item_id = f"{image_name}-item"
        
        # Get the current datetime
        current_datetime = datetime.now()
        
        # Format the datetime object
        formatted_datetime = current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        
        # Extracting values from the request data
        properties = {
            "id": data.get("id", None),
            "major": data.get("major", ""),
            "submajor": data.get("submajor", ""),
            "minor": data.get("minor", ""),
            "subminor": data.get("subminor", ""),
            "grade": data.get("grade", ""),
            "file_formats": data.get("file_formats", ""),
            "type": data.get("type", ""),
            "source_description": data.get("source_description", ""),
            "place_city": data.get("place_city", ""),
            "year": data.get("year", ""),
            "publisher": data.get("publisher", ""),
            "path": data.get("path", ""),
            "collection": data.get("collection", ""),
            "collection_type": data.get("collection_type", ""),
            "soi_toposheet_no": data.get("soi_toposheet_no", ""),
            "grade1": data.get("grade1", ""),
            "data_resolution": data.get("data_resolution", ""),
            "ownership": data.get("ownership", ""),
            "is_processed": data.get("is_processed", ""),
            "short_descr": data.get("short_descr", ""),
            "descr":data.get("descr", ""),
            "img_service":data.get("img_service", ""),
            "img_dw": data.get("img_dw", ""),
            "map_service":data.get("map_service", ""),
            "map_dw": data.get("map_dw", ""),
            "publish_on": data.get("publish_on", ""),
            "thumbnail": data.get("thumbnail", ""),
            "source": data.get("source", ""),
            "created_id": data.get("created_id", ""),
            "created_date":data.get("created_date", ""),
            "modified_id": data.get("modified_id", ""),
            "modified_date": data.get("modified_date", ""),
            "deleted_id":data.get("deleted_id", ""),
            "deleted_date": data.get("deleted_date", ""),
            "img_download_url":data.get("img_download_url",""),
            "img_vis_url":data.get("img_vis_url",""),
            "shp_file_url":data.get("shp_file_url",""),
            "sub_collection":data.get("sub_collection",""),
            "urlalias":data.get("urlalias",""),
            "datetime":formatted_datetime
                        # Add other fields accordingly
        }
        
        print("**********",properties)
        item = pystac.Item(
            id=item_id,
            geometry=footprint,
            bbox=bbox,
             datetime=datetime.now(),
            properties=properties,
        )
        print("///////",item.datetime)
    # print("Request data:", data)
    #print("Properties:",item.properties)
        catalog_path = "./stac-catalog/catalog.json"
        try:
            catalog = pystac.Catalog.from_file(catalog_path)
        except FileNotFoundError:
            catalog = pystac.Catalog(id="my-stac-catalog", description="My STAC Catalog")

        catalog.add_item(item)
        print("*********** catalog.add_item(item)********* ",catalog.add_item(item))
        item.add_asset(
            key="image",
            asset=pystac.Asset(
                href=img_download_url, media_type=pystac.MediaType.GEOTIFF
            ),
        )
        print("*********** item.add_asset********* ",item.add_asset)
      #  catalog.normalize_hrefs("./stac-catalog")
      #  print("*********** catalog.normalize_hrefs********* ",catalog.normalize_hrefs("./stac-catalog"))
        catalog.save(catalog_type=pystac.CatalogType.SELF_CONTAINED)

        return JsonResponse({"status": "success", "message": "Item added to STAC catalog","data":properties})
        
def get_bbox_and_footprint(img_download_url):
    with rasterio.open(img_download_url) as r:
        bounds = r.bounds
        bbox = [bounds.left, bounds.bottom, bounds.right, bounds.top]
        footprint = Polygon(
            [
                [bounds.left, bounds.bottom],
                [bounds.left, bounds.top],
                [bounds.right, bounds.top],
                [bounds.right, bounds.bottom],
            ]
        )
    return bbox, mapping(footprint)



class SourceDataViewSet(viewsets.ModelViewSet):
    queryset=data.objects.all()
    serializer_class=SourceDataSerializer


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Adjust the page size as needed
    page_size_query_param = 'page_size'
    max_page_size = 100

#### Function to get all catalog data all files data from stac-catalog folder
@api_view(['GET'])
def search_catalog_common_metadata_api(request, **kwargs):
   # try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"
        
        # Get limit and offset from the request query parameters
        limit = int(request.query_params.get('limit', 10))  # Default to 10 items per page
        offset = int(request.query_params.get('offset', 0))
        # List to store items
        items = []
        
        # Iterate through each item folder in the catalog
        for item_folder_name in os.listdir(catalog_path):
            # Check if the folder name is in the expected format
            if item_folder_name.endswith('-item'):
                print("Item folder name:", item_folder_name)
                
                # Extract the item name from the folder name
                item_name = item_folder_name[:-6]  # Remove the '-item' suffix
                print("Item name:", item_name)
                
                # Construct the full path to the item folder
                item_folder_path = os.path.join(catalog_path, item_folder_name)
                print("Item folder path:", item_folder_path)

                # Access files within the item folder
                for file_name in os.listdir(item_folder_path):
                    print("File name:", file_name)
                    
                    # Check if the file is either a JSON file or a GeoTIFF file
                    if file_name.endswith('-item.json') or file_name.endswith('.tiff'):
                        file_path = os.path.join(item_folder_path, file_name)
                        print("File path:", file_path)
                        
                        # Example: Read the content of JSON file
                        if file_name.endswith('-item.json'):
                            with open(file_path, 'r') as json_file:
                                item_data = json.load(json_file)
                                # Extract relevant information from properties dictionary
                                properties = item_data.get('properties', {})
                                response_data = {
                                   "Major": properties.get("major", ""),
                                "Submajor": properties.get("submajor", ""),
                                "Minor": properties.get("minor", ""),
                                "SubMinor": properties.get("subminor", ""),
                                "Grade": properties.get("grade", ""),
                                "File_formats": properties.get("file_formats", ""),
                                "Type": properties.get("type", ""),
                                "Source_Description": properties.get("source_description", ""),
                                "place_city": properties.get("place_city", ""),
                                "year": properties.get("year", ""),
                                "publisher": properties.get("publisher", ""),
                                "Path": properties.get("path", ""),
                                "Collection": properties.get("collection", ""),
                                "Collection_type": properties.get("collection_type", ""),
                                "SOI_toposheet_no": properties.get("soi_toposheet_no", ""),
                                "Data_Resolution": properties.get("data_resolution", ""),
                                "Ownership": properties.get("ownership", ""),
                                "is_processed": properties.get("is_processed", ""),
                                "short_descr": properties.get("short_descr", ""),
                                "descr": properties.get("descr", ""),
                                "img_service": properties.get("img_service", ""),
                                "img_dw": properties.get("img_dw", ""),
                                "map_service": properties.get("map_service", ""),
                                "map_dw": properties.get("map_dw", ""),
                                "publish_on": properties.get("publish_on", ""),
                                "thumbnail": properties.get("thumbnail", ""),
                                "source": properties.get("source", ""),
                                "created_date": properties.get("created_date", ""),
                                "urlalias":properties.get("urlalias","")
                                   
                                }
                                
                                items.append(response_data)
                        
        # Return the list of items
        paginated_items = items[offset : offset + limit]

        return Response({'data': paginated_items})
   # except Exception as e:
      #  return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


 #   except Exception as e:
        # Handle exceptions and return an error response
    #    error_message = str(e)
    #    return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




@api_view(['GET'])
def search_catalog_metadata_by_key_api(request, key_to_search, **kwargs):
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []

        # Iterate through each item folder in the catalog
        for item_folder_name in os.listdir(catalog_path):
            # Check if the folder name is in the expected format
            if item_folder_name.endswith('-item'):
                

                # Construct the full path to the item folder
                item_folder_path = os.path.join(catalog_path, item_folder_name)
              
                # Access files within the item folder
                for file_name in os.listdir(item_folder_path):
                  

                    # Check if the file is a JSON file
                    if file_name.endswith('-item.json'):
                        file_path = os.path.join(item_folder_path, file_name)
                       

                        # Example: Read the content of JSON file
                        with open(file_path, 'r') as json_file:
                            item_data = json.load(json_file)
                            print("-----------------",item_data)
                            # Check if the specified key is present in the properties section
                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                properties_values = item_data['properties'].values()
                                if any(str(key_to_search).lower() in str(value).lower() for value in properties_values):
                                    print("File path:", file_path)
                                    items.append(item_data)



        # Return the list of items
        paginator = CustomPageNumberPagination()
        paginated_items = paginator.paginate_queryset(items, request)
        return paginator.get_paginated_response({'data': paginated_items})

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    
    
# function for the search of side bar minor  data
@api_view(['GET'])
def sb_minor(request, **kwargs):
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []

        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Iterate through each item folder in the catalog
        for item_folder_name in os.listdir(catalog_path):
            # Check if the folder name is in the expected format
            if item_folder_name.endswith('-item'):
                # Construct the full path to the item folder
                item_folder_path = os.path.join(catalog_path, item_folder_name)

                # Access files within the item folder
                for file_name in os.listdir(item_folder_path):
                    # Check if the file is a JSON file
                    if file_name.endswith('-item.json'):
                        file_path = os.path.join(item_folder_path, file_name)

                        # Example: Read the content of JSON file
                        with open(file_path, 'r') as json_file:
                            item_data = json.load(json_file)

                            # Check if the 'properties' key is present and is a dictionary
                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                # Check if any of the selectedItems is present in the 'properties' values
                                properties_values = item_data['properties'].values()
                                if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                    print("File path:", file_path)
                                    formatted_item = format_item_data(item_data)
                                    items.append(formatted_item)
                                    

        # Return the list of items matching the specified keys along with the count
        response_data = {"data": items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# function for the search of side bar sub_minor  data
@api_view(['GET'])
def sb_subminor(request, **kwargs):
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []

        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Iterate through each item folder in the catalog
        for item_folder_name in os.listdir(catalog_path):
            # Check if the folder name is in the expected format
            if item_folder_name.endswith('-item'):
                # Construct the full path to the item folder
                item_folder_path = os.path.join(catalog_path, item_folder_name)

                # Access files within the item folder
                for file_name in os.listdir(item_folder_path):
                    # Check if the file is a JSON file
                    if file_name.endswith('-item.json'):
                        file_path = os.path.join(item_folder_path, file_name)

                        # Example: Read the content of JSON file
                        with open(file_path, 'r') as json_file:
                            item_data = json.load(json_file)

                            # Check if the 'properties' key is present and is a dictionary
                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                # Check if any of the selectedItems is present in the 'properties' values
                                properties_values = item_data['properties'].values()
                                if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                    print("File path:", file_path)
                                    formatted_item = format_item_data(item_data)
                                    items.append(formatted_item)

        # Return the list of items matching the specified keys along with the count
        response_data = {"data": items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# function for the search of side bar grade  data
@api_view(['GET'])
def sb_grade(request, **kwargs):
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []

        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Iterate through each item folder in the catalog
        for item_folder_name in os.listdir(catalog_path):
            # Check if the folder name is in the expected format
            if item_folder_name.endswith('-item'):
                # Construct the full path to the item folder
                item_folder_path = os.path.join(catalog_path, item_folder_name)

                # Access files within the item folder
                for file_name in os.listdir(item_folder_path):
                    # Check if the file is a JSON file
                    if file_name.endswith('-item.json'):
                        file_path = os.path.join(item_folder_path, file_name)

                        # Example: Read the content of JSON file
                        with open(file_path, 'r') as json_file:
                            item_data = json.load(json_file)

                            # Check if the 'properties' key is present and is a dictionary
                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                # Check if any of the selectedItems is present in the 'properties' values
                                properties_values = item_data['properties'].values()
                                if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                    formatted_item = format_item_data(item_data)
                                    items.append(formatted_item)

        # Return the list of items matching the specified keys along with the count
        response_data = {"data": items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# function for the search of side bar publisher  data
@api_view(['GET'])
def sb_publisher(request, **kwargs):
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []

        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Iterate through each item folder in the catalog
        for item_folder_name in os.listdir(catalog_path):
            # Check if the folder name is in the expected format
            if item_folder_name.endswith('-item'):
                # Construct the full path to the item folder
                item_folder_path = os.path.join(catalog_path, item_folder_name)

                # Access files within the item folder
                for file_name in os.listdir(item_folder_path):
                    # Check if the file is a JSON file
                    if file_name.endswith('-item.json'):
                        file_path = os.path.join(item_folder_path, file_name)

                        # Example: Read the content of JSON file
                        with open(file_path, 'r') as json_file:
                            item_data = json.load(json_file)

                            # Check if the 'properties' key is present and is a dictionary
                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                # Check if any of the selectedItems is present in the 'properties' values
                                properties_values = item_data['properties'].values()
                                if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                    formatted_item = format_item_data(item_data)
                                    items.append(formatted_item)

        # Return the list of items matching the specified keys along with the count
        response_data = {"data": items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# function for the search of side bar place  data
@api_view(['GET'])
def sb_place(request, **kwargs):
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []

        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Iterate through each item folder in the catalog
        for item_folder_name in os.listdir(catalog_path):
            # Check if the folder name is in the expected format
            if item_folder_name.endswith('-item'):
                # Construct the full path to the item folder
                item_folder_path = os.path.join(catalog_path, item_folder_name)

                # Access files within the item folder
                for file_name in os.listdir(item_folder_path):
                    # Check if the file is a JSON file
                    if file_name.endswith('-item.json'):
                        file_path = os.path.join(item_folder_path, file_name)

                        # Example: Read the content of JSON file
                        with open(file_path, 'r') as json_file:
                            item_data = json.load(json_file)

                            # Check if the 'properties' key is present and is a dictionary
                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                # Check if any of the selectedItems is present in the 'properties' values
                                properties_values = item_data['properties'].values()
                                if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                    print("File path:", file_path)
                                    formatted_item = format_item_data(item_data)
                                    items.append(formatted_item)

        # Return the list of items matching the specified keys along with the count
        response_data = {"data": items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# function for the search of side bar year  data
@api_view(['GET'])
def sb_year(request, **kwargs):
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []

        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Iterate through each item folder in the catalog
        for item_folder_name in os.listdir(catalog_path):
            # Check if the folder name is in the expected format
            if item_folder_name.endswith('-item'):
                # Construct the full path to the item folder
                item_folder_path = os.path.join(catalog_path, item_folder_name)

                # Access files within the item folder
                for file_name in os.listdir(item_folder_path):
                    # Check if the file is a JSON file
                    if file_name.endswith('-item.json'):
                        file_path = os.path.join(item_folder_path, file_name)

                        # Example: Read the content of JSON file
                        with open(file_path, 'r') as json_file:
                            item_data = json.load(json_file)

                            # Check if the 'properties' key is present and is a dictionary
                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                # Check if any of the selectedItems is present in the 'properties' values
                                properties_values = item_data['properties'].values()
                                if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                    print("File path:", file_path)
                                    formatted_item = format_item_data(item_data)
                                    items.append(formatted_item)

        # Return the list of items matching the specified keys along with the count
        response_data = {"data": items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# function for the search of sode bar collection data
@api_view(['GET'])
def sb_collection(request, **kwargs):
  #  try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []

        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Iterate through each item folder in the catalog
        for item_folder_name in os.listdir(catalog_path):
            # Check if the folder name is in the expected format
            if item_folder_name.endswith('-item'):
                # Construct the full path to the item folder
                item_folder_path = os.path.join(catalog_path, item_folder_name)

                # Access files within the item folder
                for file_name in os.listdir(item_folder_path):
                    if file_name.endswith('-item.json'):
                        file_path = os.path.join(item_folder_path, file_name)

                    with open(file_path, 'r') as json_file:
                        item_data = json.load(json_file)

                        if 'properties' in item_data and isinstance(item_data['properties'], dict):
                            properties_values = item_data['properties'].values()
                            if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                formatted_item = format_item_data(item_data)
                                items.append(formatted_item)
                                    
        # Return the list of items matching the specified keys along with the count
        response_data = {"data": items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)

  #  except Exception as e:
        # Handle exceptions and return an error response
      #  error_message = str(e)
      #  return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# function for the search of sode bar collection data
@api_view(['GET'])
def sb_subcollection(request, **kwargs):
    try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []

        # Get the list of selectedItems from query parameters
        query_params = request.GET.getlist('selectedItems')
        key_list = [param.replace('%20', ' ') for param in query_params]

        # Iterate through each item folder in the catalog
        for item_folder_name in os.listdir(catalog_path):
            # Check if the folder name is in the expected format
            if item_folder_name.endswith('-item'):
                # Construct the full path to the item folder
                item_folder_path = os.path.join(catalog_path, item_folder_name)

                # Access files within the item folder
                for file_name in os.listdir(item_folder_path):
                    if file_name.endswith('-item.json'):
                        file_path = os.path.join(item_folder_path, file_name)

                    with open(file_path, 'r') as json_file:
                        item_data = json.load(json_file)

                        if 'properties' in item_data and isinstance(item_data['properties'], dict):
                            properties_values = item_data['properties'].values()
                            if any(str(key).lower() in str(value).lower() for key in key_list for value in properties_values):
                                formatted_item = format_item_data(item_data)
                                items.append(formatted_item)
                                    
        # Return the list of items matching the specified keys along with the count
        response_data = {"data": items, "count": len(items)}
        return Response(response_data, status=status.HTTP_200_OK)

    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




# To manipulate the response that coming in properties for all side search we are use this function
def format_item_data(item_data):
    """
    Function to format an individual item based on the specified structure.
    """
    formatted_item = {
        "Major": item_data['properties']['major'],
        "Submajor": item_data['properties']['submajor'],
        "Minor": item_data['properties']['minor'],
        "SubMinor": item_data['properties']['subminor'],
        "Grade": item_data['properties']['grade'],
        "File_formats": item_data['properties']['file_formats'],
        "Type": item_data['properties']['type'],
        "source_description": item_data['properties']['source_description'],
        "place_city": item_data['properties']['place_city'],
        "year": item_data['properties']['year'],
        "publisher": item_data['properties']['publisher'],
        "path": item_data['properties']['path'],
        "collection": item_data['properties']['collection'],
        "collection_type": item_data['properties']['collection_type'],
        "soi_toposheet_no": item_data['properties']['soi_toposheet_no'],
      #  "grade1": item_data['properties']['grade1'],
        "data_resolution": item_data['properties']['data_resolution'],
        "ownership": item_data['properties']['ownership'],
        "is_processed": item_data['properties']['is_processed'],
        "short_descr": item_data['properties']['short_descr'],
        "descr": item_data['properties']['descr'],
        "img_service": item_data['properties']['img_service'],
        "img_dw": item_data['properties']['img_dw'],
        "map_service": item_data['properties']['map_service'],
        "map_dw": item_data['properties']['map_dw'],
        "publish_on": item_data['properties']['publish_on'],
        "thumbnail": item_data['properties']['thumbnail'],
        "source": item_data['properties']['source'],
      #  "created_id": item_data['properties']['created_id'],
        "created_date": item_data['properties']['created_date'],
     #   "modified_id": item_data['properties']['modified_id'],
      #  "modified_date": item_data['properties']['modified_date'],
    #    "deleted_id": item_data['properties']['deleted_id'],
      #  "deleted_date": item_data['properties']['deleted_date'],
         "img_vis_url":item_data['properties']['img_vis_url'],
         "img_download_url":item_data['properties']['img_download_url'],
        "shp_file_url":item_data['properties']['shp_file_url'],
        "urlalias":item_data['properties']['urlalias'],
        
    }
    return formatted_item


from django.http import JsonResponse

# Assuming your function looks something like this
def search_side_bar(request):
   # try:
        # Path to the STAC catalog
        catalog_path = "./stac-catalog"

        # List to store items
        items = []

        # Iterate through each item folder in the catalog
        for item_folder_name in os.listdir(catalog_path):
            # Check if the folder name is in the expected format
            if item_folder_name.endswith('-item'):
                

                # Construct the full path to the item folder
                item_folder_path = os.path.join(catalog_path, item_folder_name)
              
                # Access files within the item folder
                for file_name in os.listdir(item_folder_path):
                  

                    # Check if the file is a JSON file
                    if file_name.endswith('-item.json'):
                        file_path = os.path.join(item_folder_path, file_name)
                       

                        # Example: Read the content of JSON file
                        with open(file_path, 'r') as json_file:
                            item_data = json.load(json_file)
                            print("-----------------",item_data)
                            # Check if the specified key is present in the properties section
                            if 'properties' in item_data and isinstance(item_data['properties'], dict):
                                properties_values = item_data['properties'].values()
                                #if any(str(key_to_search).lower() in str(value).lower() for value in properties_values):
                                print("File path:", file_path)
                                items.append(item_data)
        # Initialize a dictionary to organize items based on properties
        data = {
            'major': [],
            'submajor': [],
            'minor': [],
            'subminor': [],
            'grade': [],
            'publisher': [],
            'place_city': [],
            'year': [],
            # Add more categories as needed
        }

        # Iterate through each item in your response
        # Iterate through each item in your response
        for item in items:
            for key in data.keys():
                if key in item['properties']:
                    subhead_value = item['properties'][key]
                    # Check if a dictionary with the same subhead already exists in the list
                    subhead_dict = next((d for d in data[key] if d['subhead'] == subhead_value), None)
                    if subhead_dict:
                        # Increment the count if the subhead exists
                        subhead_dict['count'] += 1
                    else:
                        # Add a new dictionary if the subhead doesn't exist
                        data[key].append({'subhead': subhead_value, 'count': 1})
            # Add more conditions for other properties

        # Return the organized data as JSON response
        return JsonResponse(data)

   # except Exception as e:
        # Handle exceptions and return an error response
      #  error_message = str(e)
      #  return JsonResponse({"error": error_message}, status=500)
    


def search_catalog_metadata_for_combined_response(request, query, **kwargs):
    # Path to the STAC catalog
    catalog_path = "./stac-catalog"

    # List to store items
    items = []

    # Iterate through each item folder in the catalog
    for item_folder_name in os.listdir(catalog_path):
        # Check if the folder name is in the expected format
        if item_folder_name.endswith('-item'):
            # Construct the full path to the item folder
            item_folder_path = os.path.join(catalog_path, item_folder_name)

            # Access files within the item folder
            for file_name in os.listdir(item_folder_path):
                # Check if the file is a JSON file
                if file_name.endswith('-item.json'):
                    file_path = os.path.join(item_folder_path, file_name)

                    # Example: Read the content of JSON file
                    with open(file_path, 'r') as json_file:
                        item_data = json.load(json_file)

                        # Check if the specified key is present in the properties section
                        if 'properties' in item_data and isinstance(item_data['properties'], dict):
                            properties = item_data['properties']

                            # Check if any value in properties matches the query
                            # Check if any key-value pair in properties matches any key-value pair in query
                            # Check if query is a string and matches any value in properties
                            if isinstance(query, str) and any(
                                str(query).lower() in str(value).lower() for value in properties.values()
                            ):
                                response_data = {
                                    "major": properties.get("major", ""),
                                    "Submajor": properties.get("submajor", ""),
                                    "Minor": properties.get("minor", ""),
                                    "SubMinor": properties.get("subminor", ""),
                                    "Grade": properties.get("grade", ""),
                                    "File_formats": properties.get("file_formats", ""),
                                    "Type": properties.get("type", ""),
                                    "Source_Description": properties.get("source_description", ""),
                                    "place_city": properties.get("place_city", ""),
                                    "year": properties.get("year", ""),
                                    "publisher": properties.get("publisher", ""),
                                    "Path": properties.get("path", ""),
                                    "Collection": properties.get("collection", ""),
                                    "Collection_type": properties.get("collection_type", ""),
                                    "SOI_toposheet_no": properties.get("soi_toposheet_no", ""),
                                    "Data_Resolution": properties.get("data_resolution", ""),
                                    "Ownership": properties.get("ownership", ""),
                                    "is_processed": properties.get("is_processed", ""),
                                    "short_descr": properties.get("short_descr", ""),
                                    "descr": properties.get("descr", ""),
                                    "img_service": properties.get("img_service", ""),
                                    "img_dw": properties.get("img_dw", ""),
                                    "map_service": properties.get("map_service", ""),
                                    "map_dw": properties.get("map_dw", ""),
                                    "publish_on": properties.get("publish_on", ""),
                                    "thumbnail": properties.get("thumbnail", ""),
                                    "source": properties.get("source", ""),
                                    "created_date": properties.get("created_date", ""),
                                    "img_vis_url":properties.get("img_vis_url", ""),
                                    "img_download_url":properties.get("img_download_url", ""),
                                    "shp_file_url":properties.get("shp_file_url", ""),
                                    "urlalias":properties.get("urlalias", ""),  
                                                                 }
                                items.append(response_data)

    # Return the list of items matching the specified key as JsonResponse
    return JsonResponse(items, safe=False)

def search_sidebar_for_combined_response(request, query, **kwargs):
    # Path to the STAC catalog
    catalog_path = "./stac-catalog"

    # List to store items
    items = []

    # Iterate through each item folder in the catalog
    for item_folder_name in os.listdir(catalog_path):
        # Check if the folder name is in the expected format
        if item_folder_name.endswith('-item'):
            # Construct the full path to the item folder
            item_folder_path = os.path.join(catalog_path, item_folder_name)

            # Access files within the item folder
            for file_name in os.listdir(item_folder_path):
                # Check if the file is a JSON file
                if file_name.endswith('-item.json'):
                    file_path = os.path.join(item_folder_path, file_name)

                    # Example: Read the content of JSON file
                    with open(file_path, 'r') as json_file:
                        item_data = json.load(json_file)

                        # Check if the specified key is present in the properties section
                        if 'properties' in item_data and isinstance(item_data['properties'], dict):
                            properties = item_data['properties']

                            # Check if any value in properties matches the query
                            # Check if any key-value pair in properties matches any key-value pair in query
                            # Check if query is a string and matches any value in properties
                            if isinstance(query, str) and any(
                                str(query).lower() in str(value).lower() for value in properties.values()
                            ):
                                items.append(item_data)
            # Initialize a dictionary to organize items based on properties
    data = {
            'major': [],
            'submajor': [],
            'minor': [],
            'subminor': [],
            'grade': [],
            'publisher': [],
            'place_city': [],
            'year': [],
            # Add more categories as needed
        }

        # Iterate through each item in your response
        # Iterate through each item in your response
    for item in items:
            for key in data.keys():
                if key in item['properties']:
                    subhead_value = item['properties'][key]
                    # Check if a dictionary with the same subhead already exists in the list
                    subhead_dict = next((d for d in data[key] if d['subhead'] == subhead_value), None)
                    if subhead_dict:
                        # Increment the count if the subhead exists
                        subhead_dict['count'] += 1
                    else:
                        # Add a new dictionary if the subhead doesn't exist
                        data[key].append({'subhead': subhead_value, 'count': 1})
            # Add more conditions for other properties

        # Return the organized data as JSON response
    return JsonResponse(data)


###### In this function for main page we combine the two function 
## to give response in combined format
@api_view(['GET'])
def combined_response(request, query):
    try:
        # Call the first function to get the search results
        search_results = search_catalog_metadata_for_combined_response(request, query)

        # Call the second function to get the sidebar data
        sidebar_data = search_sidebar_for_combined_response(request,query)

        # Convert JsonResponse objects to dictionaries
        search_results_dict = json.loads(search_results.content)
        sidebar_data_dict = json.loads(sidebar_data.content)

    #    Return the responses separately
        return JsonResponse({
            'ms_data': search_results_dict,
            'sb_data': sidebar_data_dict
        })
      
    except Exception as e:
        # Handle exceptions and return an error response
        error_message = str(e)
        return JsonResponse({"error": error_message}, status=500)

   

    return Response({'ms_data': search_results})
