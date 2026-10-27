#Base exception for the application
class CS2TrackerError(Exception):
    pass

#Raised when match data structure is corrupted or invalid
class InvalidMatchDataError(CS2TrackerError):
    pass
