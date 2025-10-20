from django.db import models

from user_management.models import User
# Create your models here.

class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS_CHOICES = [
        ("on_hold", "On Hold"),        
        ("planned", "Planned"),        
        ("completed", "Completed"),        
        ("cancelled", "Cancelled"),
        ("in_progress", "In Progress"),
    ]

    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="planned")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="medium")
    project_lead = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True)

    end_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def total_budgeted_cost(self):
        """Sum of all budgeted costs across all stages."""
        total = 0
        for stage in self.project_stage.all():
            total += stage.total_budgeted_cost
        return total

    @property
    def total_actual_cost(self):
        """Sum of all actual costs from related activities."""
        total = 0
        for stage in self.project_stage.all():
            total += stage.total_actual_cost
        return total

    @property
    def progress_percent(self):
        total_items = self.items.count()
        if total_items == 0:
            return 0
        completed_items = self.items.filter(is_completed=True).count()
        return round((completed_items / total_items) * 100, 2)


class Stage(models.Model):
    main_project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_stage")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Project.STATUS_CHOICES, default="planned")
    priority = models.CharField(max_length=20, choices=Project.PRIORITY_CHOICES, default="medium")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Sub of {self.main_project.name})"
    
    @property
    def total_budgeted_cost(self):
        """Sum of all budgeted costs from related activities."""
        return sum(activity.budgeted_cost for activity in self.items.all())

    @property
    def total_actual_cost(self):
        """Sum of all actual costs from related activities."""
        return sum(activity.actual_cost for activity in self.items.all())

class StageActivities(models.Model):    
    stage = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name="items", null=True, blank=True)

    name = models.CharField(max_length=255)  # e.g. "Cement", "Labor"
    budgeted_cost = models.DecimalField(max_digits=12, decimal_places=2)
    actual_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


# class ProjectItem(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="items")
#     sub_project = models.ForeignKey(Stage, on_delete=models.CASCADE, related_name="items", null=True, blank=True)

#     name = models.CharField(max_length=255)  # e.g. "Cement", "Labor"
#     budgeted_cost = models.DecimalField(max_digits=12, decimal_places=2)
#     actual_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
#     is_completed = models.BooleanField(default=False)

#     def __str__(self):
#         return f"{self.name} - {self.project.name if self.project else self.sub_project.name}"


# class ProjectProgress(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="progress_logs", null=True, blank=True)
#     sub_project = models.ForeignKey(SubProject, on_delete=models.CASCADE, related_name="progress_logs", null=True, blank=True)
#     item = models.ForeignKey(ProjectItem, on_delete=models.CASCADE, related_name="progress_updates", null=True, blank=True)

#     description = models.TextField()  # e.g. "Foundation completed"
#     date = models.DateField(auto_now_add=True)
#     percent_completed = models.DecimalField(max_digits=5, decimal_places=2, help_text="Cumulative % completed")

#     def __str__(self):
#         return f"{self.project.name if self.project else self.sub_project.name} - {self.percent_completed}%"


# class AuditLog(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="audits", null=True, blank=True)
#     sub_project = models.ForeignKey(SubProject, on_delete=models.CASCADE, related_name="audits", null=True, blank=True)

#     auditor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     remarks = models.TextField()
#     risk_level = models.CharField(max_length=20, choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")], default="low")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Audit - {self.project.name if self.project else self.sub_project.name} by {self.auditor}"