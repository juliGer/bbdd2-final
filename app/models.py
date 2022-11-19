from pyexpat import model
from djongo import models


class FlightPrice(models.Model):
    legId = models.TextField()
    searchDate = models.TextField(null=True)
    flightDate = models.TextField(null=True)
    startingAirport = models.TextField(null=True)
    destinationAirport = models.TextField(null=True)
    fareBasisCode = models.TextField(null=True)
    travelDuration = models.TextField(null=True)
    elapsedDays = models.IntegerField(null=True)
    isBasicEconomy = models.BooleanField(null=True)
    isRefundable = models.BooleanField(null=True)
    isNonStop = models.BooleanField(null=True)
    baseFare = models.FloatField(null=True)
    totalFare = models.FloatField(null=True)
    seatsRemaining = models.IntegerField(null=True)
    totalTravelDistance = models.IntegerField(null=True)
    segmentsDepartureTimeEpochSeconds = models.TextField(null=True)
    segmentsDepartureTimeRaw = models.TextField(null=True)
    segmentsArrivalTimeEpochSeconds = models.TextField(null=True)
    segmentsArrivalTimeRaw = models.TextField(null=True)
    segmentsArrivalAirportCode = models.TextField(null=True)
    segmentsDepartureAirportCode = models.TextField(null=True)
    segmentsAirlineName = models.TextField(null=True)
    segmentsAirlineCode = models.TextField(null=True)
    segmentsEquipmentDescription = models.TextField(null=True)
    segmentsDurationInSeconds = models.TextField(null=True)
    segmentsDistance = models.TextField(null=True)
    segmentsCabinCode = models.TextField(null=True)
    objects = models.DjongoManager()
