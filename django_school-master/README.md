# README

# Assignment 4

## Abstract

This assignment is to copy re-create the first assignment in a new language and
Framework. I spent the majority of my time on this application trying out Scala
frameworks. I spent nearly a week feeling like I was making progress and just
about able to deploy an application when I came to the real conclusion that I
had very little working code to show and was not likely to succeed in finishing
the application before the assignment was over. I decided to switch frameworks
and languages and time-box my effort. 

I created the application in Django with an allowed time of 8 hours. This
included the time needed to setup the development environment, learn the
framework, I had never used Django before, and build the application. Django
allowed me to successfully build a website in this time by providing good
documentation, and powerful administration and developer tools. 

## Introduction

After completing Assignment 3 using Ruby on Rails, Assignment 4 presents an
opportunity to try a new language and framework. I decided I wanted to try
Scala, so I did a quick research session and found the framework Scalatra. I
spent about 2 hours learning Scala, 2 hours learning SBT (Simple Build Tool),
and then started in on some Scalatra framework examples. Scalatra is a
bare-bones framework with very little functionality included out of the box.
Each example was created to test a small piece of functionality. After about 4
hours of playing with Scalatra and not being able to make any real progress, I
decided to switch to a new Scala framework that might have better support for
beginners. I tried both Play and Lift and had a horrible time getting the
entire stack setup. For all three frameworks, I found lots of out of date
tutorials and tools. Several times, I downloaded the sample code and flowed the
build instructions only for there to be an error with the build or I would not
be able to find the proper tools to follow the example. I persisted trying to
get projects going, I have about ten different attempts started on my computer,
but as of Friday realized that it was doubtful I would be able to complete the
assignment in Scala being so new to the language, build tool, and the
frameworks. So I decided to switch to Python with Django. 

Django is advertised as a framework that encourages rapid development. For this
assignment, I have decided to put this to the test. I have allotted 8 (all the
time I have available this weekend) to learn the framework, and get a basic web
application up and running. I will test this claim by creating a similar
application to the one I built in Assignment 1 in this minimal amount of time.
Hopefully, some of the lessons learned here, with another new language and
framework will also translate back to Scala. 

## Method/Measurement

For this application. I will start by quickly running through the tutorial. I
will allow 1.5 hours to this effort and hopefully get far enough that I will be
able to build my application. As part of this, I will also set up my own Python
and Django environment. I have setup python virtual environments before, but it
has been a long time. 

Next, I will set up a new Django project to build this application form the
bare Django framework. The rest of the work will be done as best I can running
off the instruction from the tutorial.

## Results 

### Step 1: Tutorial 2hrs

It took me a bit longer to get everything setup than expected. Getting python
just right took a couple tries but I finally have a new environment setup for
the project and have done enough of the tutorial that I think I can create the
new application. Django has a similar structure to Ruby on Rails and feels
familiar but does not provide as much boilerplate code. Instead, you have to
add code for each route, view, template, and model. This means opening a lot of
files early on in the development.

##Step 2: Build the Application 6hrs

The first step is to setup the application. I ran the command:

```bash
django-admin startproject school 
```

to setup the project. Next, I decided to create separate “apps” for each
entity. I setup the scaffold for them using the new manage.py in the new school
directory. 

```bash
python manage.py startapp professors
python manage.py startapp courses
python manage.py startapp sections
```

Each of these will hold their portion of the model, their own templates,
routes, and controllers. Inside or each of these apps, I created the model for
the app. 

```python
# Professors:
class Professor(models.Model):
    name = models.CharField(max_length=200)
    department = models.CharField(max_length=200)
    def __str__(self):
        return self.name
# Courses:
class Course(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=600)
    department = models.CharField(max_length=200)
    def __str__(self):
        return self.name
# Sections:
class Section(models.Model):
    professor = models.ForeignKey('professors.Professor', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE)
    time = models.TimeField()
    def __str__(self):
        return self.course.name + " taught by  " + self.professor.name + " @ " + self.time.__str__()
```

I added the __str__ methods so that the objects are identifiable when debugging
in the command line or in the admin console. 

I then applied these changes to the model using manage.py migrations

```bash
python manage.py makemigrations professors
python manage.py makemigrations courses
python manage.py makemigrations sections

python manage.py sqlmigrate professors 0001
python manage.py sqlmigrate courses 0001
python manage.py sqlmigrate sections 0001

python manage.py migrate
```

