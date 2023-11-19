from django.shortcuts import redirect

def redirect_to_store(request):
    return redirect('etienda/')