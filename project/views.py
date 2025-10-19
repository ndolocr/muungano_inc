from django.shortcuts import render
from django.shortcuts import redirect

from user_management.models import User

from project.models import Project
from project.models import ProjectCategory

# Create your views here.

def view_all(request):
    if request.method == "GET":
        records = Project.objects.all()
        context = {
            'records': records
        }
        return render(request, 'project/home_page.html', context)
    
def project_create(request):
    if request.method == "GET":
        project_categories = ProjectCategory.objects.all()
        users = User.objects.all()

        context = {
            'users': users,
            'project_categories': project_categories
        }

        return render(request, 'project/create.html', context)
    elif request.method == "POST":        
        status = request.POST.get('status', '')
        category = request.POST.get('category', '')
        location = request.POST.get('location', '')
        end_date = request.POST.get('end_date', '')
        priority = request.POST.get('priority', '')
        start_date = request.POST.get('start_date', '')
        description = request.POST.get('description', '')
        project_lead = request.POST.get('project_lead', '')
        project_name = request.POST.get('project_name', '')

        user_obj = User.objects.get(pk=project_lead)
        category_obj = ProjectCategory.objects.get(pk=category)

        print(f"Project Name --> {project_name}")
        print(f"Project Lead --> {project_lead}")
        print(f"Project Status --> {status}")
        print(f"Project Category --> {category}")
        print(f"Project Location --> {location}")
        print(f"Project Priority --> {priority}")
        print(f"Project End Date --> {end_date}")
        print(f"Project Start Date --> {start_date}")
        print(f"Project Description --> {description}")
        print(f"Project Lead OBJ --> {user_obj}")
        print(f"Project Category OBJ --> {category_obj}")

        try:
            record = Project.objects.create(
                status = status,
                name = project_name,                
                location = location,
                end_date = end_date,
                priority = priority,
                category = category_obj,
                project_lead = user_obj,
                start_date = start_date,
                description = description,
            )
            return redirect('project:view-all')
        except Exception as e:
            print(f'Error on saving --> {e}')
            return render(request, 'project/create.html')

def view_project(request, id):
    project_obj = Project.objects.get(pk=id)
    context = {
        'project_obj': project_obj,
    }

    return render(request,'project/view_project.html',context)

def categories_home_page(request):
    records = ProjectCategory.objects.all()
    context = {
        'records': records
    }
    return render(request, 'project_category/home_page.html', context)

def categories_create(request):
    if request.method == "GET":
        return render(request, 'project_category/create.html')
    elif request.method == "POST":
        description = request.POST.get('description', '')
        name = request.POST.get('name', '')

        print(f"Category Name {name}")
        print(f"Category Description {description}")

        try:
            record = ProjectCategory.objects.create(name = name, description = description)
            return redirect('project:categories-home-page')
        except Exception as e:
            print(f'Error on saving --> {e}')
            return render(request, 'project/create.html')
        
def stages_view_all(request):    
    return render(request, 'project_stage/view_all.html')

def stages_create(request):
    return render(request, 'stages_category/create.html')