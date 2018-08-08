
var map;

var exitIds = {
    exit1: '5b68fc6e7c31b70004d8b26a',
    exit2: '5b692739dac0a20004f2ebdd',
    exit3: '5b692754f3f9dd0004e190d0',
    exit4: '5b692775f3f9dd0004e190d2',
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
        var self = this;
        for(exitId in exitIds){
            Mapwize.Api.getDirections({placeId: this.mwPlace._id}, {placeId: exitIds[exitId]}, null, null, function(err, directions){
                if (err) {
                    console.error('An error occur during direction fetching', err);
                }
                else {
                    self.exitRoutes.push(directions);
                    if(self.exitRoutes.length >= 4){
                        self.sortRoutes();
                        map.startDirections(self.exitRoutes[0]);
                    }
                }
            });
        }
    }
}

function Location(lat, lng){
    this.lat = lat;
    this.lng = lng;
    this.exitRoutes = new Array();

    this.sortRoutes = function(){
        this.exitRoutes.sort(function(er1, er2){
            return er1.distance - er2.distance;
        });
    }

    this.getRoutesAndDisplay = function(){
        var self = this;
        for(exitId in exitIds){
            Mapwize.Api.getDirections({latitude: self.lat, longitude: self.lng, floor: 1}, {placeId: exitIds[exitId]}, null, null, function(err, directions){
                if (err) {
                    console.error('An error occur during direction fetching', err);
                }
                else {
                    self.exitRoutes.push(directions);
                    if(self.exitRoutes.length >= 4){
                        self.sortRoutes();
                        map.startDirections(self.exitRoutes[0]);
                    }
                }
            });
        }
    }
}

$(document).ready(function($) {
    map = Mapwize.map('myMapId', {
        apiKey: 'e32cf47a2a7a0df9e93d13fa4535b940',
        center: [-37.803704, 144.959694],
        zoom: 19,
        floor: 1,
    }, function (err, mapInstance) {
        if (err) {
            console.error('An error occur during map initialization', err);
        }
        else {
            console.log('map is now loaded');
            mapInstance.showDirections({placeId: '5b6904757c31b70004d8b28b'}, {placeId: '5b68fc6e7c31b70004d8b26a'});
        }
    });

    map.on('placeClick', function (e) {
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

    map.on('click', function (e) {
        map.stopDirections();
        var location = new Location(e.latlng.lat, e.latlng.lng);
        location.getRoutesAndDisplay();
    });
});
