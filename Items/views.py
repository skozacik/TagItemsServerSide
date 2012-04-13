
import json
import urllib
from django.http import HttpResponse
from django.core import serializers
from django.utils.encoding import smart_str, smart_unicode
from Items.models import *
from TagItems.local_settings import *
from django.views.decorators.csrf import csrf_exempt

def barcode(request,barcode):
    try:
      bcstored=Item.objects.get(bc=barcode)
      JSONserializer=serializers.get_serializer("json")
      json_serializer=JSONserializer();
      response=HttpResponse()
      json_serializer.serialize(Beer.objects.filter(bc=barcode),stream=response,use_natural_keys=True)
      return response
    except Item.DoesNotExist:
    
      baseurl="https://www.googleapis.com/shopping/search/v1/public/products?key="
      baseurl+=key;
      baseurl+="&&country=US&q=" 
      baseurl+=smart_str(barcode);
      baseurl+="&alt=json";
    
      result=json.load(urllib.urlopen(baseurl));
      
      resp='Not in DataBase yet using google shopper name'
      try:
        p=Item(bc=long(barcode),name=smart_str(result["items"][0]["product"]["title"]),maker=smart_str(result["items"][0]["product"]["brand"]),imageurl=result["items"][0]["product"]["images"][0]["link"],rating=0,raters=0)
        p.save()  
        JSONserializer=serializers.get_serializer("json")
        json_serializer=JSONserializer();
        response=HttpResponse()
        json_serializer.serialize(Item.objects.filter(bc=barcode),stream=response,use_natural_keys=True)
      except KeyError:
        response="Not Found by google shopper"
      return response

def rated(request,barcode,rating):
  rated=Item.objects.get(bc=barcode)
  rated.rating=(int(rating)+rated.rating*rated.raters)/(rated.raters+1)
  rated.raters=rated.raters+1
  rated.save()
  return HttpResponse(smart_str(rated.rating))

@csrf_exempt
def search(request):
   searchterms=smart_str(request.POST.keys()[0])
   searchvalue=smart_str(request.POST.values()[0])
   kwargs={}
   kwargs[searchterms+"__search"] = searchvalue 
   search=Item.objects.filter(**kwargs)
   JSONserializer=serializers.get_serializer("json")
   json_serializer=JSONserializer()
   response=HttpResponse()
   json_serializer.serialize(search,stream=response)
   if (len(search)):
     return response
   try:
     baseurl="https://www.googleapis.com/shopping/search/v1/public/products?key="
     baseurl+=key;
     baseurl+="&&country=US&q="   
     baseurl+=searchvalue
     baseurl+="&alt=json";
     result=json.load(urllib.urlopen(baseurl));
     i=0
     for item in result["items"]:
       try:
         p=Item(bc=long(item["product"]["gtin"]),name=smart_str(item["product"]["title"]),maker=smart_str(item["product"]["brand"]),imageurl=item["product"]["images"][i]["link"],rating=0,raters=0) 
         p.save()  
       except KeyError:
         p=Item(bc=123456,name=smart_str(item["product"]["title"]),maker=smart_str(item["product"]["brand"]),imageurl=item["product"]["images"][i]["link"],rating=0,raters=0)
         p.save()
    
     JSONserializer=serializers.get_serializer("json")
     json_serializer=JSONserializer();
     response=HttpResponse()
     json_serializer.serialize(Item.objects.filter(name__search=searchvalue),stream=response,use_natural_keys=True)
     #return barcode
   except KeyError :
   #  response=HttpResponse("Key Error on" +
    return response
       # return HttpResponse("Key Error") 
   return response
@csrf_exempt
def tagpost(request,barcode):
  tag=smart_str(request.POST["tag"]);
  try:
    
    tagged=Item.objects.get(bc=barcode,review__tag=tag)
    tagged2=tagged.review.get(tag=tag)
    tagged2.votes=tagged2.votes+1
    tagged2.save()
    tagged.save()
    return HttpResponse(tagged2.votes)
  except Item.DoesNotExist:
    tagged=Item.objects.get(bc=barcode)
    tagobj=Reviews.objects.create(votes=1,tag=tag)#make a new many to many object
    tagged.review.add(tagobj)#append as if to a list

    tagged.save()#save object
  return HttpResponse("tagged")



