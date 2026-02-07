import json
import uuid

from django.db import models
from django.template import Template, Context


# Create your models here.
class TemplateFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    file = models.FileField()
    num_slots = models.IntegerField()

    def render(self, data):
        # Load the contents of self.file, which will be a django template
        self.file.open('r')
        template_content = self.file.read()
        self.file.close()

        # Render the template with the given data using django's renderer
        template = Template(template_content)
        context = Context({"data": data})

        # Pass the context as {"data": data}
        return template.render(context)

    def render_sample(self):
        return self.render(['SAMPLE'] * self.num_slots)

    def slot_iterator(self):
        return range(self.num_slots)

    def __str__(self):
        return self.name


class CustomizedFile(models.Model):
    guest_name = models.CharField(max_length=255)
    template = models.ForeignKey(TemplateFile, on_delete=models.CASCADE)
    slot_data = models.TextField()  # A json-formatted list of strings
    created = models.DateTimeField(auto_now_add=True)

    def render(self):
        data = json.loads(self.slot_data)
        return self.template.render(data)

    def __str__(self):
        return f"{self.guest_name}'s customized {self.template.name}"