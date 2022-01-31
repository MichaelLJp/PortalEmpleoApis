from django.urls import  path
from .views import UserAPI,CandidateList,RegisterCandidateAPI, OffersList, PostulationCreate,OffersCreate,OffersUpdate

urlpatterns = [
    path('candidate_list/', CandidateList.as_view(), name='candidate_list'),
    path('create_user/', UserAPI.as_view(), name ="create_user"),
    path('register_candidate/', RegisterCandidateAPI.as_view(), name ="register_candidate"),
    path('offers_list/', OffersList.as_view(), name ="offers_list"),
    path('postulation_create/', PostulationCreate.as_view(), name ="postulation_create"),
    path('offers_create/', OffersCreate.as_view(), name ="offers_create"),
    path('offers_update/<int:pk>/', OffersUpdate.as_view(), name ="Offers_update"),


    

]
