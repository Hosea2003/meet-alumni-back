from django.db import models
from django.http import Http404


def getFromModel(model: models.Model, pk):
    try:
        model = model.objects.get(id=pk)
        return model
    except models.Model.DoesNotExist:
        raise Http404("College not found")
