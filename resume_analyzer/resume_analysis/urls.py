from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path('extract_text_from_pdf/', views.extract_text_from_pdf, name='extract_text_from_pdf'), 
    path('extract_text_from_docx/',views.extract_text_from_docx,name="extract_text_from_docx"),
    path('predict/', views.predict, name='predict'),  # Add your other paths here
]