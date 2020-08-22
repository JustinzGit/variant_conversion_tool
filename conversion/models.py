from django.db import models

class Gene(models.Model):
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence
        
