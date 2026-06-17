import hashlib
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserFile

from Blockchain.blockchain import store_file_hash

# Create your views here.
def userhome(request):
    user = request.user
    return render(request, 'User/userhome.html', {'user':user})

@login_required
def upload_file(request):

    if request.method == "POST":

        uploaded_file = request.FILES['file']

        # Generate SHA256 hash
        sha256 = hashlib.sha256()

        for chunk in uploaded_file.chunks():
            sha256.update(chunk)

        file_hash = sha256.hexdigest()

        existing_file = UserFile.objects.filter(file_hash=file_hash).first()

        if existing_file:

            # reuse same stored file
            UserFile.objects.create(
                user=request.user,
                file=existing_file.file,   
                file_name=uploaded_file.name,
                file_hash=file_hash,
                blockchain_tx=existing_file.blockchain_tx
            )

        else:

            tx_hash = store_file_hash(file_hash)

            UserFile.objects.create(
                user=request.user,
                file=uploaded_file,
                file_name=uploaded_file.name,
                file_hash=file_hash,
                blockchain_tx=tx_hash
            )

        return redirect('view_files')

    return render(request, "user/upload.html")

@login_required
def view_files(request):

    files = UserFile.objects.filter(user=request.user)

    return render(request, "user/view_files.html", {"files": files})