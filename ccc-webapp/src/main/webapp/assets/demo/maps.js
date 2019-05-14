var Maps = function () {

    var initGoogleMaps = function () {

        var myLatlng = new google.maps.LatLng(-37.814, 144.96332);

        var mapOptions = {
            zoom: 8,
            center: myLatlng,
            scrollwheel: false//we disable de scroll over the map, it is a really annoing when you scroll through page
            // styles: [{
            //     "featureType": "water",
            //     "stylers": [{
            //         "saturation": 43
            //     }, {
            //         "lightness": -11
            //     }, {
            //         "hue": "#0088ff"
            //     }]
            // }, {
            //     "featureType": "road",
            //     "elementType": "geometry.fill",
            //     "stylers": [{
            //         "hue": "#ff0000"
            //     }, {
            //         "saturation": -100
            //     }, {
            //         "lightness": 99
            //     }]
            // }, {
            //     "featureType": "road",
            //     "elementType": "geometry.stroke",
            //     "stylers": [{
            //         "color": "#808180"
            //     }, {
            //         "lightness": 54
            //     }]
            // }, {
            //     "featureType": "landscape.man_made",
            //     "elementType": "geometry.fill",
            //     "stylers": [{
            //         "color": "#ece2d9"
            //     }]
            // }, {
            //     "featureType": "poi.park",
            //     "elementType": "geometry.fill",
            //     "stylers": [{
            //         "color": "#ccdca1"
            //     }]
            // }, {
            //     "featureType": "road",
            //     "elementType": "labels.text.fill",
            //     "stylers": [{
            //         "color": "#767676"
            //     }]
            // }, {
            //     "featureType": "road",
            //     "elementType": "labels.text.stroke",
            //     "stylers": [{
            //         "color": "#ffffff"
            //     }]
            // }, {
            //     "featureType": "poi",
            //     "stylers": [{
            //         "visibility": "off"
            //     }]
            // }, {
            //     "featureType": "landscape.natural",
            //     "elementType": "geometry.fill",
            //     "stylers": [{
            //         "visibility": "on"
            //     }, {
            //         "color": "#b8cb93"
            //     }]
            // }, {
            //     "featureType": "poi.park",
            //     "stylers": [{
            //         "visibility": "on"
            //     }]
            // }, {
            //     "featureType": "poi.sports_complex",
            //     "stylers": [{
            //         "visibility": "on"
            //     }]
            // }, {
            //     "featureType": "poi.medical",
            //     "stylers": [{
            //         "visibility": "on"
            //     }]
            // }, {
            //     "featureType": "poi.business",
            //     "stylers": [{
            //         "visibility": "simplified"
            //     }]
            // }]

        };
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);

        var marker = new google.maps.Marker({
            position: myLatlng,
            title: "Hello World!"
        });

        // To add the marker to the map, call setMap();
        marker.setMap(map);
        $.ajax({
            url: resturi + '/api/geo/lga',
            type: 'GET',
            contentType: 'application/json',
            success: function (json) {
                var response = JSON.parse(json);
                var coord;
                var arr1;
                var polygon1;
                for (var i = 0; i < response.length; i++) {
                        arr1 = new Array();
                        coord = response[i].geometry.coordinates[0];
                        for (var j = 0; j < coord.length; j++) {
                            arr1.push(new google.maps.LatLng(coord[j][1], coord[j][0]));
                        }
                        var polygon2 = new google.maps.Polygon({
                            path: arr1,
                            strokeColor: 'red',
                            strokeOpacity: 0.8,
                            strokeWeight: 3,
                            fillColor: 'red',
                            fillOpacity: 0.35,
                        });
                        polygon2.setMap(map);
                    }
            },
            error: function (msg, a) {
                alert(JSON.stringify(msg));
            }
        });
    };

    return {
        init: function () {
            initGoogleMaps();
        }
    };
}();

jQuery(document).ready(function () {
    Maps.init();
});