from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
import os
from django.http import FileResponse

@login_required
def keyshare(request):
    return render(request, "keyshare.html")


# Imaginary function to handle an uploaded file.
from . import save_key
from . import predict_data


@login_required
def upload_key(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            save_key.handle_uploaded_file(request.FILES["file"], request.user.username)
            return HttpResponseRedirect("/success/")
        else:
            return HttpResponseRedirect("/accounts/login")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})


@login_required
def predict(request):
    if request.method == "POST":
        tmp = "./acps/keys/" + request.user.username + ".key"
        form = UploadFileForm(request.POST, request.FILES)
        if os.path.isfile(tmp) == False:
            return render(request, "predict.html", {"form": form})
        if form.is_valid():
            predict_data.handle_uploaded_file(
                request.FILES["file"], request.user.username
            )
            encrypted_data=predict_data.read_data(request.user.username)
            predict_data.predict(encrypted_data,request.user.username)
            response = FileResponse(open("./acps/predictions/"+request.user.username+".pred", "rb"),as_attachment=True)
            
            return response

    else:
        form = UploadFileForm()
    return render(request, "predict.html", {"form": form})
    
def download(request):
    response = FileResponse(open("./acps/client/client_data.zip", "rb"),as_attachment=True)
            
    return response

