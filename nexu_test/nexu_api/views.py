from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from nexu_api import serializers, models

# Create your views here.
class ApiViewBrand(APIView):
    idModelsSerializer = serializers.idModelsSerializer
    betweenModelsSerializer = serializers.betweenModelsSerializer
    ModelsSerializer = serializers.ModelsSerializer
    def get(self,request):
        brands = models.Models.objects.distinct('brand_name')
        bsList =[]
        for b in brands.objects:
            r = {
                'id' : b.id,
                'name' :b.name,
                'avg_price' : b.avg_price,
                'brand_name' : b.brand_name,
                }
            bsList.append(r)
        return Response(bsList)


    def post(self,request):
        ser = self.ModelsSerializer(data= request.data)
        if ser.is_valid():
            id =  ser.validated_data.get('id')
            name = ser.validated_data.get('name')
            brand = models.Models.objects.filter(id=id).brand_name
            count= models.Models.objects.filter(brand_name=brand & name != name ).aggregate(num= Count('name'))
            if count[0].num == 0:
                new = models.Models(name= name, brand_name = brand, avg_price = 0)
                new.save()
            return Response(bsList)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiViewModel(APIView):
    def get(self,request):
        ser = self.betweenModelsSerializer(data= request.data)
        if ser.is_valid():
            greater =  ser.validated_data.get('greater')
            lower = ser.validated_data.get('lower')
            brands = models.Models.objects.filter(avg_price=(lower,greater))
            for b in brands:
                r = {
                    'id' : b.id,
                    'name' :b.name,
                    'avg_price' : b.avg_price,
                    'brand_name' : b.brand_name,
                    }
                bsList.append(r)
            return Response(bsList)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self,request):
        ser = self.idModelsSerializer(data= request.data)
        if ser.is_valid():
            id =  ser.validated_data.get('id')
            model= models.Models.objects.filter(id=id)
            cars = models.Models.objects.filter(name=model.name & avg_price>0 )
            avg = cars.aggregate(Avg('brand_name'))
            model.update(avg_price = avg['brand_name__avg'])
            return Response({'avg_price': avg['brand_name__avg']})

        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)
