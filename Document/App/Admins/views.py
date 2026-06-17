from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from Users.models import UserFile
from django.db.models import Count
import hashlib
import os
from django.conf import settings

def adminhome(request):
    users = User.objects.filter(is_staff=False, is_superuser=False) 
    return render(request, "Admin/adminhome.html", {"users": users})

def admin_update_userstatus(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        # Toggle the is_active status
        user.is_active = not user.is_active
        user.save()

        # Display message based on the action
        if user.is_active:
            messages.success(request, f"User {user.username} has been activated.")
        else:
            messages.success(request, f"User {user.username} has been deactivated.")
        
        return redirect('adminhome')  # Redirect back to the admin home page
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('adminhome')
    
@login_required
def deduplicated_files(request):

    files = (
        UserFile.objects
        .values('file_hash')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    dedup_list = []

    for f in files:

        users = UserFile.objects.filter(file_hash=f['file_hash'])

        dedup_list.append({
            "hash": f['file_hash'],
            "count": f['total'],
            "records": users
        })

    return render(request, "admin/dedup_files.html", {"files": dedup_list})

@login_required
def audit_file(request, file_id):

    file_record = UserFile.objects.get(id=file_id)

    file_path = os.path.join(settings.MEDIA_ROOT, str(file_record.file))

    status = "FILE NOT FOUND"

    if os.path.exists(file_path):

        sha256 = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)

        current_hash = sha256.hexdigest()

        if current_hash == file_record.file_hash:
            status = "VALID"
        else:
            status = "TAMPERED"

    return render(request, "admin/audit_result.html", {
        "file": file_record,
        "status": status
    })