from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Deploy Django + Vercel + Supabase funcionando!</h1>")
