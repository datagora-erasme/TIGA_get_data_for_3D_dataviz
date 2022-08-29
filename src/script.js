// Create the Mapbox map
mapboxgl.accessToken =
  "pk.eyJ1IjoiYmJlcnRoYXVkIiwiYSI6ImNrbms1bW1yaTA3cWUydnBtMmczZWlrY3MifQ.BvIypZJdZEpE5v0KMStArA";

var { MapboxLayer, HexagonLayer } = deck;

var stylesheet = "mapbox://styles/mapbox/dark-v10?optimize=true";

var map = new mapboxgl.Map({
  container: document.body,
  style: stylesheet,
  center: [4.85, 45.76],
  zoom: 9.5,
  pitch: 40.5,
  antialias: true
});

// Parameters
const filename = "data/data_processed.csv";

var capitauxPresent = false;

//TODO : extract value
d3.csv(filename).then(function (data) {
  capitauxPresent = data.columns.includes("capitaux");
});

const OPTIONS = ["radius", "opacity", "elevationScale"];

/*
old SECTOR_RANGE
const SECTOR_RANGE = [
  "Activités de services administratifs",
  "Activités extra-territoriales",
  "Activités financières et d'assurance",
  "Activités immobilières",
  "Activités spécialisées, scientifiques et tech.",
  "Administration publique",
  "Agriculture, sylviculture et pêche",
  "Arts, spectacles et activités récréatives",
  "Autres activités de services",
  "Commerce ; réparation d'automobiles ...",
  "Construction",
  "Enseignement",
  "Hébergement et restauration",
  "Industrie manufacturière",
  "Industries extractives",
  "Information et communication",
  "Production et distribution d'eau ...",
  "Production et distribution d'électricité ...",
  "Santé humaine et action sociale",
  "Transports et entreposage",
  "Données manquantes"
];
*/

const SECTOR_RANGE = [
  'Production et distribution d’électricité, de gaz et d’eau : gestion des déchets',
  'Autres industries manufacturières : réparation et installation de machines et d’équipements',
  'Métallurgie et fabrication de produits métalliques à l’exception des machines et des équipements',
  'Industrie pharmaceutique',
  'Fabrication de machines et équipements n.c.a.',
  'Industrie chimique',
  'Fabrication de denrées alimentaires, de boissons et de produits à base de tabac',
  'Fabrication de matériels de transport',
  'Fabrication de produits en caoutchouc et en plastique ainsi que d’autres produits minéraux non métalliques',
  'Fabrication d’équipements électriques',
  'Travail du bois, industries du papier et imprimerie',
  'Fabrication de textiles, industries de l’habillement, industrie du cuir et de la chaussure',
  'Fabrication de produits informatiques, électroniques et optiques',
  'Cokéfaction et raffinage',
  'Industries extractives'
];

// COLOR_RANGE length must be egal to SECTOR_RANGE length !
/*
const COLOR_RANGE = [
  [230, 25, 75],
  [60, 180, 75],
  [255, 225, 25],
  [0, 130, 200],
  [245, 130, 48],
  [145, 30, 180],
  [70, 240, 240],
  [240, 50, 230],
  [210, 245, 60],
  [250, 190, 212],
  [0, 128, 128],
  [220, 190, 255],
  [170, 110, 40],
  [255, 250, 200],
  [128, 0, 0],
  [170, 255, 195],
  [128, 128, 0],
  [255, 215, 180],
  [0, 0, 128],
  [255, 255, 255],
  [128, 128, 128]
];
*/

let COLOR_RANGE = [];

for (i in SECTOR_RANGE) {
  /*let value = i/SECTOR_RANGE.length*125 + 125;*/
  let value = 255 ;
  console.log(value);
  /*COLOR_RANGE.push([Math.floor(Math.random()*255), Math.floor(Math.random()*255), Math.floor(Math.random()*255)]);*/
  COLOR_RANGE.push([0, 0, value]);
}

const LIGHT_SETTINGS = {
  lightsPosition: [-0.144528, 49.739968, 8000, -3.807751, 54.104682, 8000],
  ambientRatio: 0.4,
  diffuseRatio: 0.6,
  specularRatio: 0.2,
  lightsStrength: [0.8, 0.0, 0.8, 0.0],
  numberOfLights: 2
};

