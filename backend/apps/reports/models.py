from django.db import models

from utils.models import BranchScopedModel


class DynamicReport(BranchScopedModel):
    OUTPUT_FORMATS = [('excel', 'Excel'), ('pdf', 'PDF'), ('csv', 'CSV')]

    name = models.CharField(max_length=200)
    sql_query = models.TextField()
    output_format = models.CharField(max_length=10, choices=OUTPUT_FORMATS, default='csv')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
