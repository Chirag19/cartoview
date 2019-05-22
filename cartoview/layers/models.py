import jsonfield
from cartoview.base_resource.models import BaseModel
from cartoview.connections.models import Server
from cartoview.connections.utils import get_server_by_value
from cartoview.fields import ListField
from cartoview.validators import ListValidator
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from guardian.shortcuts import assign_perm

from .validators import validate_projection


class BaseLayer(BaseModel):
    name = models.CharField(max_length=255)
    attribution = models.TextField(null=True, blank=True)
    bounding_box = ListField(null=False, blank=False, default=[0, 0, 0, 0], validators=[
                             ListValidator(min_length=4, max_length=4), ])
    projection = models.CharField(max_length=30, blank=False, null=False,
                                  validators=[validate_projection, ])
    server = models.ForeignKey(Server, on_delete=models.CASCADE,
                               related_name='layers')
    valid = models.BooleanField(default=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                              related_name="layers", blank=True, null=True)
    url = models.URLField(verbose_name='layer URL', null=True, blank=True)
    tile_size = ListField(null=False, blank=False, default=[256, 256], validators=[
                          ListValidator(min_length=2, max_length=2), ])
    urls = ListField(null=True, blank=True)
    wrap_x = models.BooleanField(help_text="Whether to wrap the world horizontally.", default=True)
    is_base = models.BooleanField(default=False, null=False, blank=False)
    @property
    def server_type(self):
        if not self.server:
            return None
        return self.server.server_type

    @property
    def server_url(self):
        if self.server:
            return self.server.url
        return None

    @property
    def server_operations(self):
        if self.server:
            return self.server.operations
        return {}

    @property
    def proxyable(self):
        if self.server:
            if self.server.connection:
                return True
            else:
                return False
        return False

    @property
    def server_proxy(self):
        return '{}?url='.format(reverse_lazy('api:server_proxy',
                                             args=(self.server.pk,)))

    def set_public_permission(self):
        public_group = Group.objects.get(name=settings.ANONYMOUS_GROUP_NAME)
        assign_perm("view_layer", public_group, self)

    @property
    def layer_type(self):
        if self.server:
            server = get_server_by_value(self.server.server_type)
            return server.type
        return None

    class Meta:
        abstract = True
        unique_together = (("name", "server"),)


class Layer(BaseLayer):
    extra = jsonfield.JSONField()

    def __str__(self):
        return "{}({},{})<{}>".format(self.name, self.layer_type,
                                      self.server_type, self.server)


@receiver(pre_save, sender=Layer)
def layer_pre_save(sender, instance, **kwargs):
    if instance.server and not instance.url:
        instance.url = instance.server.url


@receiver(post_save, sender=Layer)
def layer_post_save(sender, instance, created, **kwargs):
    if created and instance.owner and \
            instance.owner.username != settings.ANONYMOUS_USER_NAME:
        users = get_user_model().objects.filter(is_superuser=True,)
        if instance.owner:
            users = users.union(get_user_model().objects.filter(
                username=instance.owner.username))
        for user in users:
            assign_perm("view_layer", user, instance)
            assign_perm("change_layer", user, instance)
            assign_perm("delete_layer", user, instance)
        try:
            public_group = Group.objects.get(
                name=settings.ANONYMOUS_GROUP_NAME)
            assign_perm("view_layer", public_group, instance)
        except ObjectDoesNotExist:
            pass
