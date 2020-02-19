"""File helper."""
import logging
import os
import uuid

from django.core.files.storage import default_storage
from django.db import models
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from storages.backends.gcloud import GoogleCloudStorage

logger = logging.getLogger(__name__)


@deconstructible
class DateUploadPath(object):
    """DateUploadPath Helper.

    This class help to construct file upload into UUID format
    """

    def __init__(self, sub_path):
        """Class initializer."""
        now = timezone.now()
        sub_path = os.path.join(sub_path, now.strftime('%Y/%m/%d'))
        self.path = sub_path

    def __call__(self, instance, file_name):
        """Class callback."""
        _, ext = os.path.splitext(file_name)
        file_name = _ if file_name else uuid.uuid4().hex
        if ext:
            file_name = f'{file_name}{ext}'
        ret = os.path.join(self.path, file_name)
        return ret


def remove_filefield_file(_file: models.FileField):
    """Remove File from storage."""
    if _file:
        if isinstance(default_storage, GoogleCloudStorage):
            default_storage.delete(_file.name)
        else:
            path = _file.path
            try:
                default_storage.delete(path)
                logger.debug('Deleted %s', path)
            except Exception as e:
                logger.error(e)
