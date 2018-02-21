# coding: utf-8

# Get total time of the trip
def tripTime(trip):
    if type(trip) == list: # If it's a multi-line trip
        hr1, min1 = trip[0].get("Origin").get("time").split(":")
        hr2, min2 = trip[-1].get("Destination").get("time").split(":")
        hr1, hr2, min1, min2 = int(hr1), int(hr2), int(min1), int(min2)

        # If delay goes over midnight (23.59->00.01)
        if not trip[0].get("Origin").get("date") == trip[-1].get("Destination").get("date"):
            if hr1 < hr2:
                hr1 += 24
            else:
                hr2 += 24

    else: # If it's a single-line trip
        hr1, min1 = trip.get("Origin").get("time").split(":")
        hr2, min2 = trip.get("Destination").get("time").split(":")
        hr1, hr2, min1, min2 = int(hr1), int(hr2), int(min1), int(min2)

        # If trip passes midnight 
        if not trip.get("Origin").get("date") == trip.get("Destination").get("date"):
            if hr1 < hr2:
                hr1 += 24
            else:
                hr2 += 24

    # Turn hours into minutes to calculate difference
    min1 += hr1 * 60
    min2 += hr2 * 60
    triptime = min2 - min1
    tH = triptime // 60
    tM = triptime % 60

    return triptime, tH, tM

# Function for planning a trip. Searches for stops and gets a plan between them.
def plan(self, fr, to, time_, date, arr, smallChangeTime):
    self.lastTripDepStop = fr
    self.lastTripArrStop = to
    
    toStop, toStopname = self.api.findStop(to)
    if not toStop:
        print("Destination stop not found.")
        return

    frStop, frStopname = self.api.findStop(fr)
    if not frStop:
        print("Origin stop not found.")
        return
    self.lastTripDepStop = frStopname
    self.lastTripArrStop = toStopname

    trip = self.api.getPlan(frStop, toStop, time_=time_, date=date, arr=arr, smallChangeTime=smallChangeTime)
    self.printPlan(trip, toStopname, frStopname)

# Search for stop and get departures
def dep(self, stop, time_, date):
    # Find stop
    stop, stopname = self.api.findStop(stop)
    if not stop:
        print("Stop not found.")
        return
    self.lastDepStop = stopname

    # Get departures from stop
    departures = self.api.getDepartures(stop, date=date, time_=time_)
    self.printDepartures(departures, stopname, date, time_)

# Function for getting total delay
def getDelay(times):
    # If a stop has realtime departure time
    if times.get("rtDepTime"):
        hr1, min1 = times.get("rtDepTime").split(":")
        hr2, min2 = times.get("depTime").split(":")
        rtDate = times.get("rtDepDate")
        date = times.get("depDate")

    # If a stop only has realtime arrival time
    elif times.get("rtArrTime"):
        hr1, min1 = times.get("rtArrTime").split(":")
        hr2, min2 = times.get("arrTime").split(":")
        rtDate = times.get("rtArrDate")
        date = times.get("arrDate")

    # If a stop only has one realtime time
    elif times.get("rtTime"):
        hr1, min1 = times.get("rtTime").split(":")
        hr2, min2 = times.get("time").split(":")
        rtDate = times.get("rtDate")
        date = times.get("date")

    # If the journey is cancelled
    elif times.get("cancelled") == "true":
        return " Inställd"
    else:
        return " Error"
        
    hr1, hr2, min1, min2 = int(hr1), int(hr2), int(min1), int(min2)

    # If the delay goes over midnight.
    if not rtDate == date:
        if hr1 < hr2:
            hr1 += 24
        else:
            hr2 += 24

    # Turn hours into minutes and calculate the difference
    min1 += hr1 * 60
    min2 += hr2 * 60
    delay = min1 - min2
    
    # Formatting
    if delay >= 0:
        delay = "+" + str(delay)
    else:
        delay = str(delay)
        
    return delay

if __name__ == "__main__":        
	print("This file is only supposed to be used as a module.")