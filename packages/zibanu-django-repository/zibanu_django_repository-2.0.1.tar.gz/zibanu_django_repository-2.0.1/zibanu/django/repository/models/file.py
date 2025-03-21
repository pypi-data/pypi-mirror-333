# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2023. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2023. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         2/02/23 16:13
# Project:      Zibanu Django Project
# Module Name:  models
# Description:
# ****************************************************************
import uuid
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from zibanu.django.db import models
from zibanu.django.repository.lib import managers


class File(models.Model):
    """
    Model class of document entity to store and manage document data.
    """
    code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_("Validation Code"))
    uuid = models.UUIDField(default=uuid.uuid4, verbose_name=_("UUID File"))
    owner = models.ForeignKey(get_user_model(), verbose_name=_("Owner"), on_delete=models.PROTECT)
    generated_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Generated At"))
    description = models.CharField(max_length=150, blank=False, null=False, verbose_name=_("Description"), default="")
    file_type = models.CharField(max_length=6, default="pdf", verbose_name=_("File Type"))
    checksum = models.CharField(max_length=64, blank=True, null=True, verbose_name=_("Checksum"), editable=False)
    # Set default Manager
    objects = managers.File()

    class Meta:
        """
        Metaclass for Document model class.
        """
        verbose_name = _("File")
        verbose_name_plural = _("Files")
        constraints = [
            models.UniqueConstraint(fields=("code", ), name="UNQ_files_code"),
            models.UniqueConstraint(fields=("uuid", ), name="UNQ_files_uuid")
        ]

    def __str__(self):
        """ Return human-readable string representation. """
        file_str = self.file_name
        if hasattr(self, "file_extended") and self.file_extended is not None:
            file_str = self.file_extended.title + " ({})".format(file_str)
        return file_str

    @property
    def file_name(self) -> str:
        """ Get file name without path."""
        return f"{self.uuid.hex}.{self.file_type}"

    @property
    def file_url(self) -> str:
        """ Return file url."""
        import os
        from django.conf import settings
        from zibanu.django.lib import FileUtils
        file_dir = os.path.join(settings.ZB_REPOSITORY_ROOT_DIR, settings.ZB_REPOSITORY_FILES_DIR)
        file_utils = FileUtils(file_name=self.file_name, file_dir=file_dir)

        return file_utils.file_url

    def clean(self):
        """
        Override method to clean document data.
        Returns
        -------
        None
        """
        self.file_type = self.file_type.lower()
        super().clean()

