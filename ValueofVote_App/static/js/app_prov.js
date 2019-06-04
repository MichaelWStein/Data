


function build_prov_map() {

// Tile layer
lightMap=L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.light",
  accessToken: API_KEY
})

satelliteMap=L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.satellite",
  accessToken: API_KEY
})

// Define a baseMaps object to hold our base layers
var baseMaps = {
  "Light Map": lightMap,
  "Satellite": satelliteMap
};

var overlayMaps = {};
var map;

//Fill colors
function getColor(d) {
  return d > 12000000 ? '#800026' :
         d > 10000000  ? '#BD0026' :
         d > 8000000  ? '#E31A1C' :
         d > 5000000  ? '#FC4E2A' :
         d > 2000000   ? '#FD8D3C' :
         d > 1000000   ? '#FEB24C' :
         d > 500000   ? '#FED976' :
                    '#FFEDA0';
}

//Link to province geo-json
var prov_link = "/prov_geojson";


// Grabbing our GeoJSON data..
d3.json(prov_link, function(data) {
  // Creating a GeoJSON layer with the retrieved data
  var population = L.geoJson(data.features);
  
  //overlay population
  overlayMaps.Population=population;

  map = L.map("map-province", {
    center: [57.130367, -106.346771],
    zoom: 3,
    layers: [lightMap, population]
  });

  //coloring choropleth
  function style(population) {
    return {
        fillColor: getColor(population.properties.Population),
        weight: 2,
        opacity: 1,
        color: 'grey',
        dashArray: '3',
        fillOpacity: 0.7
    };
  
  }

  L.geoJson(data.features, {style: style}).addTo(map);

  //creating mouse-over event
  function highlightFeature(e) {
    var layer = e.target;

    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });

    if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
        layer.bringToFront();
    }
}

//mouseout
function resetHighlight(e) {
  population.resetStyle(e.target);
}

//click
function zoomToFeature(e) {
  map.fitBounds(e.target.getBounds());
}

function onEachFeature(feature, layer) {
  layer.on({
      mouseover: highlightFeature,
      mouseout: resetHighlight,
      click: zoomToFeature
  });

  layer.bindTooltip("<h6>" + feature.properties.PRENAME + "</h6><hr><h6>Population: "+ feature.properties.Population+"</h6>");
}

population = L.geoJson(data.features, {
  style: style,
  onEachFeature: onEachFeature
}).addTo(map);

//Legend
var legend = L.control({position: 'bottomright'});

legend.onAdd = function (map) {

    var div = L.DomUtil.create('div', 'info legend'),
        grades = [500000,1000000,2000000,5000000,8000000,10000000,12000000],
        labels = [];

    // loop through our density intervals and generate a label with a colored square for each interval
    for (var i = 0; i < grades.length; i++) {
        div.innerHTML +=
            '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
            grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
        console.log(getColor(grades[i] + 1));
    }

    return div;
};



L.control.layers(baseMaps,overlayMaps, {
    collapsed: false
}).addTo(map);

legend.addTo(map);

});

}

build_prov_map();


//bubble chart
d3.json("/prov_bubble", function(data) {
  // Creating a GeoJSON layer with the retrieved data
  var data = data;
  console.log(data);
  var cp = 35151728;

  
  var trace = {
    type: "scatter",
    mode: "markers",
    x: data.population,
    y: data.ridings,
    text: data.geo_name,
    marker: {
      color: ['blue','orange','orange','orange','blue','red','yellow','red','orange','red'],
      size: [10,50,30,30,15,70,25,75,40,65]
      // colorscale: 'YIOrRd',
    }
  };
        var scatter = [trace];
    
            var layout = {
              title: 'Value of Vote by Province',
              showlegend: false,
                  // height: 300,
                  // width: 300,
              xaxis: {
                title: {
                  text: 'Population',
                }
              },
          
                  yaxis: {
                    title: {
                      text: 'Ridings',
                    }
                  }
                };
            
                Plotly.newPlot("bubble", scatter, layout);

});
