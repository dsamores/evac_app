
var map;
var landmarkGroup;
var obstacleGroup;
var startLocation;

var zoom;
var minZoom, maxZoom;
var maxBounds;

var obstacleIcon = L.icon({
    iconUrl: imagesUrl + 'blocked.png',
    iconSize: [30, 30]
});

var exitIds = {
//    'exit1': '5b68fc6e7c31b70004d8b26a',
//    'exit2': '5b692739dac0a20004f2ebdd',
//    'exit3': '5b692754f3f9dd0004e190d0',
//    'exit4': '5b692775f3f9dd0004e190d2',
    'exit5': '5b7bb1b79721cb0013906134',
    'exit6': '5b7bb1dba6bdda00137ca780',
    'exit7': '5b7bb24470759d00134db139',

}

var assemblyAreaId = [
    '5b68f6dd85cc1800048455cd',
    '5b976807f2aaa60013ec2630',
    '5b9768280ac4690013c499e0',
    '5b976849f2aaa60013ec2633',
];


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
    this.marker = null;

    this.sortRoutes = function(){
        this.exitRoutes.sort(function(er1, er2){
            return er1[1].distance - er2[1].distance;
        });
    }

    this.getRoutesAndDisplay = function(){
        startLoading();
        var self = this;
        var blocked = false;
        var numRoutes = Object.keys(exitIds).length;
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
                    var eId = reverseRouteLookup(directions.to.placeId);
                    self.exitRoutes.push([eId, directions]);
                    if(self.exitRoutes.length >= numRoutes){
                        self.sortRoutes();

                        Mapwize.Api.getDirections({latitude: self.lat, longitude: self.lng, floor: self.floor}, {placeId: assemblyAreaId[self.floor]}, [{placeId: exitIds[self.exitRoutes[0][0]]}], null, function(err1, directions1){
                            if (err1) {
                                console.error('An error occur during direction fetching', err);
                                stopLoading();
                            }
                            else {
                                map.startDirections(directions1);
                                map.setMinZoom(minZoom);
                                map.setMaxZoom(maxZoom);
                                map.setMaxBounds(null);

                                self.marker = L.marker([self.lat, self.lng], {
                                    icon: new L.DivIcon({
                                        className: 'landmark',
                                        html:   '<img class="landmark-icon" src="static/evacuation/images/icons/start-pin.png" />' +
                                                '<div class="landmark-text">Start</div>'
                                    }),
                                    zIndexOffset: 100
                                });
                                self.marker.addTo(map);

                                stopLoading();

                            }
                        });
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
    var initialZoom, initialCenter;
    if(showAssembly){
        initialZoom = 17;
        initialCenter = [-37.802894303416345, 144.96115372516218];
    }
    else{
        initialZoom = 19;
        initialCenter = [-37.803704, 144.959694];
    }
    map = Mapwize.map('indoor-map', {
        apiKey: 'e32cf47a2a7a0df9e93d13fa4535b940',
        center: initialCenter,
        zoom: initialZoom,
        floor: currentFloor,
        showUserPosition: false,
        mapwizeAttribution: false,
        floorControlOptions: {'position': 'topright'},
        displayPlaces: false,
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
    landmarkGroup = L.layerGroup().addTo(map);
    obstacleGroup = L.layerGroup().addTo(map);

    map.on('placeClick', function (e) {
        console.log(e.place);
//        if(e.place.placeType.name != 'ISO7010-E001' && e.place.placeType.name != 'ISO7010-E002'){
//            map.stopDirections();
//            var place = new Place(e.place);
//            place.getRoutesAndDisplay();
//        }
    });

    map.on('click', function (e) {
        console.log('lat:', e.latlng.lat, 'lon:', e.latlng.lng);
        if(insideBuilding([e.latlng.lat, e.latlng.lng])){
            zoom = map.getZoom();
            minZoom = map.getMinZoom();
            maxZoom = map.getMaxZoom();
            map.setMinZoom(zoom);
            map.setMaxZoom(zoom);
            map.setMaxBounds(map.getBounds());

            map.stopDirections();
            if(startLocation && startLocation.marker)
                map.removeLayer(startLocation.marker);
            startLocation = new Location(e.latlng.lat, e.latlng.lng);
            startLocation.getRoutesAndDisplay();
            (new Interaction('map-exitroute', 'lat:' + e.latlng.lat + ',lon:' + e.latlng.lng, window.location.href, null)).save();
        }
    });

    map.on('floorChange', function (e) {
        currentFloor = e.floor;
        if(startLocation && startLocation.marker){
            if(startLocation.floor == currentFloor){
                startLocation.marker.addTo(map);
            }
            else{
                map.removeLayer(startLocation.marker);
            }
        }
        if(currentFloor == 0){
            exitIds = {
                'exit1': '5b68fc6e7c31b70004d8b26a',
                'exit2': '5b692739dac0a20004f2ebdd',
                'exit3': '5b692754f3f9dd0004e190d0',
                'exit4': '5b692775f3f9dd0004e190d2',
            }
        }
        else if(currentFloor == 1){
            exitIds = {
                'exit5': '5b7bb1b79721cb0013906134',
                'exit6': '5b7bb1dba6bdda00137ca780',
                'exit7': '5b7bb24470759d00134db139',
            }
        }
        else if(currentFloor == 2){
            exitIds = {
                'exit8': '5b7c0245d224a900214bf8ac',
                'exit9': '5b7c026b447f35002bb5a13f',
                'exit10': '5b7c0290a7d5e8002b641c29',
            }
        }
        else if(currentFloor == 3){
            exitIds = {
                'exit11': '5b7c02b2d224a900214bf8b3',
                'exit12': '5b7c02d4a7d5e8002b641c4f',
                'exit13': '5b7c02f243d06c002ba60673',
            }
        }

        loadLandmarks(currentFloor);
        loadObstacles();
        saveMapEvent('map-floorChange');
    });

    map.on('zoomstart', function(e) {
        saveMapEvent('map-zoomstart');
    });

    map.on('zoomend', function(e) {
        saveMapEvent('map-zoomend');
    });

    map.on('movestart', function(e) {
        saveMapEvent('map-movestart');
    });

    map.on('moveend', function(e) {
        saveMapEvent('map-moveend');
    });

    $("#button-assembly-area").click(function (){
        map.panTo(new L.LatLng(-37.802894303416345, 144.96115372516218));
        map.setZoom(17);
    });

});

function saveMapEvent(eventName){
    var eventDescription = "zoom:" + map.getZoom() + ",center:" + map.getCenter();
    (new Interaction(eventName, eventDescription, window.location.href, null)).save();
}

function loadLandmarks(currentFloor){
    landmarkGroup.clearLayers();
    for(i in landmarks){
        var landmark = landmarks[i].fields;
        if(landmark.floor != currentFloor)
            continue;
        var landmarkIcon = L.icon({
            iconUrl: 'static/evacuation/images/icons/' + landmark.icon + '.png',
            iconSize: [30, 30]
        });
        L.marker([landmark.latitude, landmark.longitude], {
            icon: new L.DivIcon({
                className: 'landmark',
                html:   '<img class="landmark-icon" src="static/evacuation/images/icons/' + landmark.icon + '.png" />' +
                        '<span class"landmark-text">' + landmark.display_name + '</span>'
            }),
            zIndexOffset: 100
        }).addTo(landmarkGroup);
    }
}

function loadObstacles(){
    obstacleGroup.clearLayers();
    for(i in obstacles){
        var obstacle = obstacles[i].fields;
        for(var ei in exitIds){
            if(obstacle.place_id == exitIds[ei]){
                L.marker([obstacle.latitude, obstacle.longitude], {icon: obstacleIcon, zIndexOffset: 100}).addTo(obstacleGroup);
            }
        }
    }
}

function insideBuilding(point) {

    var vs = [
        [-37.80352392493654, 144.95930492877963],
        [-37.80338723255397, 144.95977833867073],
        [-37.804143805821965, 144.9601082503796],
        [-37.80407148665343, 144.95954632759097]
    ];

    var x = point[0], y = point[1];

    var inside = false;
    for (var i = 0, j = vs.length - 1; i < vs.length; j = i++) {
        var xi = vs[i][0], yi = vs[i][1];
        var xj = vs[j][0], yj = vs[j][1];

        var intersect = ((yi > y) != (yj > y))
            && (x < (xj - xi) * (y - yi) / (yj - yi) + xi);
        if (intersect) inside = !inside;
    }

    return inside;
};

function reverseRouteLookup(exitId){
    for(var i in exitIds){
        if(exitId == exitIds[i])
            return i;
    }
    return null;
}