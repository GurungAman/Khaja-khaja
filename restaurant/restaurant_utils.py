from .serializers import MenuSerializer

def menu_details(data):
    response = []
    for i in data:
        json_data = {}
        menu_serializer= MenuSerializer(i)
        json_data = menu_serializer.data
        json_data['total_items'] = i.menu.all().count()
        response.append(json_data)
    return response

