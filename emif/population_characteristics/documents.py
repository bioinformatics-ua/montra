import json

from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, ListView
from .models import Picture
from .response import JSONResponse, response_mimetype
from .serialize import serialize, serialize_dummy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test, login_required

from emif.views import createqsets, get_api_info
from django.shortcuts import render

import os

def handle_uploaded_file(f):
    print "abspath"

    with open(os.path.join(os.path.abspath(settings.PROJECT_DIR_ROOT + 'emif/static/upload_images/'), f.name),
              'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def document_form_view_upload(request, template_name='documents_upload_form.html'):

    #if request.FILES:
        #for name, f in request.FILES.items():
            #handle_uploaded_file(f)
    files = [serialize_dummy(request.FILES)]
    data = {'files': files}
    response = JSONResponse(data, mimetype=response_mimetype(request))
    response['Content-Disposition'] = 'inline; filename=files.json'
    return response

    

def document_form_view(request, runcode, qs, template_name='documents_upload_form.html'):
    
    qsets, name, db_owners, fingerprint_ttype = createqsets(runcode)

    if fingerprint_ttype == "":
        raise "There is missing ttype of questionarie, something is really wrong"

    apiinfo = json.dumps(get_api_info(runcode));
    owner_fingerprint = False
    for owner in db_owners.split(" "):
        print owner
        print request.user.username
        if (owner == request.user.username):
            owner_fingerprint = True
    
    return render(request, template_name, 
        {'request': request, 'qsets': qsets, 'export_bd_answers': True, 
        'apiinfo': apiinfo, 'fingerprint_id': runcode,
                   'breadcrumb': True, 'breadcrumb_name': name.decode('ascii', 'ignore'),
                    'style': qs, 'collapseall': False, 
                    'owner_fingerprint':owner_fingerprint,
                    'fingerprint_dump': True,
                    'fingerprint_ttype': fingerprint_ttype,
                    })

    


# Code adapted from: https://github.com/sigurdga/django-jquery-file-upload
class PictureCreateView(CreateView):
    model = Picture
    template_name = 'documents_upload_form.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PictureCreateView, self).dispatch(*args, **kwargs)

    def get_initial(self):
        
        return { 'request': self.request }


    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')

class BasicVersionCreateView(PictureCreateView):
    template_name_suffix = '_basic_form'


class BasicPlusVersionCreateView(PictureCreateView):
    template_name = 'documents_upload_form.html'


class AngularVersionCreateView(PictureCreateView):
    template_name_suffix = '_angular_form'


class jQueryVersionCreateView(PictureCreateView):
    template_name_suffix = '_jquery_form'


class PictureDeleteView(DeleteView):
    model = Picture

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class PictureListView(ListView):
    model = Picture

    def render_to_response(self, context, **response_kwargs):
        files = [ serialize(p) for p in self.get_queryset() ]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response