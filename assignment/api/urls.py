from django.urls import path
from .views import (
    TrainFormatMatch,
    TrainFormatLearn,
    FormatMatch,

)

app_name = 'api'
urlpatterns = [
    path('train/format/match/', TrainFormatMatch.as_view()),
    path('train/format/learn/',TrainFormatLearn.as_view()),
    path('format/match/', FormatMatch.as_view()),
]