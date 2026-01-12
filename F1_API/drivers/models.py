from django.db import models
from django.conf import settings

# Create your models here.
class Driver(models.Model):
    driver_id = models.CharField(max_length=100, unique=True, db_index=True)

    #Basic driver info
    given_name = models.CharField(max_length=100)
    family_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=100)

    #Driver Specific info
    permanent_number = models.IntegerField(null=True, blank=True)
    code = models.CharField(max_length=100, null=True, blank=True)

    #urls and images
    driver_image = models.URLField(null=True, blank=True)
    wikipedia_url = models.URLField(null=True, blank=True) #provided by the Jolpica api

    #CAREER Stats
    total_races = models.IntegerField(null=True, blank=True)
    total_wins = models.IntegerField(null=True, blank=True)
    total_podiums = models.IntegerField(null=True, blank=True)

    #METADATA
    last_updated = models.DateTimeField(auto_now=True) #used to know when data was last synced from the API
    created_at = models.DateTimeField(auto_now_add=True) # used to know when a driver was added into the database

    class Meta:
        ordering = ['family_name', 'given_name']

    def __str__(self):
        return f"{self.given_name} {self.family_name}"
    
    @property
    def full_name(self):
        return f"{self.given_name} {self.family_name}"

# Teams that a driver has raced for throughout their career
class DriverConstructorHistory(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='constructor_history')
    constructor_id = models.CharField(max_length=100)
    constructor_name = models.CharField(max_length=100)

    #Year Range
    first_year = models.IntegerField()
    last_year = models.IntegerField()

    #statistics with the Team
    races_with_constructors = models.IntegerField()
    wins_with_constructors = models.IntegerField()
    podiums_with_constructors = models.IntegerField()

    class Meta:
        ordering = ['first_year']
        unique_together = ['driver', 'constructor_id', 'first_year']

    def __str__(self):
        return f"{self.driver.full_name} - {self.constructor_name} ({self.first_year}-{self.last_year})"
    
class RaceResult2025(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, related_name='results_2025')

    # Race Identification
    round_number = models.IntegerField()
    race_name = models.CharField(max_length=100)
    circuit_name = models.CharField(max_length=100)
    race_date = models.DateField()

    #Race Results
    grid_psoition = models.IntegerField()
    final_position = models.IntegerField()
    position_text = models.CharField(max_length=100)
    points = models.FloatField()
    status = models.CharField(max_length=100)
    laps_completed = models.IntegerField()
    fastest_lap_rank = models.IntegerField(null=True, blank=True) #null if they did not set the fastest lap
    
    class Meta:
        ordering = ['round_number']
        unique_together = ['driver', 'round_number']

    def __str__(self):
        return f"{self.driver.full_name} - {self.race_name} ({self.round_number})"
    
    