# onebus-serial-display
Script to poll the onebusaway API and send formatted results to a serial LCD from a raspberry pi

Requires onebusaway api key [http://pugetsound.onebusaway.org/p/OneBusAwayApiService.action] set via environment variable and a stops.json file with the following structure:

{ "stops":                               
  [                                      
      { "label": "Stop1", "id": "1_75502"}, 
      { "label": "Stop2", "id": "1_5622"}   
  ]                                      
}                                        
