<template>
  <div id="app">
    <div class="uk-margin">
      <div id="map"></div>
    </div>
    <div class="uk-margin uk-text-left" id="info">
      <div class="uk-margin">
        <button class="uk-button uk-button-default" v-on:click="switchMode">Enable/disable</button>
      </div>
      <input class="uk-input" id="inputBox" v-model="userInput" type="text" placeholder="Type country name here">
      <div class="uk-margin">
        <ul class="uk-list-circle"
            id="organisationsList" style="list-style-type: none">
          <li v-for="organisation in organisations" v-bind:key="organisation">
            {{ organisation }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import "ol/ol.css";
import Map from "ol/Map";
import View from "ol/View";
import GeoJSON from 'ol/format/GeoJSON';
import {Vector as VectorLayer} from 'ol/layer';
import {Vector as VectorSource} from 'ol/source';
import {Fill, Stroke, Style, Text} from 'ol/style';
import OLCesium from "olcs/OLCesium";
import * as Cesium from "cesium";

export default {
  data() {
    return {
      organisations: [],
      userInput: '',
      vectorLayer: new VectorLayer,
      map: new Map,
      map3d: undefined,
      featureOverlay: new VectorLayer,
      highlight: false,
      baseUrl: "http://localhost:8080/"
    }
  },
  watch: {
    userInput: async function () {
      let serverResponse = await fetch(this.baseUrl + "codes/" + this.userInput)
      let retrievedData = await serverResponse.json();
      const countryCode = retrievedData.country_code
      if (countryCode !== undefined) {
        this.showBorders(countryCode);

        serverResponse = await fetch(this.baseUrl + "organisations/" + this.userInput)
        retrievedData = await serverResponse.json();
        this.organisations = retrievedData.country_organisations
      }
    }
  },
  async mounted() {
    await this.initiateMap();
  },
  methods: {
    initiateMap() {
      let style = new Style({
        fill: new Fill({
          color: 'rgba(255, 255, 255, 0.6)'
        }),
        stroke: new Stroke({
          color: '#319FD3',
          width: 1
        }),
        text: new Text({
          font: '12px Calibri,sans-serif',
          fill: new Fill({
            color: '#000'
          }),
          stroke: new Stroke({
            color: '#fff',
            width: 3
          })
        })
      });

      this.vectorLayer = new VectorLayer({
        source: new VectorSource({
          url: 'https://openlayers.org/en/latest/examples/data/geojson/countries.geojson',
          format: new GeoJSON()
        }),
        style: function (feature) {
          style.getText().setText(feature.get('name'));
          return style;
        }
      });

      this.map = new Map({
        target: 'map',
        layers: [this.vectorLayer],
        view: new View({
          center: [0, 0],
          zoom: 1
        })
      });

      let highlightStyle = new Style({
        stroke: new Stroke({
          color: '#f00',
          width: 1
        }),
        fill: new Fill({
          color: 'rgba(255,0,0,0.1)'
        }),
        text: new Text({
          font: '12px Calibri,sans-serif',
          fill: new Fill({
            color: '#000'
          }),
          stroke: new Stroke({
            color: '#f00',
            width: 3
          })
        })
      });

      this.featureOverlay = new VectorLayer({
        source: new VectorSource(),
        style: function (feature) {
          highlightStyle.getText().setText(feature.get('name'));
          return highlightStyle;
        }
      });
      this.map.addLayer(this.featureOverlay);

      this.map3d = new OLCesium({
        map: this.map
      });
      const scene = this.map3d.getCesiumScene();
      scene.terrainProvider = Cesium.createWorldTerrain();
      this.map3d.setEnabled(false);
    },
    showBorders(countryCode) {
      let feature = this.vectorLayer.getSource().getFeatureById(countryCode);
      if (this.highlight) {
        this.featureOverlay.getSource().removeFeature(this.highlight);
      }
      if (feature) {
        this.featureOverlay.getSource().addFeature(feature);
      }
      this.highlight = feature;
    },
    switchMode() {
      this.map3d.setEnabled(!this.map3d.getEnabled());
    }
  }
};
</script>

<style lang="less">
@import "../node_modules/uikit/src/less/uikit.less";

#map {
  position: absolute;
  margin: 0;
  padding: 0;
  height: 500px;
  width: 99%;
}

#info {
  padding: 550px;
  width: 400px;
}

#organisationsList {
  margin: 10px;
  width: 400px;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>