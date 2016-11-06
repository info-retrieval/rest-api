from django.db import models
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + (
    'es_index_name', 'es_type_name', 'es_mapping'
)


class H1(models.Model):
    title = models.CharField(max_length=1000)


class H2(models.Model):
    title = models.CharField(max_length=1000)


class H3(models.Model):
    title = models.CharField(max_length=1000)


class Document(models.Model):
    class Meta:
        es_index_name = 'foo'
        es_type_name = 't'
        es_mapping = {
            'properties': {
                'id': {'type': 'string', 'index': 'not_analyzed'},
                'title': {'type': 'string', 'index': 'not_analyzed'},
                'text': {'type': 'string', 'index': 'no'},
                'h1': {'type': 'string', 'store': 'yes', 'index': 'not_analyzed'},
                'h2': {'type': 'string', 'store': 'yes', 'index': 'not_analyzed'},
                'h3': {'type': 'string', 'store': 'yes', 'index': 'not_analyzed'}
            }
        }
    id = models.CharField(max_length=10, primary_key=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    h1 = models.ManyToManyField(H1, null=True, blank=True)
    h2 = models.ManyToManyField(H2, null=True, blank=True)
    h3 = models.ManyToManyField(H3, null=True, blank=True)

    def es_repr(self):
        data = {}
        mapping = self._meta.es_mapping
        data['_id'] = self.pk
        for field_name in mapping['properties'].keys():
            data[field_name] = self.field_es_repr(field_name)
        return data

    def field_es_repr(self, field_name):
        config = self._meta.es_mapping['properties'][field_name]
        if hasattr(self, 'get_es_%s' % field_name):
            field_es_value = getattr(self, 'get_es_%s' % field_name)()
        else:
            if config['type'] == 'object':
                related_object = getattr(self, field_name)
                field_es_value = {}
                field_es_value['_id'] = related_object.pk
                for prop in config['properties'].keys():
                    field_es_value[prop] = getattr(related_object, prop)
            else:
                field_es_value = getattr(self, field_name)
        return field_es_value

    def get_es_h1(self):
        if not self.h1.exists():
            return []
        return [c.title for c in self.h1.all()]

    def get_es_h2(self):
        if not self.h2.exists():
            return []
        return [c.title for c in self.h2.all()]

    def get_es_h3(self):
        if not self.h3.exists():
            return []
        return [c.title for c in self.h3.all()]


class Search(models.Model):
    query = models.CharField(max_length=200)
    date = models.DateTimeField
    results = models.CharField
