## /////////////////////////////////////////////////////////////////////////////
## IMPORTANT:
## THE CODE BELOW IS READ-ONLY CODE AND YOU SHOULD INSPECT IT TO SEE WHAT IT
## DOES IN ORDER TO COMPLETE THE TASK, BUT DO NOT MODIFY IT IN ANY WAY AS THAT
## WILL RESULT IN A TEST FAILURE
## /////////////////////////////////////////////////////////////////////////////

from django.urls import re_path
from my_app import views 
 
urlpatterns = [ 
    re_path(r'^api/player$', views.player_collection),
    re_path(r'^api/player/(?P<id>[0-9]+)$', views.player),
    re_path(r'^api/team/process$', views.team_process),
]