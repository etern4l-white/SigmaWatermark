from django.shortcuts import render, HttpResponse
from django.http import Http404
from .utils import watermark_doc
from .forms import UploadFileForm



def watermark_image(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            pass
        else:
            return Http404("Error")
        processed_document = watermark_doc(request.FILES.get("fileUpload"), request.POST['name'])
        response = HttpResponse(processed_document, content_type='application/octet-stream')
        # response['Content-Dispositiearon'] = f'attachment; filename="qwerqwer.docx"'  # Set a proper filename
        return response
    return render(request, "watermarky/base.html")
    
