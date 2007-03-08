from opal.db import models
from opal.utils.translation import gettext_lazy as _

class ContentTypeManager(models.Manager):
    def get_for_model(self, model):
        """
        Returns the ContentType object for the given model, creating the
        ContentType if necessary.
        """
        opts = model._meta
        # The str() is needed around opts.verbose_name because it's a
        # opal.utils.functional.__proxy__ object.
        ct, created = self.model._default_manager.get_or_create(app_label=opts.app_label,
            model=opts.object_name.lower(), defaults={'name': str(opts.verbose_name)})
        return ct

class ContentType(models.Model):
    name = models.CharField(maxlength=100)
    app_label = models.CharField(maxlength=100)
    model = models.CharField(_('python model class name'), maxlength=100)
    objects = ContentTypeManager()
    class Meta:
        verbose_name = _('content type')
        verbose_name_plural = _('content types')
        db_table = 'django_content_type'
        ordering = ('name',)
        unique_together = (('app_label', 'model'),)

    def __str__(self):
        return self.name

    def model_class(self):
        "Returns the Python model class for this type of content."
        from opal.db import models
        return models.get_model(self.app_label, self.model)

    def get_object_for_this_type(self, **kwargs):
        """
        Returns an object of this type for the keyword arguments given.
        Basically, this is a proxy around this object_type's get_object() model
        method. The ObjectNotExist exception, if thrown, will not be caught,
        so code that calls this method should catch it.
        """
        return self.model_class()._default_manager.get(**kwargs)
