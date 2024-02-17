from django.shortcuts import render
from ultralytics import YOLO
from PIL import Image
import os
import shutil
from .forms import *
from roboflow import Roboflow

# detection model
def load_model():
    model = YOLO('yolov8n.pt')
    return model 

# segmentation model
# def load_segmentation_model():
#     model = YOLO('yolov8n-seg.pt')
#     return model 

# custom detection model
# def load_custom_detection_model():
#     rf = Roboflow(api_key="485V2UYUIK961W1Rbxkc")
#     project = rf.workspace().project("tanjil_identifier")
#     model = project.version(1).model
#     return model 


def check_file_type(uploaded_filename):
    file_name, file_extension = os.path.splitext(uploaded_filename)

    # List of common image file extensions
    image_extensions = ['.jpg', '.jpeg', '.png']

    # List of common video file extensions
    video_extensions = ['.mp4', '.avi']

    if file_extension.lower() in image_extensions:
        file_type = "img"
    elif file_extension.lower() in video_extensions:
        file_type = "vdo"
    
    return file_type



def detect(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            conf = float(request.POST.get('conf', '0.7'))
            uploaded_file = request.FILES['file'] 
            uploaded_filename = uploaded_file.name
            # extracting the original extension 
            original_extension = os.path.splitext(uploaded_filename)[1]

            file_type = check_file_type(uploaded_filename)
            instance = form.save(commit=False)
            instance.file = uploaded_file 
            instance.save() 
            file_path = os.path.join('media', 'uploaded_files', uploaded_file.name)
            model = load_model()
            src = file_path 
            result = model(src, show=True, conf=conf, save=True)
            save_dir = result[0].save_dir
            result_file_path = os.path.join(save_dir, uploaded_file.name)
            destination_dir = os.path.join('media', 'result_files')

            # Create the destination directory if it doesn't exist
            os.makedirs(destination_dir, exist_ok=True)

            # Copy the result file to the destination directory
            shutil.copy(result_file_path, destination_dir)

            # Construct the URL of the copied file for rendering in the template
            copied_file_path = os.path.join('result_files', uploaded_file.name)

            context={
                'form' : form,
                'result_file_path' : copied_file_path,
                'file_type' : file_type
            }

            return render(request, 'App_Detection/index.html', context) 
    else:
        form = FileUploadForm()
        context = {
            'form' : form 
        }
        return render(request, 'App_Detection/index.html', context)