from . import Timer
import json
from rest_framework import generics,status
from .permissions import JWTAuthentication
from .models import Team,Progress,Question
from rest_framework.response import Response
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import redirect   
from django.http import JsonResponse

''' 
Life_line Flag -->
 1 -> no lifeline is currently activated
 2 -> lifeline 1 is currently activated
 3 -> lifeline 2 is currently activated
 4 -> lifeline 3 is currently activated 
'''


#conditions remaining

#lifeline 1
def Amplifier(progress):
    if (progress.lifeline1 == False and progress.isAttemptedFirst == False):
        progress.lifeline_flag = 2
        progress.isAttemptedFirst = True
        progress.lifeline1 = True
        progress.save()
    else :
        return Response({"error": "Lifeline is already used or can't use right now"}, status=status.HTTP_406_NOT_ACCEPTABLE)

#lifeline 2
def Freezer(progress,issubmit = False):
    if ( not progress.lifeline2 and progress.lifeline1):
        progress.lifeline2 = True
        progress.lifeline_flag = 3
        progress.start_time = timezone.now()
        progress.save()
    elif progress.lifeline_flag == 3:

        time_delta = ((timezone.now() - progress.start_time).total_seconds())//10
        print("time delta = ",time_delta)
        print("time now = ",timezone.now().timestamp())

        if (time_delta >= 6 or issubmit ):
            progress.lifeline_flag = 1
            print("end_time before=> ",progress.end_time.timestamp())
            progress.end_time += timezone.timedelta(seconds=(time_delta * 9))
            print("end_time after=> ",progress.end_time.timestamp())

            progress.save()
            return JsonResponse(
                {
                'hours': -1,
                'minutes': -1,
                'seconds': -1
            }
            )
     
        time_remaining = progress.end_time - progress.start_time - timezone.timedelta(seconds=time_delta)
        print("time remaing = ",time_remaining)
        time_data = Timer.Timer(time_remaining)

        return JsonResponse(time_data)
    else :
        return Response({"error": "Lifeline is already used or can't use right now"}, status=status.HTTP_406_NOT_ACCEPTABLE)

def Poll(progress):
    progress.lifeline_flag = 4 
    questions_data = (progress.question_list).split(',')
    que_id = questions_data[progress.current_question-1]
    question = Question.objects.get(question_id = que_id)
    responses = json.loads(question.responses)
    return responses

class GetLifeline1(generics.ListAPIView):
    permission_classes = [JWTAuthentication]

    def get(self, request):
        lifeline_no = request.query_params.get('lifeline',default = "NONE")
        try:
            team = Team.objects.get(Q(user1=request.user) | Q(user2=request.user))
            progress = Progress.objects.get(team = team)
        except Team.DoesNotExist:
            return Response({"error": "Team not found for the authenticated user"}, status=status.HTTP_404_NOT_FOUND)
        except Progress.DoesNotExist:
            return Response({"error": "Team not found for the authenticated user"}, status=status.HTTP_404_NOT_FOUND)
        if (lifeline_no == "aqua_point"):
            Amplifier(progress)
        elif (lifeline_no == "time_freeze"):
            context = Freezer(progress)
            if (context):
                return context
        elif (lifeline_no == "poll"):
            context = Poll(progress)
            if (context):

                return Response(context)
        return redirect('get_question')
        



def save_response(question,answer):
    response_answer = str(answer)
    responses = json.loads(question.responses)
    if (response_answer in responses):
        responses[response_answer] +=1
    else :
        responses[response_answer] =1
    question.responses = json.dumps(responses)
    question.save()


def reset_lifelines(progress):
    if(progress.lifeline_flag == 3 ):
        Freezer(progress,True) 
    else:
        progress.lifeline_flag = 1