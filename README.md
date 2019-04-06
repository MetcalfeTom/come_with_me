## Come With Me

This project will (eventually) have some nice functionality - the ability to take the top attractions
 and restaurants from TripAdvsior and implant them directly into your Google Maps as pins (since navigation
 is easier with Maps)
 
Unfortunately TripAdvsior do not allow public access to their API, so I have had to resort to scraping
 for now unless there is a better solution
 
To run from command line, you will need the city name and Tripadvisor city ID.  Best way to get this is
visit their website for corresponding city, I will automate it later.

Example:
```buildoutcfg
python main.py 190454 vienna
```