// Legend

const legendCellSize = 15,
  margin = 10;
var legend = d3.select("#legend-display").append("svg");
legend.attr("height", COLOR_RANGE.length * legendCellSize + margin);
var panel = document.querySelector(".panel");
legend.attr("width", getComputedStyle(panel).width);

function componentToHex(c) {
  var hex = c.toString(16);
  return hex.length === 1 ? "0" + hex : hex;
}

function rgbToHex(rgb) {
  return (
    "#" +
    componentToHex(rgb[0]) +
    componentToHex(rgb[1]) +
    componentToHex(rgb[2])
  );
}

legend
  .selectAll("svg")
  .data(d3.range(COLOR_RANGE.length))
  .enter()
  .append("svg:rect")
  .attr("height", legendCellSize / 2 + "px")
  .attr("width", legendCellSize * 1.5 + "px")
  .attr("x", 0)
  .attr("y", (d) => d * legendCellSize + margin)
  .style("fill", (d) => rgbToHex(COLOR_RANGE[d]))
  .attr("rx", 2)
  .attr("ry", 2);

var SECTOR_RANGE_DISPLAY = d3.range(SECTOR_RANGE.length);

// Filter data based on 3 filters (sector, workforce and investment)

var valueCapitaux = 0,
  valueRH0 = 1,
  valueRH1 = Infinity;

function filterData(d) {
  const sectorFilter = SECTOR_RANGE_DISPLAY.includes(+d.secteur);
  const workforceFilter = +d.RH >= valueRH0 && +d.RH <= valueRH1;
  var investmentFilter = true;
  if (capitauxPresent) {
    investmentFilter = +d.capitaux >= valueCapitaux;
  }
  return sectorFilter && workforceFilter && investmentFilter;
}

legend
  .selectAll("svg")
  .data(d3.range(COLOR_RANGE.length))
  .enter()
  .append("text")
  .attr("id", (d) => d)
  .attr("x", 30)
  .attr("y", (d) => d * legendCellSize + 2 * margin)
  .text((d) => SECTOR_RANGE[d])
  .style("fill", "white")
  .on("mouseover", function (event, d) {
    d3.select(this).style("cursor", "pointer");
    d3.select(this).style("fill", "grey");
  })
  .on("mouseout", function (event, d) {
    d3.select(this).style("fill", "white");
  })
  .on("click", function (event, d) {
    if (SECTOR_RANGE_DISPLAY.includes(d)) {
      d3.select(this).style("opacity", 0.5);
      SECTOR_RANGE_DISPLAY = SECTOR_RANGE_DISPLAY.filter((s) => s !== d);
    } else {
      d3.select(this).style("opacity", 1);
      SECTOR_RANGE_DISPLAY.push(d);
    }

    if (hexagonLayer) {
      hexagonLayer.setProps({
        data: d3.csv(filename).then(function (data) {
          return data.filter((d) => filterData(d));
        })
      });
    }
  });

// Display or hide panels
var legendDisplay = false;

document.getElementById("legend-control").onclick = (evt) => {
  if (legendDisplay) {
    document.getElementById("legend-display").style.display = "none";
    legendDisplay = false;
  } else {
    document.getElementById("legend-display").style.display = "block";
    legendDisplay = true;
  }
};

var backgroundDisplay = false;

document.getElementById("map-control").onclick = (evt) => {
  if (backgroundDisplay) {
    document.getElementById("map-display").style.display = "none";
    backgroundDisplay = false;
  } else {
    document.getElementById("map-display").style.display = "flex";
    backgroundDisplay = true;
  }
};

var infoDisplay = false;

document.getElementById("info-control").onclick = (evt) => {
  if (infoDisplay) {
    document.getElementById("info-display").style.display = "none";
    infoDisplay = false;
  } else {
    document.getElementById("info-display").style.display = "block";
    infoDisplay = true;
  }
};

document.getElementById("info-ok").onclick = (evt) => {
  document.getElementById("info-display").style.display = "none";
};

// Utility functions
function argmax(array) {
  return array.map((x, i) => [x, i]).reduce((r, a) => (a[0] > r[0] ? a : r))[1];
}

