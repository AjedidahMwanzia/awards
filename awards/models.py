from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length = 100, null=False,blank=False)

    def __str__(self):
        return self.name
    def save_category(self):
        self.save()
    # delete the image database
    def delete_category(self):
        self.delete()

    def get_all_category(cls):
        categories = Category.objects.all()
        return categories

class Photo(models.Model):
    name = models.CharField(max_length =30,null=True)
    category=models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,blank=True)
    description=models.TextField(null=True)
    image = models.ImageField(default='DEFAULT VALUE')
    location = models.ForeignKey('Location',null=True,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.description

    def save_image(self):
        self.save()
    # delete the image database
    def delete_image(self):
        self.delete()
    # get all images
    def update_image(self, name, description, location, category):
        self.name = name
        self.description = description
        self.location = location
        self.category = category
        self.save()

    @classmethod
    def get_all_images(cls):
        images = Photo.objects.all()
        return images
    

    # get image by id
    @classmethod
    def get_image_by_id(cls, id):
        image = Photo.objects.get(id=id)
        return image

    @classmethod
    def filter_by_category(cls, category_id):
        images = Photo.objects.filter(category_id=category_id)
        return images
    # get images by location
    @classmethod
    def filter_by_location(cls, location_id):
        images = Photo.objects.filter(location__id=location_id)
        return images

    @classmethod
    def search_by_category(cls,search_term):
        searched_photos=cls.objects.filter(category__name__icontains=search_term)
        return searched_photos

class Location(models.Model):
    name = models.CharField(max_length=50, unique=True)
    # save location to database
    def save_location(self):
        self.save()

    # update location
    def update_location(self, name):
        self.name = name
        self.save()

     # delete location from database
    def delete_location(self):
        self.delete()

    def __str__(self):
        return self.name

  