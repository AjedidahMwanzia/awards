from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
import cloudinary
import cloudinary.uploader
import cloudinary.api


from django.http import JsonResponse
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProfileSerializer,ProjectSerializer
from .permissions import IsAdminOrReadOnly


def home(request):
    project = Project.objects.all()
    latest_project = project[0]
    rating = Rating.objects.filter(project_id=latest_project.id).first()
    

    return render(
        request, "home.html", {"projects": project, "project_home": latest_project, "rating": rating}
    )
   
def project_details(request, project_id):
    project = Project.objects.get(id=project_id)
    rating = Rating.objects.filter(project=project)
    return render(request, "project.html", {"project": project, "rating": rating})


@login_required(login_url="/accounts/login/")
def profile(request):  
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()  # get profile
    project = Project.objects.filter(user_id=current_user.id).all()  # get all projects
    return render(request, "profile.html", {"profile": profile, "images": project})


@login_required(login_url="/accounts/login/")
def update_profile(request):
    if request.method == "POST":

        current_user = request.user

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        bio = request.POST["bio"]
        contact = request.POST["contact"]

        profile_image = request.FILES["profile_pic"]
        profile_image = cloudinary.uploader.upload(profile_image)
        profile_url = profile_image["url"]

        user = User.objects.get(id=current_user.id)

        # check if user exists in profile table and if not create a new profile
        if Profile.objects.filter(user_id=current_user.id).exists():

            profile = Profile.objects.get(user_id=current_user.id)
            profile.profile_photo = profile_url
            profile.bio = bio
            profile.contact = contact
            profile.save()
        else:
            profile = Profile(
                user_id=current_user.id,
                profile_photo=profile_url,
                bio=bio,
                contact=contact,
            )
            profile.save_profile()

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        user.save()

        return redirect("/profile", {"success": "Profile Updated Successfully"})
    else:
        return render(request, "profile.html", {"danger": "Profile Update Failed"})



@login_required(login_url="/accounts/login/")
def save_project(request):
    if request.method == "POST":

        current_user = request.user

        title = request.POST["title"]
        location = request.POST["location"]
        description = request.POST["description"]
        url = request.POST["url"]
        image = request.FILES["image"]
        image = cloudinary.uploader.upload(image, crop="limit", width=500, height=500)
        image_url = image["url"]

        project = Project(
            user_id=current_user.id,
            title=title,
            location=location,
            description=description,
            url=url,
            image=image_url,
        )
        project.save_project()

        return redirect("/profile", {"success": "Project Saved Successfully"})
    else:
        return render(request, "profile.html", {"danger": "Project Save Failed"})


@login_required(login_url="/accounts/login/")
def delete_project(request, id):
    project = Project.objects.get(id=id)
    project.delete_project()
    return redirect("/profile", {"success": "Project Deleted Successfully"})



@login_required(login_url="/accounts/login/")
def rate_project(request, id):
    if request.method == "POST":

        project = Project.objects.get(id=id)
        current_user = request.user

        design_rate=request.POST["design"]
        usability_rate=request.POST["usability"]
        content_rate=request.POST["content"]

        Rating.objects.create(
            project=project,
            user=current_user,
            design_rate=design_rate,
            usability_rate=usability_rate,
            content_rate=content_rate,
            avg_rate=round((float(design_rate)+float(usability_rate)+float(content_rate))/3,2),
        )

       
        avg_rating= (int(design_rate)+int(usability_rate)+int(content_rate))/3

      
        project.rate=avg_rating
        project.update_project()

        return render(request, "project.html", {"success": "Project Rated Successfully", "project": project, "rating": Rating.objects.filter(project=project)})
    else:
        project = Project.objects.get(id=id)
        return render(request, "project.html", {"danger": "Project Rating Failed", "project": project})



def search_project(request):
    if 'search_term' in request.GET and request.GET["search_term"]:
        search_term = request.GET.get("search_term")
        searched_projects = Project.objects.filter(title__icontains=search_term)
        message = f"Search For: {search_term}"

        return render(request, "search.html", {"message": message, "projects": searched_projects})
    else:
        message = "You haven't searched for any term"
        return render(request, "search.html", {"message": message})



class ProfileList(APIView): # get all profiles
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_profiles = Profile.objects.all()
        serializers = ProfileSerializer(all_profiles, many=True)
        return Response(serializers.data)

    

class ProjectList(APIView): # get all projects
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)