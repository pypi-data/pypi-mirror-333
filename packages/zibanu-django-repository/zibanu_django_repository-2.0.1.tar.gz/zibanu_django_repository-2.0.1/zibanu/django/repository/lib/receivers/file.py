# -*- coding: utf-8 -*-

#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2025. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2025. Todos los derechos reservados.

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         18/02/25
# Project:      Zibanu Django
# Module Name:  file
# Description:
# ****************************************************************
from django.db.models.signals import post_save
from django.dispatch import receiver
from zibanu.django.repository.models import File


@receiver(post_save, sender=File)
def file_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        pass