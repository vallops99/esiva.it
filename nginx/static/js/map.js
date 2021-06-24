"use strict";

const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);

function createMap() {
  var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/satellite-streets-v11',
    center: [10, 57],
    zoom: 3.3,
    scrollZoom: false,
    attributionControl: false
  })
  .addControl(
    new mapboxgl.NavigationControl({
      showCompass: false
    })
  )
  .on('load', () => {

    if (window.onlyBok) {
      if (window.livePoint.length > 0) {
        let el = document.createElement('div');
        el.className = 'marker-live';
        new mapboxgl.Marker(el)
          .setLngLat([window.livePoint[0], window.livePoint[1]])
          .addTo(map);
      }
    }
    else {
      locations.forEach(marker => {

        // create a HTML element for each feature
        let el = document.createElement('div');
        el.className = 'marker';

        // make a marker for each feature and add to the map
        new mapboxgl.Marker(el)
          .setLngLat([marker.coordinate_y, marker.coordinate_x])
          .addTo(map);
      });

      map.addSource('route', {
        'type': 'geojson',
        'data': {
          'type': 'Feature',
          'properties': {},
          'geometry': {
            'type': 'LineString',
            'coordinates': window.road
          }
        }
      }).addLayer({
        'id': 'route',
        'type': 'line',
        'source': 'route',
        'layout': {
          'line-join': 'round',
          'line-cap': 'round'
        },
        'paint': {
          'line-color': '#4646FF',
          'line-width': 8
        }
      });
    }
  });

  if (vw < 980) {
    map.dragPan.disable();
    map.zoom = 3;
  }
}

(function() {
  createMap();
})();