This last command applied all of the migrations along with all the need
migrations for the out of the box packages, like authentication. 

The next step was to enable the Admin console for these models. As I learned in
the tutorial, Django provides a powerful admin content designed to allow the
separation of admin duties, like creating content, from consumer duties. 

In each app’s admin.py file I added a couple lines to register the model. Here
is the one for professors. 

```python
From .models import Professor
Admin.site.register(Professor)
```

This gave me the ability to test the models without having to build any routes
or views. 

![Admin Console](/README_IMAGES/admin_console1.png?raw=true)
![Admin Console](/README_IMAGES/admin_console_2.png?raw=true)


With some test data in place, I moved on to displaying it. I decided to change
the design from the first application slightly. I imagined that instead of
building out an admin page for a school, I would let the Django admin portal
handle that functionality. Instead, the site would be a place for professors to
view courses and sign up to teach them. In this scenario, the model is the
same, but the front-end is different. Here is the new structure for the views.

* Professors
   * Index
   * Detail
   * Add_Section (GET)
   * Create_Section (POST)
* Courses
   * Index
   * Detail
* Sections
   * Delete

I setup these new routes in the urls.py files. I had to create the files for
each new app. Then include them in the main router for the school. Here is what
I added:

```python
urlpatterns = [
    url(r'^professors/', include('professors.urls')),
    url(r'^courses/', include('courses.urls')),
    url(r'^sections/', include('sections.urls')),
    url(r'^admin/', admin.site.urls),
]
```

and for the different apps

```python
app_name = 'professors'
urlpatterns = [
    url(r'^$', views.professors, name='index'),
    url(r'professors$', views.professors, name='professors'),
    url(r'^(?P<professor_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<professor_id>[0-9]+)/add_section$', views.add_section, name='add_section'),
    url(r'^(?P<professor_id>[0-9]+)/create_section$', views.create_section, name='create_section'),
]
```

```python
app_name = 'courses'
urlpatterns = [
    url(r'^$', views.courses, name='index'),
    url(r'courses$', views.courses, name='courses'),
    url(r'^(?P<course_id>[0-9]+)/$', views.detail, name='detail'),
]
```

```python
app_name = 'sections'
urlpatterns = [
    url(r'^$', views.sections, name='index'),
    url(r'sections$', views.sections, name='sections'),
    url(r'^(?P<section_id>[0-9]+)/delete$', views.delete, name='delete'),
]
```

I then stubbed out each of these routes in the views.py files so that the app
would build and got to work on the templates.

The templates are html with some python language annotations to include
variables and create lists. Each template was created from scratch. Unlike Ruby
on Rails, the templates were not automatically created. While creating the one
form, to add a section, I found that there is probably a more ‘Django’ way of
generating the form from a python object, but that method had not been shown in
the Tutorial. I decided with my limited time, to exploit what I knew vs trying
to learn additional methods. I will mark it for a future refactor. 

As I completed each template, I stitched it to its controller in the views.py
file. Here are screenshots of the results. They are very rudimentary, but
capture all of the functionality of the app. They are ready to be made pretty
with CSS and given better navigation. 

![Professor List](/README_IMAGES/Professors_View.jpg?raw=true)
![Professor View](/README_IMAGES/Professor_Detail.png?raw=true)
![Create a Section](/README_IMAGES/Create_A_Section.png?raw=true)
![Course Detail](/README_IMAGES/Course_Detail.png?raw=true)


## Conclusion

After playing with Scalatra and Scala, Django felt like cheating. There is so
much ‘magic’ behind the scenes that it is very easy to start an app without
thinking about it. Out of the box, you get an admin console and an ORM. Most of
the Scala frameworks required you to add in an ORM or just a JDBC connector.
Those Scala ORM’s then required you to find a different tool to create and
manage migrations. Because there were so many options available in Scala, it
was a lot of work even deciding on which one to try. Django instead defaulted
to a database, sqlite, and an ORM which eliminated the majority of the setup
and allowed me to get right into the business logic development. 

I ended up sticking pretty close to the 8 hours allotted for this application.
That included setting up the environments, going through the tutorials, and
building the app from the ground up. I had spent nearly three times as long
trying just to get a proof of concept started in Scala. The documentation for
Django was very well maintained, and the only times I had issues was when I
introduced errors through typos. Django is structured such that beginner
programmers, or even some non-programmers, could create sites.

## Sources
* https://www.djangoproject.com/

### Author
* Alan Peters


