from django.shortcuts import render
from django.shortcuts import redirect

from project.models import Project

# Create your views here.

def home_page(request):
    if request.method == "GET":
        records = Project.objects.all()
        context = {
            'records': records
        }
        return render(request, 'project/home_page.html', context)
    
def create(request):
    if request.method == "GET":
        return render(request, 'project/create.html')
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

        print(f"Project Name {project_name}")
        print(f"Project Lead {project_lead}")
        print(f"Project Status {status}")
        print(f"Project Category {category}")
        print(f"Project Location {location}")
        print(f"Project Priority {priority}")
        print(f"Project End Date {end_date}")
        print(f"Project Start Date {start_date}")
        print(f"Project Description {description}")

        try:
            record = Project.objects.create(
                status = status,
                category = category,
                location = location,
                end_date = end_date,
                priority = priority,
                start_date = start_date,
                description = description,
                project_lead = project_lead,
                project_name = project_name,
            )
            return redirect('project:home-page')
        except Exception as e:
            print(f'Error on saving --> {e}')
            return render(request, 'project/create.html')