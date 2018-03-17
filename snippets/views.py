from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
# from getDataFromMlab import getUserLocation
from snippets.getDataFromMlab import getUserLocation
import json
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SnippetSerializer(data=request.data)
        # print(serializer[0])
        # if request.data.keys() == 'longtitude':
        # a = request.data.keys()
        # print(a)
        if serializer.is_valid():
            print(type(serializer.data))
            # print(serializer.data['latitude'])
            if not serializer.data:
                print("data Null")
            # name , data = serializer.data.iteritems()
            # print(name,data)
            # elif serializer.data['latitude'] == None or serializer.data['longtitude'] == None:
            #     print("some data Null")
            # elif serializer.data.iteritems
            else:
                # print(serializer.data.iteritems)
                # getUserLocation.getCoworkingForRecommendation(serializer.data)
                result = getUserLocation.getCoworkingForRecommendation(serializer.data)
                resultRecomment = json.loads(result)
                # a = [{'longtitude':12313.432423,'latitude':23.34242423}]
                return Response(resultRecomment, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)