function argsort(array, reverse = false) {
  const arrayObject = array.map((value, idx) => {
    return { value, idx };
  });
  const rev = reverse ? -1 : 1;
  arrayObject.sort((a, b) => {
    if (a.value < b.value) {
      return rev * -1;
    }
    if (a.value > b.value) {
      return rev * 1;
    }
    return 0;
  });
  const argIndices = arrayObject.map((data) => data.idx);
  return argIndices;
}

function getWorkforceBySector(points) {
  var workforceBySector = [];
  for (var point of points) {
    // 1rt time there is no source attribute
    if (Object.keys(point).includes("source")) {
      point = point.source;
    }
    var indexSector = point.secteur;
    if (workforceBySector[indexSector] == null) {
      workforceBySector[indexSector] = +point.RH;
    } else {
      workforceBySector[indexSector] += +point.RH;
    }
  }
  return workforceBySector;
}

function getMode(points) {
  var workforceBySector = getWorkforceBySector(points);
  return argmax(workforceBySector);
}

// Create a popup
var popup = new mapboxgl.Popup({
  closeButton: false,
  closeOnClick: false,
  anchor: "top-left",
  className: "popup",
  maxWidth: "500px"
});

function onHover(info) {
  if (info.object) {
    var elevationValue = info.object.elevationValue;
    var workforceBySector = getWorkforceBySector(info.object.points);
    var order = argsort(workforceBySector, true);
    var html = "";

    //the 3 most represented companies
    for (
      var i = 0;
      //if order is smaller than 3
      i < Math.min(3, order.filter((x) => x !== undefined).length);
      i++
    ) {
      html +=
        "<b>" +
        (i + 1) +
        ". </b>" +
        SECTOR_RANGE[order[i]] +
        " : " +
        workforceBySector[order[i]] +
        " (" +
        Math.round((100 * workforceBySector[order[i]]) / elevationValue) +
        "%)" +
        "<br />";
    }

    //the rest of companies
    var workforceOther = order
      .map((x) => workforceBySector[x])
      .slice(3)
      .reduce((a, b) => a + b, 0);

    html +=
      "autres : " +
      workforceOther +
      " (" +
      Math.round((100 * workforceOther) / elevationValue) +
      "%)" +
      "<br />" +
      "<b>effectif total</b> : " +
      elevationValue +
      " (100%)";

    popup.setLngLat(info.coordinate).setHTML(html).addTo(map);
  } else {
    popup.remove();
  }
}

// Create the hexagon layer
var hexagonLayer;

var maxElevationDomain = 20000;
d3.csv(filename).then(function (data) {
  maxElevationDomain = d3.sum(data, function (d) {
    return +d.RH;
  });
});

hexagonLayer = new MapboxLayer({
  type: HexagonLayer,
  id: "heatmap",
  data: d3.csv(filename).then(function (data) {
    return data.filter((d) => filterData(d));
  }),
  radius: radiusByZoom(),
  coverage: 0.9,
  colorRange: COLOR_RANGE,
  colorDomain: [0, COLOR_RANGE.length - 1],
  elevationRange: [0, 500],
  // elevationDomain arbitrary
  elevationDomain: [0, maxElevationDomain],
  elevationScale: 250,
  extruded: true,
  getPosition: (d) => [+d.lng, +d.lat],
  getElevationWeight: (d) => +d.RH,
  elevationAggregation: "SUM",
  getColorValue: getMode,
  lightSettings: LIGHT_SETTINGS,
  opacity: 1,
  pickable: true,
  onHover: onHover
});

//init radius value for control panel
document.getElementById("radius").value = radiusByZoom();
document.getElementById("radius-value").value = radiusByZoom();

// Add the deck.gl Custom Layer to the map once the Mapbox map loads
map.on("style.load", () => {
  //add the deck.gl hex layer below labels in the Mapbox map
  map.addLayer(hexagonLayer);
});

function radiusByZoom() {
  const zoom = map.getZoom();
  //the law of variation is tuned manually
  var radius = Math.round((19 / zoom) ** 10);
  //radius must respect limits of the slider
  radius = Math.max(radius, 1);
  radius = Math.min(radius, document.getElementById("radius").max);
  return radius;
}

