from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
import cloudinary
import cloudinary.uploader
import cloudinary.api


def home(request):
    project = Project.objects.all()
    # get the latest project from the database
    latest_project = project[0]
    # get project rating
    rating = Rating.objects.filter(project_id=latest_project.id).first()
    # print(latest_project.id)

    return render(
        request, "home.html", {"projects": project, "project_home": latest_project, "rating": rating}
    )
   
