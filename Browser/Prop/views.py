from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json
from Prop import completeexperiment
import pandas as pd
from multiprocessing import Process
import time
from Prop.DownloadTextVideoImage import *
from django.views.decorators.csrf import csrf_exempt

df_images = pd.DataFrame(columns = [ 'title', 'description'])   
df_doc = pd.DataFrame(columns = ['link', 'title', 'short_description' ,'description']) 
df_video = pd.DataFrame(columns = ['link', 'title', 'description'])        


@csrf_exempt
def index(request):
  content = {'query':" "}
  return render(request,"searchbtn.html",content)


def runText(terms):
  df_doc=completeexperiment.loadText_Text(terms)
  print("df_doc herer in view ",df_doc)
  df_doc.to_csv('df_doc_filename.csv', index = False)


def runImage(terms):
  df_images=completeexperiment.loadText_ImagesNew(terms)
  df_images.to_csv('df_images_filename.csv', index = False)
  #print("View image :",df_images)


def runVideo(terms):
  df_video=completeexperiment.loadText_VideoNew(terms)
  df_video.to_csv('df_video_filename.csv', index = False)
  #print("View Video saved: ",df_video)


query=""

def search2(request):

  inp_value = request.GET.get('input_query', 'This is a default value')
  print("Query: : : "+ inp_value)
  global query
  query=inp_value
  p1=Process(target=runText,args=(query,))
  p2=Process(target=runImage,args=(query,))
  p3=Process(target=runVideo,args=(query,))

  p2.start()
  p1.start()
  p3.start()
  p1.join()
  p2.join()
  p3.join()
  p1.terminate()
  p2.terminate()
  p3.terminate()

  completeexperiment.generateSummary_Text()
  df_images=pd.read_csv('/content/drive/MyDrive/Browser/df_images_filename.csv')
  df_doc=pd.read_csv('/content/drive/MyDrive/Browser/df_doc_filename.csv')
  df_video=pd.read_csv('/content/drive/MyDrive/Browser/df_video_filename.csv')
  completeexperiment.extractImportantSentences_video(df_video)
  completeexperiment.extractImportantSentences_text(df_doc)
  completeexperiment.extractImportantSentences_image(df_images)


  listt=completeexperiment.findSimilarityBetweenQueryAndQueries(query)
  print("Tota Relevant Sentences : ",len(listt))

  callRetrivalMethod=True
  content = {'query':query, 'dect':listt,'callRetrivalMethod':callRetrivalMethod}

  # check="click"
  # pageName="search2"
  # print("variable set search2 call")
  # content = {'variable':inp_value,'clickorNot':check, 'pageName':pageName}
  
  return render( request, 'index.html', content)


def search3(request):
  df_images=pd.read_csv('/content/drive/MyDrive/Browser/df_images_filename.csv')
  df_doc=pd.read_csv('/content/drive/MyDrive/Browser/df_doc_filename.csv')
  df_video=pd.read_csv('/content/drive/MyDrive/Browser/df_video_filename.csv')
  completeexperiment.extractImportantSentences_video(df_video)
  completeexperiment.extractImportantSentences_text(df_doc)
  completeexperiment.extractImportantSentences_image(df_images)


  listt=completeexperiment.findSimilarityBetweenQueryAndQueries(query)
  #print("len of list tow show : ",len(listt))
  content = {'query':query, 'dect':listt}
  return render(request,"index.html",content)



@csrf_exempt
def create(request):
  print("call method")
  if request.method=="POST":
    name_val=request.POST['name']
    print(name_val)
    
    success=GoogleSpider().search(name_val)
    print(success)
    #dfjson=df_json = df_text.to_json()
    #list1=["hellow this is one","hellow this is two","hellow this is three and four"]
    #success={'lis1':list1,'value2':'Valueof the second'}
    #success={'value2':"this is secondvariable",'lis1':dfjson}
    return HttpResponse( json.dumps( success ) )

@csrf_exempt
def imageTab(request):
  if request.method=="POST":
    name_val=request.POST['name']
    print(name_val)
   
    success=GoogleSpider.imagesData(name_val)
    print(success)
    #dfjson=df_json = df_text.to_json()
    #list1=["hellow this is one","hellow this is two","hellow this is three and four"]
    #success={'lis1':list1,'value2':'Valueof the second'}
    #success={'value2':"this is secondvariable",'lis1':dfjson}
    return HttpResponse( json.dumps( success ) )    


@csrf_exempt
def videoTab(request):
  if request.method=="POST":
    name_val=request.POST['name']
    print("Name :",name_val)
    try:
      success=GoogleSpider.PresentVideo(name_val)    
    except Exception as e:
      print("error ",e )
    print("Error finding...")
    return HttpResponse( json.dumps( success ) ) 