// Automatically update radius based on zoom
function render() {
  const check = document.getElementById("switch").checked;
  if (check) {
    const key = "radius";
    var radius = radiusByZoom();

    document.getElementById(key).value = radius;
    document.getElementById(key + "-value").value = radius;
    if (hexagonLayer) {
      hexagonLayer.setProps({
        [key]: radius
      });
    }
  }
}

map.on("zoomend", render);

document.getElementById("switch").onclick = (event) => {
  const check = document.getElementById("switch").checked;
  if (check) {
    document.getElementById("control-panel").style.display = "none";
  } else {
    document.getElementById("control-panel").style.display = "block";
  }
};

// Update sliders and inputs to change the layer's settings based on user input
OPTIONS.forEach((key) => {
  document.getElementById(key).onchange = (event) => {
    var value = Number(event.target.value);
    document.getElementById(key + "-value").value = value;
    if (key === "opacity") {
      value /= 100;
    }
    if (hexagonLayer) {
      hexagonLayer.setProps({
        [key]: value
      });
    }
  };

  document.getElementById(key + "-value").onchange = (event) => {
    var value = Number(event.target.value);
    document.getElementById(key).value = value;
    if (key === "opacity") {
      value /= 100;
    }
    if (hexagonLayer) {
      hexagonLayer.setProps({
        [key]: value
      });
    }
  };
});

// Filter on national investment
var key = "capitaux";

if (capitauxPresent) {
  document.getElementById(key).onchange = (event) => {
    valueCapitaux = Number(event.target.value);
    document.getElementById(key + "-value").value = valueCapitaux;
    if (hexagonLayer) {
      hexagonLayer.setProps({
        data: d3.csv(filename).then(function (data) {
          return data.filter((d) => filterData(d));
        })
      });
    }
  };

  document.getElementById(key + "-value").onchange = (event) => {
    valueCapitaux = Number(event.target.value);
    document.getElementById(key).value = valueCapitaux;
    if (hexagonLayer) {
      hexagonLayer.setProps({
        data: d3.csv(filename).then(function (data) {
          return data.filter((d) => filterData(d));
        })
      });
    }
  };
} else {
  document.getElementById(key + "-present").remove();
}

// Filter for elevation based on filter-slider

//max of elevation for a compagny
d3.csv(filename).then(function (data) {
  var max = d3.max(data, function (d) {
    return +d.RH;
  });

  $(function () {
    $("#filter").slider({
      range: true,
      min: 1,
      max: max,
      step: 1,
      values: [1, max],
      slide: function (event, ui) {
        //update number inputs linked to filter-slider when slide moves
        $("#value0").val(ui.values[0]);
        $("#value1").val(ui.values[1]);
      },
      change: function (event, ui) {
        [valueRH0, valueRH1] = ui.values;
        if (hexagonLayer) {
          hexagonLayer.setProps({
            data: d3.csv(filename).then(function (data) {
              return data.filter((d) => filterData(d));
            })
          });
        }
      }
    });

    //init number inputs
    $("#value0").val($("#filter").slider("values", 0));
    $("#value1").val($("#filter").slider("values", 1));
    document.getElementById("value1").max = max;
  });
});

//update filter-slider when number inputs change
[0, 1].forEach((i) => {
  document.getElementById("value" + i).onchange = (event) => {
    var value = Number(event.target.value);
    $("#filter").slider("values", i, value);
  };
});

// Update style for the background map depending on map input radio
var mapBackground;

document.getElementById("map-panel").onchange = (evt) => {
  mapBackground = document.querySelector("input[name=map]:checked");
  var style = mapBackground.value;
  switch (style) {
    case "dark":
      stylesheet = "mapbox://styles/mapbox/dark-v10?optimize=true";
      break;
    case "light":
      stylesheet = "mapbox://styles/mapbox/light-v10?optimize=true";
      break;
    case "outdoors":
      stylesheet = "mapbox://styles/mapbox/outdoors-v10?optimize=true";
      break;
    case "satellite":
      stylesheet = "mapbox://styles/mapbox/satellite-v9";
      break;
    default:
  }
  if (map) {
    map.setStyle(stylesheet);
  }
};
