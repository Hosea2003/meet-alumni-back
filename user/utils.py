import os
from uuid import uuid4

from django.db import models
from django.http import Http404


def getFromModel(model: models.Model, pk):
    try:
        model = model.objects.get(id=pk)
        return model
    except models.ObjectDoesNotExist:
        raise Http404("College not found")

def upload_to(path):
    def wrapper(instance, filename: str):
        ext = filename.split(".")[-1]

        #         set the filename as a random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(path, filename)

    return wrapper
