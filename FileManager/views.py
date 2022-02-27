from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
import json
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

@api_view(('POST',))
@csrf_exempt
def handle_file_upload(request):
    # if request.method == "POST":
    folder_name=request.POST.get("folder")
    topics_name=request.POST.get("topic")
    topics=topics_name.split(",")  

    files=request.FILES.getlist('file')

    if folder_name=="":
        return Response({"Msg":"NO folder Name"},status=status.HTTP_400_BAD_REQUEST)  

    if len(files)==0:
        return Response({"Msg":"file not found"},status=status.HTTP_400_BAD_REQUEST)


    for file in files: 
        f=file.name
        filename=(f.split('.')[0])
        try:
            folder_name_accrd_file=list(Folder.objects.filter(file__file_name__iexact=filename).values())[0]  
            if folder_name_accrd_file.get('folder_name') == folder_name :
                return Response({"st":"same file exist in same folder"},status=status.HTTP_400_BAD_REQUEST)
        except:
            pass
        for topic_name in topics:
            try:
                topic_obj=Topics.objects.get(topic_name__iexact=topic_name)
            except ObjectDoesNotExist:
                topic_obj=Topics(topic_name=topic_name)
                topic_obj.save()
            finally:
                try :
                    file_obj= FileUpload.objects.get(file_name__iexact=filename)
                except:
                    file_obj=FileUpload(file_name=filename,file=file,file_size=file.size,file_type=file.content_type)
                    file_obj.save()
                finally:
                    file_obj.file_topic.add(topic_obj)

            try :
                folder_obj=Folder.objects.get(folder_name=folder_name) 
            except:
                folder_obj=Folder(folder_name=folder_name,files_no=0)
                folder_obj.save()
            finally: 
                folder_obj.file.add(file_obj)

    content = {'Msg': 'The file has been inserted'}
    return Response(content, status=status.HTTP_200_OK)
        
    # else : 
        # folder_name='test'

        # # get files by folder name 
        # files_all=FileUpload.objects.filter(file_name='sql_help.txt')
        # json_obj=FileSerializers(files_all,many=True) 

        # # get folders by file name
        # folder_all = Folder.objects.filter(file__file_name__iexact='sql_help.txt')
        # json_folder=FolderSerializers(folder_all,many=True)

        # topic_all=Topics.objects.all()
        # json_topics=TypesSerializers(topic_all,many=True)
        # return Response({},status=status.HTTP_200_OK)

@api_view(['POST'])
@csrf_exempt
def file_search_handle(request): 
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode) 
    folder_name=body.get("folder_name")
    document_topics=body.get("topic")
    file_names=body.get("file_name")
        
    final_response=[]
    topic_id=[]

    if folder_name is "" and len(document_topics)==0 and len(file_names)==0:
        return Response({"st":"no body found"},status=status.HTTP_400_BAD_REQUEST)

    elif folder_name is "" and len(document_topics)!=0 and len(file_names)==0:
        try:
            for tp in document_topics:
                t=FileUpload.objects.filter(file_topic__topic_name__iexact=tp)
                final_response.append(FileSerializers(t,many=True).data) 
            if len(final_response[0])==0:
                return Response({"st":"no such file found"},status=status.HTTP_400_BAD_REQUEST)
            return Response(final_response,status=status.HTTP_200_OK)
        except:
            return Response({"st":"no such file found"},status=status.HTTP_400_BAD_REQUEST)

    elif folder_name is not "" and len(document_topics)!=0 and len(file_names)==0:
        try:
            for tp in document_topics:
                t=FileUpload.objects.filter(file_topic__topic_name__iexact=tp).filter(f2f__folder_name__iexact=folder_name)
                final_response.append(FileSerializers(t,many=True).data) 
            if len(final_response[0])==0:
                return Response({"st":"no such file found"},status=status.HTTP_400_BAD_REQUEST)
            return Response(final_response,status=status.HTTP_200_OK)
        except:
            return Response({"st":"no such file found"},status=status.HTTP_400_BAD_REQUEST)

    elif folder_name is not "" and len(document_topics)==0 and len(file_names)==0:
        try: 
            t=FileUpload.objects.filter(f2f__folder_name__iexact=folder_name)
            final_response.append(FileSerializers(t,many=True).data) 
            if len(final_response[0])==0:
                return Response({"st":"no such file found"},status=status.HTTP_400_BAD_REQUEST)
            return Response(final_response,status=status.HTTP_200_OK)
        except:
            return Response({"st":"no such file found"},status=status.HTTP_400_BAD_REQUEST)


    if len(document_topics)!=0:
        for doc_top in document_topics:
            try:
                tp=Topics.objects.get(topic_name__iexact=doc_top)
                topic_id.append(tp.id)
            except:
                pass
    for f_name in file_names:
        try:
            if folder_name is "": 
                file_obj1=FileUpload.objects.filter(file_name__iexact=f_name) 
            else:
                file_obj1=FileUpload.objects.filter(file_name__iexact=f_name).filter(f2f__folder_name__iexact=folder_name) 

            file_topics_all_dict=list(Topics.objects.filter(topics__file_name__iexact=f_name).values('id'))

            file_topics_all=[]
            for f_t in file_topics_all_dict:
                file_topics_all.append(f_t.get("id"))
            json_doc1=FileSerializers(file_obj1,many=True) 
            print(file_topics_all,topic_id)
            intersection_set = set.intersection(set(file_topics_all), set(topic_id))
            common_topic_ids=len(list(intersection_set))

            if common_topic_ids > 0 or len(document_topics)==0 :
                final_response.append(json_doc1.data)
        except: 
            return Response({"st":"server error"},status=status.HTTP_503_SERVICE_UNAVAILABLE) 
    return Response(final_response,status=status.HTTP_200_OK) 
        
        
