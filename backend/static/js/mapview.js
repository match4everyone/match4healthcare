mapViewPage = {
    options: {
        mapViewContainerId: '',
        facilitiesURL : '',
        supportersURL : '',
        supporterListURL  : '',
        hospitalListURL   : '',
        mapboxToken: '',
        isStudent: true,
        isHospital: true,
        createPopupTextStudent  :  (countrycode,city, plz, count, url) => '',
        createPopupTextHospital :  (countrycode,city, plz, count, url) => '',
    },

    mapObject: null,

    initializeMap: function initializeMap() {
        let mapOptions = {
            center: [51.13, 10.018],
            zoom: 6
        }
    
        let tileLayerURL = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}@2x?access_token=' + this.options.mapboxToken
        let tileLayerOptions = {
            attribution: ' <a href="https://www.mapbox.com/about/maps/">© Mapbox</a> | <a href="http://www.openstreetmap.org/copyright">© OpenStreetMap</a> | <a href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a>',
            maxZoom: 18,
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1,
            preferCanvas: true,
          }
    
        this.mapObject = L.map(this.options.mapViewContainerId,mapOptions)
        L.tileLayer(tileLayerURL, tileLayerOptions).addTo(this.mapObject);    
    },

    onResizeWindow: function onResizeWindow() {
        let height = $(window).height()
        let navHeight = $('.navbar').outerHeight()
        let searchHeight = $('.search-map').innerHeight()
        let footerHeight = $('.footer').innerHeight()
        let isNavbarActive = document.getElementById('hospital_navbar') !== null
        let newHeight = height - navHeight - ( isNavbarActive ? searchHeight : 0 ) - footerHeight
        $(document.getElementById(mapViewPage.options.mapViewContainerId)).height(newHeight)
        mapViewPage.mapObject.invalidateSize()
    },

    registerEventHandlers : function registerEventHandlers(document, window) {
        $(window).on("resize", (event) => { this.onResizeWindow() }).trigger("resize")

    },

    loadMapMarkers : async function loadMapMarkers() {
        let [ facilities, supporters ] = await Promise.all([$.get(this.options.facilitiesURL),$.get(this.options.supportersURL)])
        
        let facilityMarkers = L.layerGroup(this.createMapMarkers(facilities,(lat,lon,countrycode,city,plz,count) => {
            return L.marker([lon,lat]).bindPopup(
                this.options.createPopupTextHospital(countrycode,city, plz, count, this.options.hospitalListURL.replace("COUNTRYCODE",countrycode).replace("PLZ",plz))
            )
        }))

        let supporterMarkers = L.layerGroup(this.createMapMarkers(supporters,(lat,lon,countrycode,city,plz,count) => {
            return L.circle([lon,lat], { 
                radius: count > 30 ? ( 2000 + 50 * count ) : ( 500 + 100 * count ),
                color: '#ed0a71', 
                fillColor: '#ed0a71', 
                weight: 2 + 0.25 * count, 
                fillOpacity: .2 
            }).bindPopup(this.options.createPopupTextStudent(countrycode,city, plz, count, this.options.supporterListURL.replace("COUNTRYCODE",countrycode).replace("PLZ",plz)))
        }))
        
        var overlays = {
            "Einrichtungen" : facilityMarkers,
            "Helfer*innen"  : supporterMarkers
        }

        facilityMarkers.addTo(this.mapObject)
        supporterMarkers.addTo(this.mapObject)

        L.control.layers(null, overlays, { collapsed: false, position: 'topleft' }).addTo(this.mapObject)
    },

    showUserCount: async function showUserCount() {
        var count = await $.getJSON("/accounts/count")
        document.getElementById("user_count").textContent = count.user_count
        document.getElementById("facility_count").textContent = count.facility_count
    },

    createMapMarkers : function addMapMarkers(markers, createMarkerFunction) {
        let markerArray = []
        
        for (countryCode in markers) {
            for (zipCodeKey in markers[countryCode]) {
                let zipCode = markers[countryCode][zipCodeKey]
                markerArray.push(createMarkerFunction(zipCode.latitude, zipCode.longitude, countryCode, zipCode.city, zipCode.plz, zipCode.count))
            }
        }

        return markerArray
    }



}
$.extend(mapViewPage.options, pageOptions)

document.addEventListener("DOMContentLoaded", function domReady() {

    mapViewPage.initializeMap()
    mapViewPage.loadMapMarkers()
    mapViewPage.showUserCount()
    mapViewPage.registerEventHandlers(document, window)

})
