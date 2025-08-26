from django.shortcuts import render

# Create your views here.
import os, shutil
from django.shortcuts import render
from django.http import JsonResponse
from .constants import FILE_CATEGORIES
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, "organizer/index.html")

@csrf_exempt
def analyze_folder(request):
    if request.method == "POST":
        folder_path = request.POST.get("folder_path")

        if not os.path.exists(folder_path):
            return JsonResponse({"error": "Path does not exist!"}, status=400)

        categorized = {cat: [] for cat in FILE_CATEGORIES.keys()}

        for file in os.listdir(folder_path):
            full_path = os.path.join(folder_path, file)
            if os.path.isfile(full_path):
                ext = file.split(".")[-1].lower()
                found = False
                for category, extensions in FILE_CATEGORIES.items():
                    if ext in extensions:
                        categorized[category].append(file)
                        found = True
                        break
                if not found:
                    categorized["Others"].append(file)

        return JsonResponse({"data": categorized, "folder": folder_path})

@csrf_exempt
def make_changes(request):
    if request.method == "POST":
        folder_path = request.POST.get("folder_path")
        categorized = request.POST.get("categorized")

        if not os.path.exists(folder_path):
            return JsonResponse({"error": "Path does not exist!"}, status=400)

        import json
        categorized = json.loads(categorized)

        for category, files in categorized.items():
            if not files:
                continue
            category_path = os.path.join(folder_path, category)
            os.makedirs(category_path, exist_ok=True)

            for file in files:
                src = os.path.join(folder_path, file)
                dst = os.path.join(category_path, file)
                if os.path.exists(src) and not os.path.exists(dst):
                    shutil.move(src, dst)

        return JsonResponse({"status": "success"})