@api_view(['delete'])
@csrf_exempt
def delete(request):
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode) 
    folder_name=body.get("folder_name") 
    file_names=body.get("file_name")

    if folder_name!="" and len(file_names)==0:
        try:
            folder_qury_set=Folder.objects.filter(folder_name__iexact=folder_name)
            if folder_qury_set is not None:  
                folder_qury_set.delete()  
                return Response({"msg":"folder removed successfully"},status=status.HTTP_200_OK)
        except:
            return Response({"msg":"such folder doest not exist."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)




    elif folder_name=="" and len(file_names)!=0:
        success_file_names=[]
        for file in file_names: 
            try:
                file_query_set=FileUpload.objects.filter(file_name__iexact=file)
                print(file_query_set)
                if file_query_set.exists():  
                    success_file_names.append(file)
                    file_query_set.delete()   
            except:
                continue
        if len(success_file_names)==0:
            return Response({"msg":"such folder doest not exist."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"deleted_files":success_file_names,"msg":"files delete successfully.x"},status=status.HTTP_200_OK)



    elif folder_name=="" and len(file_names)==0:
        return Response({"msg":"no body found."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    elif folder_name!="" and len(file_names)!=0:
        success_file_names=[]
        try:
            folder_qury_set=Folder.objects.filter(folder_name__iexact=folder_name)
            if folder_qury_set.exists():  
                print(folder_qury_set)  
                for file in file_names: 
                    # if there exists any files according to that folder name
                    folder_file_rel_query=FileUpload.objects.filter(f2f__folder_name__iexact=folder_name).filter(file_name__iexact=file)
                    try:
                        if list(folder_file_rel_query.values())[0] is not None:
                            # file exists with same folder name
                            # chcek this file is related with other folder if not delet it otherwise unlink it from current floder
                            folder_find_status=Folder.objects.filter(file__file_name__iexact=file).filter(~Q(folder_name__iexact=folder_name)).exists() 
                            if folder_find_status is False:
                                # no link with other folder delete successfully
                                FileUpload.objects.filter(file_name__iexact=file).delete() 
                            success_file_names.append(file)
                    except:
                        pass 
                folder_qury_set.delete()
                # return the file name which cann be sucessfully deleted
                return Response({"deleted_files":success_file_names,"msg":"folder and files delete successfully."},status=status.HTTP_200_OK)
            else:
                return Response({"msg":"such folder doest not exist."},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except:
            print("hii")
            return Response({"msg":"such folder/files doest not exist."},status=status.HTTP_500_INTERNAL_SERVER_ERROR) 