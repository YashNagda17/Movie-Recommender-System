from django.shortcuts import render
from django.http import JsonResponse
from forming.models import movies
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import movie_serializer
from .ml_code import Predictions

# Create your views here.

@api_view(['GET','POST'])

def default_page(request):
    

    if request.method == 'GET':
        title = request.GET.get('title')
        
        if (title==None):
            if (request.path) == '/not/':
                data = movies.objects.order_by('movieId').values()
            else:
                data = movies.objects.order_by('?').values()
            
            serialize_data = movie_serializer(data,many=True)
    
        else:

            data = movies.objects.filter(title__icontains = title).values()
            
            if (len(data)==0):  ## Check len = 0 and len  = 1 
                data = movies.objects.filter(movieId__in = [1,2]).values()
                serialize_data = movie_serializer(data,many=True)
            
            elif (len(data)==1):
                data1 = movies.objects.filter(movieId__in = [1]).values()
                data = data | data1  
                serialize_data = movie_serializer(data,many=True)
            
            else:
                serialize_data = movie_serializer(data,many=True)

        
        return Response(serialize_data.data)
    
    if request.method == 'POST':
        dct = {}
        k = request.data
        
        n = len(k)
        for i in k:
            dct[i['title']] = i['rating']
        
         

        pred = Predictions(dct)
        p = pred.run()
        
        data = movies.objects.filter(movieId__in = p)
        data = sorted(data, key=lambda i: p.index(i.pk))
        
        
        serialize_data = movie_serializer(data,many=True)
        fin = serialize_data.data
        
        return Response(fin)




@api_view()
def something_fishy(request):
    return Response("I Could not understand that! Use GET or Post Method")



