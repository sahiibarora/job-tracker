from django.shortcuts import render, redirect, get_object_or_404
from .models import JobApplication
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def dashboard(request):
    jobs = JobApplication.objects.all()
    total = jobs.count()
    applied = jobs.filter(status='Applied').count()
    interview = jobs.filter(status='Interview').count()
    offer = jobs.filter(status='Offer').count()
    rejected = jobs.filter(status='Rejected').count()

    return render(request, 'tracker/dashboard.html', {
        'jobs': jobs,
        'total': total,
        'applied': applied,
        'interview': interview,
        'offer': offer,
        'rejected': rejected
    })

@csrf_exempt
def add_job(request):
    if request.method == 'POST':
        JobApplication.objects.create(
            company = request.POST.get('company'),
            role = request.POST.get('role'),
            status = request.POST.get('status'),
            date = request.POST.get('date'),
            notes = request.POST.get('notes', ''),
        )
        return redirect('dashboard')

    return render(request, 'tracker/add_job.html')

@csrf_exempt
def edit_job(request, pk):
    job = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
        job.company = request.POST.get('company')
        job.role = request.POST.get('role')
        job.status = request.POST.get('status')
        job.date = request.POST.get('date')
        job.notes = request.POST.get('notes', '')
        job.save()
        return redirect('dashboard')
    return render(request, 'tracker/edit_job.html', {'job': job})

@csrf_exempt
def delete_job(request, pk):
    job = get_object_or_404(JobApplication, pk=pk)
    job.delete()
    return redirect('dashboard')