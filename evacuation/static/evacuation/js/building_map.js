
var map;
var currentFloor = 1;

var obstacleIcon = L.icon({
    iconUrl: images_url + 'delete2.png',
    iconSize: [30, 30]
});

var exitIds = {
//    exit1: '5b68fc6e7c31b70004d8b26a',
//    exit2: '5b692739dac0a20004f2ebdd',
//    exit3: '5b692754f3f9dd0004e190d0',
//    exit4: '5b692775f3f9dd0004e190d2',
    exit5: '5b7bb1b79721cb0013906134',
    exit6: '5b7bb1dba6bdda00137ca780',
    exit7: '5b7bb24470759d00134db139',

}

function Place(mwPlace){
    this.mwPlace = mwPlace;
    this.exitRoutes = new Array();

    this.sortRoutes = function(){
        this.exitRoutes.sort(function(er1, er2){
            return er1.distance - er2.distance;
        });
    }

    this.getRoutesAndDisplay = function(){
        startLoading();
        var self = this;
        var blocked = false;
        var numRoutes = 3;
        for(exitId in exitIds){
            blocked = false;
            for(i in obstacles){
                var obstacle = obstacles[i].fields;
                if(obstacle.place_id == exitIds[exitId]){
                    blocked = true;
                    numRoutes--;
                    break;
                }
            }
            if(blocked)
                continue;
            Mapwize.Api.getDirections({placeId: this.mwPlace._id}, {placeId: exitIds[exitId]}, null, null, function(err, directions){
                if (err) {
                    console.error('An error occur during direction fetching', err);
                    stopLoading();
                }
                else {
                    self.exitRoutes.push(directions);
                    if(self.exitRoutes.length >= numRoutes){
                        self.sortRoutes();
                        map.startDirections(self.exitRoutes[0]);
                    }
                }
                stopLoading();
            });
        }
    }
}

function Location(lat, lng){
    this.lat = lat;
    this.lng = lng;
    this.floor = currentFloor;
    this.exitRoutes = new Array();

    this.sortRoutes = function(){
        this.exitRoutes.sort(function(er1, er2){
            return er1.distance - er2.distance;
        });
    }

    this.getRoutesAndDisplay = function(){
        startLoading();
        var self = this;
        var blocked = false;
        var numRoutes = 3;
        for(exitId in exitIds){
            blocked = false;
            for(i in obstacles){
                var obstacle = obstacles[i].fields;
                if(obstacle.place_id == exitIds[exitId]){
                    blocked = true;
                    numRoutes--;
                    break;
                }
            }
            if(blocked)
                continue;
            Mapwize.Api.getDirections({latitude: self.lat, longitude: self.lng, floor: self.floor}, {placeId: exitIds[exitId]}, null, null, function(err, directions){
                if (err) {
                    console.error('An error occur during direction fetching', err);
                    stopLoading();
                }
                else {
                    self.exitRoutes.push(directions);
                    if(self.exitRoutes.length >= numRoutes){
                        self.sortRoutes();
                        map.startDirections(self.exitRoutes[0]);
                        stopLoading();
                    }
                }
            });
        }
    }
}

function startLoading(){
    $('#staticModal').show();
}

function stopLoading(){
    $('#staticModal').hide();
}

$(document).ready(function($) {
    startLoading();
    map = Mapwize.map('indoor-map', {
        apiKey: 'e32cf47a2a7a0df9e93d13fa4535b940',
        center: [-37.803704, 144.959694],
        zoom: 19,
        floor: currentFloor,
    }, function (err, mapInstance) {
        if (err) {
            console.error('An error occur during map initialization', err);
        }
        else {
            console.log('map is now loaded');
            // mapInstance.showDirections({placeId: '5b6904757c31b70004d8b28b'}, {placeId: '5b68fc6e7c31b70004d8b26a'});
        }
        stopLoading();
    });

    for(i in obstacles){
        var obstacle = obstacles[i].fields;
        L.marker([obstacle.latitude, obstacle.longitude], {icon: obstacleIcon, zIndexOffset: 100}).addTo(map);
    }

    map.on('placeClick', function (e) {
        console.log(e.place);
        if(e.place.placeType.name != 'ISO7010-E001' && e.place.placeType.name != 'ISO7010-E002'){
            map.stopDirections();
            var place = new Place(e.place);
            place.getRoutesAndDisplay();
        }
    });

    map.on('click', function (e) {
        map.stopDirections();
        var location = new Location(e.latlng.lat, e.latlng.lng);
        location.getRoutesAndDisplay();
    });

    map.on('floorChange', function (e) {
        currentFloor = e.floor;
        if(currentFloor == 0){
            exitIds = {
                exit1: '5b68fc6e7c31b70004d8b26a',
                exit2: '5b692739dac0a20004f2ebdd',
                exit3: '5b692754f3f9dd0004e190d0',
                exit4: '5b692775f3f9dd0004e190d2',
            }
        }
        else{
            exitIds = {
                exit5: '5b7bb1b79721cb0013906134',
                exit6: '5b7bb1dba6bdda00137ca780',
                exit7: '5b7bb24470759d00134db139',
            }
        }
    });
});
