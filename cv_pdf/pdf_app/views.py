from django.shortcuts import render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io

def user_data(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        summary = request.POST.get('summary', '')
        degree = request.POST.get('degree', '')
        university = request.POST.get('university', '')
        previous_jobs = request.POST.get('previous_jobs', '')
        skills = request.POST.get('skills', '')

        profile = Profile(name=name, email=email, phone=phone,
                          summary=summary, degree=degree,
                          university=university,
                          previous_jobs=previous_jobs, skills=skills)
        profile.save()

    return render(request, 'pdf_app/user_data.html')

def cv_view(request, id):
    user_profile = Profile.objects.get(pk=id)
    context = {'user_profile': user_profile}
    template = loader.get_template('pdf_app/cv.html')
    html = template.render({'user_profile':user_profile})
    options = {
        'page-size':'Letter',
        'encoding':'UTF-8'
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment'
    filename = 'cv.pdf'

    return response

def users_cvs(request):
    profiles = Profile.objects.all()
    return render(request, 'pdf_app/users_cvs.html', {'profiles':profiles})

