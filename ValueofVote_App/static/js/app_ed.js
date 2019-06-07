// Creating map object

  var mapboxAccessToken = "{your access token here}";
  var map = L.map("map-ed", {
    center: [57.130367, -106.346771],
    zoom: 3,
  });

  
  // Adding tile layer
  lightMap=L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=" + mapboxAccessToken, {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.light",
  }).addTo(map);
  
  var link = "/ed_geojson";
  
  // Grabbing our GeoJSON data..
  d3.json(link, function(data) {
    // Creating a GeoJSON layer with the retrieved data
    L.geoJson(data).addTo(map);
    console.log(data);
  });
  