# AUTHOR: Brian Pankau
# DATE: 6 June 2017
# CLASS: UWLAX DS710 SUMMER 2017 
# ASSIGNMENT: 2 R program 
# CODE:
#
my_airport = read.csv("C:/Users/bpankau/Documents/GitHub/ds710summer2017assignment2/airport1.csv")
attach(my_airport)
airport_count = 0
passenger_total = 0
passenger_mean = 0
for(airport_index in 1:length(Airport)){
    if (Scheduled_Departures[airport_index] < Performed_Departures[airport_index]){
        print (Airport[airport_index])
        airport_count = airport_count + 1
		passenger_total = passenger_total = Passengers[airport_index]
    }
}
passenger_mean = passenger_total / airport_count
sprintf ("PASSENGER TOTAL = %i", passenger_total)
sprintf ("AIRPORT COUNT = %i", airport_count)
sprintf ("PASSENGER MEAN = %5.1f", passenger_mean)
