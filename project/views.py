from django.db.models import Sum
from django.shortcuts import render
from django.shortcuts import redirect

from user_management.models import User

from project.models import Stage
from project.models import Project
from project.models import ProjectCategory
from project.models import StageActivities

# Create your views here.

def view_all(request):
    if request.method == "GET":
        records = Project.objects.all()
        context = {
            'records': records,
            'project_open': 'open',
            'project_active': 'active',
            'project_view_all_open': 'open',
            'project_view_all_active': 'active',
        }
        return render(request, 'project/home_page.html', context)
    
def project_create(request):
    if request.method == "GET":
        project_categories = ProjectCategory.objects.all()
        users = User.objects.all()

        context = {
            'users': users,
            'project_open': 'open',
            'project_active': 'active',
            'project_create_open': 'open',
            'project_create_active': 'active',
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
    stages = Stage.objects.filter(main_project = project_obj).prefetch_related('items')

    # Sum all budgeted and actual costs from related activities
    total_budgeted_cost = StageActivities.objects.filter(stage__main_project=project_obj).aggregate(
        total=Sum('budgeted_cost')
    )['total'] or 0

    total_actual_cost = StageActivities.objects.filter(stage__main_project=project_obj).aggregate(
        total=Sum('actual_cost')
    )['total'] or 0
    context = {
        'stages': stages,
        'project_open': 'open',        
        'project_active': 'active',
        'project_obj': project_obj,
        'project_view_all_open': 'open',
        'project_view_all_active': 'active',
        'total_actual_cost': total_actual_cost,
        'total_budgeted_cost': total_budgeted_cost,        
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
    if request.method == "POST":
        
        status = request.POST.get('status', '')
        name = request.POST.get('stage_name', '')
        end_date = request.POST.get('end_date', '')
        priority = request.POST.get('priority', '')
        start_date = request.POST.get('start_date', '')
        description = request.POST.get('description', '')
        main_project = request.POST.get('project_id', '')

        project = Project.objects.get(pk=main_project)

        stage = Stage.objects.create(
            name = name,
            status = status,            
            end_date = end_date,
            priority = priority,
            main_project = project,
            start_date = start_date,
            description = description,            
        )

        # Loop through activities dynamically
        index = 0
        while True:
            activity_name = request.POST.get(f'activity_name_{index}')
            budgeted_cost = request.POST.get(f'budgeted_cost_{index}')
            actual_cost = request.POST.get(f'actual_cost_{index}')
            is_completed = request.POST.get(f'is_completed_{index}') == 'true'

            if not activity_name:
                break  # Stop when no more activities

            StageActivities.objects.create(
                stage=stage,
                name=activity_name,
                budgeted_cost=budgeted_cost or 0,
                actual_cost=actual_cost or 0,
                is_completed=is_completed,
            )
            index += 1

    return redirect('project:view-project', id=main_project)

def activity_create(request):
    if request.method == "POST":
        complete = True
        stage_id = request.POST.get('stage_id', '')
        actual_cost = request.POST.get('actual_cost', '')
        is_completed = request.POST.get('is_completed', '')
        budgeted_cost = request.POST.get('budgeted_cost', '')
        activity_name = request.POST.get('activity_name', '')
        main_project = request.POST.get('main_project_id', '')

        print(f"Stage ID --> {stage_id}")
        print(f"Actual Cost --> {actual_cost}")
        print(f"Main Project --> {main_project}")
        print(f"Is Completed --> {is_completed}")
        print(f"Budgeted Cost --> {budgeted_cost}")
        print(f"Activity Name --> {activity_name}")
        
        if is_completed == "0":
            complete = False

        stage_obj = Stage.objects.get(pk=stage_id)
        activity = StageActivities.objects.create(
            stage = stage_obj,            
            name = activity_name,
            is_completed = complete,
            actual_cost = actual_cost,
            budgeted_cost = budgeted_cost,            
        )

        return redirect('project:view-project', id=main_project)