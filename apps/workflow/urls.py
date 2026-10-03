from django.urls import path
from .views import WorkflowTransitionView

urlpatterns = [path("visits/<int:pk>/transition/", WorkflowTransitionView.as_view(), name="workflow-transition")]