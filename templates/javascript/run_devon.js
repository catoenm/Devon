// In the following example, markers appear when the user clicks on the map.
// The markers are stored in an array.
// The user can then click an option to hide, show or delete the markers.
var map;
var markers = [];
var marker_count = 0;

function initMap() {
    var haightAshbury = {lat: 37.769, lng: -122.446};

    map = new google.maps.Map(document.getElementById('view'), {
        zoom: 12,
        center: haightAshbury,
        mapTypeId: 'terrain'
    });

    // This event listener will call addMarker() when the map is clicked.
    map.addListener('click', function(event) {
        addMarker(event.latLng);
    });

    // Adds a marker at the center of the map.
    addMarker(haightAshbury);
}

var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() {
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }

        anHttpRequest.open( "GET", aUrl, true );
        anHttpRequest.send( null );
    }
}



// Adds a marker to the map and push to the array.
function addMarker(location) {
    $.ajax({
      url: 'http://127.0.0.1:5000/'
    });

    if(marker_count < 2) {
        marker_count++;
        var marker = new google.maps.Marker({
            position: location,
            map: map
        });
        markers.push(marker);
    } else {
        deleteMarkers()
    }
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
    setMapOnAll(null);
}

// Shows any markers currently in the array.
function showMarkers() {
    setMapOnAll(map);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
    clearMarkers();
    markers = [];
    marker_count = 0;
}