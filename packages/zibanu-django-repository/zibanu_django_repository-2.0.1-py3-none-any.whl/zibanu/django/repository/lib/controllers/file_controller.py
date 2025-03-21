# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2025. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2025. Todos los derechos reservados.

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         4/03/25
# Project:      Zibanu Django
# Module Name:  file_controller
# Description:
# ****************************************************************
import logging
import traceback
import os
from uuid import uuid4
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from zibanu.django.repository.models import File
from zibanu.django.lib import BaseModelController, FileUtils, CodeGenerator
from typing import Any

class FileController(BaseModelController):
    """ FileController class """
    def __init__(self, pk: int = None, **kwargs: dict[str, ...]) -> None:
        super().__init__(**kwargs)
        self._hash_method = settings.ZB_REPOSITORY_HASH_METHOD
        self._root_dir = settings.ZB_REPOSITORY_ROOT_DIR
        self._files_dir = settings.ZB_REPOSITORY_FILES_DIR
        self._multi_level_allowed = settings.ZB_REPOSITORY_MULTILEVEL_FILES_ALLOWED
        self._mixin_files_allowed = settings.ZB_REPOSITORY_MIX_FILES_CATS_ALLOWED


    class Meta:
        """ Metaclass for FileController """
        model = File
        fields = ["id", "code", "uuid", "generated_at", "description", "file_type", "checksum", "owner_id"]
        related_fields = ["file_extended", "file_tables"]

    @staticmethod
    def __validate_file(attrs) -> bool:
        b_return = True
        file_extended = attrs.get("file_extended", None)
        file_type = attrs.get("file_type", None)


        if file_extended is not None:
            category = file_extended.get("category", None)
            if category is not None:
                file_types = category.file_types
                if file_types is not None and file_type not in file_types:
                    raise ValidationError(_(f"Invalid file type '{file_type}'"))
                # Validate that the file could not be loaded on root category.from
                if category.is_root:
                    raise ValidationError(_(f"The root category does not support files upload."))
                if not category.files_allowed:
                    raise ValidationError(_(f"The category does not support files upload."))
        return b_return


    def save_from_file(self, file: Any, attrs: dict[str, ...]) -> Any:
        file_dir = os.path.join(self._root_dir, self._files_dir)
        file = FileUtils(file=file, hash_method=self._hash_method, file_dir=file_dir, overwrite=True)
        file_save = True
        if self.is_adding:
            # If it is a new file.
            code_gen = CodeGenerator(action="save_from_file")
            attrs["generated_at"] = file.created_at
            attrs["file_type"]  = file.file_suffix
            attrs["checksum"] = file.hash
            attrs["owner"] = self.request.user
            attrs["uuid"] = self._instance.uuid
            attrs["code"] = code_gen.get_alpha_numeric_code()
        else:
            #If it is and old file.
            if self._instance.checksum != file.hash:
                attrs["checksum"] = file.hash
                attrs["uuid"] = uuid4()
                attrs["file_type"] = file.file_suffix
            else:
                file_save = False
        if self.__validate_file(attrs):
            self.save(attrs)
            # Save file only if the new is different from old.
            if file_save:
                file.file_name = self._instance.file_name
                file.save()




