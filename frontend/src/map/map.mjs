import $ from 'jquery'
import L from 'leaflet'
import 'leaflet.markercluster'
import 'leaflet.featuregroup.subgroup'
import 'leaflet/dist/leaflet.css'
import 'leaflet.markercluster/dist/MarkerCluster.css'
import 'leaflet.markercluster/dist/MarkerCluster.Default.css'
import '../css/map.css'

export class MapViewPage {

    constructor(options) {
        let defaultOptions = {
            mapViewContainerId: '',
            facilitiesURL : '',
            supportersURL : '',
            supporterListURL  : '',
            hospitalListURL   : '',
            mapboxToken: '',
            isStudent: true,
            isHospital: true,
            // eslint-disable-next-line no-unused-vars
            createPopupTextStudent  :  (countrycode,city, plz, count, url) => '',

            // eslint-disable-next-line no-unused-vars
            createPopupTextHospital :  (countrycode,city, plz, count, url) => '',

            // eslint-disable-next-line no-unused-vars
            createFacilitiesCountText: (count) => '',

            // eslint-disable-next-line no-unused-vars
            createSupportersCountText: (count) => '',
            facilityIcon: new L.Icon.Default(),
        }

        Object.assign(defaultOptions,options)
        this.options = defaultOptions
        this.mapObject = null
    }

    createFacilityIcon(count) {
        return L.divIcon({
            className: 'leaflet-marker-icon marker-cluster marker-cluster-single leaflet-zoom-animated leaflet-interactive facilityMarker',
            html: `<div><span>${count}</span></div>`,
            iconSize: [40, 40],
            popupAnchor: [-10,-10],
        })
    }

    createSupporterIcon(count) {
        return L.divIcon({
            className: 'leaflet-marker-icon marker-cluster marker-cluster-single leaflet-zoom-animated leaflet-interactive supporterMarker',
            html: `<div><span>${count}</span></div>`,
            iconSize: [40, 40],
        })
    }

    cssClassedIconCreateFunction(cssClass) {
        return (function (cluster) {
            let childCount = cluster.getChildCount()
            let cssClasses = ['marker-cluster']
            let c = ' marker-cluster-'
            if (childCount < 10) {
                c += 'small'
            } else if (childCount < 100) {
                c += 'medium'
            } else {
                c += 'large'
            }
            cssClasses.push(c)
            cssClasses.push(cssClass)
            return new L.DivIcon({
                html: '<div><span>' + childCount + '</span></div>',
                className: cssClasses.join(' '),
                iconSize: new L.Point(40, 40)
            })
        })
    }

    initializeMap() {
        let mapOptions = {
            center: [51.13, 10.018],
            zoom: 6
        }

        let tileLayerURL = 'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}@2x?access_token=' + this.options.mapboxToken
        let tileLayerOptions = {
            attribution: ' <a href="https://www.mapbox.com/about/maps/">© Mapbox</a> | <a href="http://www.openstreetmap.org/copyright">© OpenStreetMap</a> | <a href="https://www.mapbox.com/map-feedback/" target="_blank">Improve this map</a> | Icons by <a href="https://www.flaticon.com/authors/freepik" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">flaticon.com</a>',
            maxZoom: 18,
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1,
            preferCanvas: true,
        }

        this.mapObject = L.map(this.options.mapViewContainerId,mapOptions)
        L.tileLayer(tileLayerURL, tileLayerOptions).addTo(this.mapObject)

        // Enhance MarkerCluster - override getChildCount
        L.MarkerCluster.prototype.getChildCount = function (){
            const children = this.getAllChildMarkers()
            return children.reduce((sum,marker) => (sum + marker.options.itemCount),0)
        }

    }

    onResizeWindow() {
        let height = $(window).height()
        let navHeight = $('.navbar').outerHeight()
        let searchHeight = $('.search-map').innerHeight()
        let footerHeight = $('.footer').innerHeight()
        let isSearchBarActive = document.getElementById('hospital_navbar') !== null
        let newHeight = height - navHeight - ( isSearchBarActive ? searchHeight : 0 ) - footerHeight
        $(document.getElementById(this.options.mapViewContainerId)).height(newHeight)
        this.mapObject.invalidateSize()
    }

    registerEventHandlers(window) {
        $(window).on('resize', () => { this.onResizeWindow() }).trigger('resize')
    }

    async loadMapMarkers() {
        let [ facilities, supporters ] = await Promise.all([$.get(this.options.facilitiesURL),$.get(this.options.supportersURL)])

        let facilityClusterMarkerGroup = L.markerClusterGroup({
            iconCreateFunction: this.cssClassedIconCreateFunction('facilityMarker'),
        })
        let facilityMarkers = L.featureGroup.subGroup(facilityClusterMarkerGroup, this.createMapMarkers(facilities,(lat,lon,countrycode,city,plz,count) => {
            return L.marker([lon,lat],{
                icon:  this.createFacilityIcon(count),
                itemCount: count,
            }).bindPopup(this.options.createPopupTextHospital(countrycode,city, plz, count, this.options.hospitalListURL.replace('COUNTRYCODE',countrycode).replace('PLZ',plz)))
        }))

        let supporterClusterMarkerGroup = L.markerClusterGroup({
            iconCreateFunction: this.cssClassedIconCreateFunction('supporterMarker'),
        })
        let supporterMarkers = L.featureGroup.subGroup(supporterClusterMarkerGroup, this.createMapMarkers(supporters,(lat,lon,countrycode,city,plz,count) => {
            return L.marker([lon,lat],{
                icon:  this.createSupporterIcon(count),
                itemCount: count,
            }).bindPopup(this.options.createPopupTextStudent(countrycode,city, plz, count, this.options.supporterListURL.replace('COUNTRYCODE',countrycode).replace('PLZ',plz)))
        }))

        supporterClusterMarkerGroup.addTo(this.mapObject)
        supporterMarkers.addTo(this.mapObject)
        facilityClusterMarkerGroup.addTo(this.mapObject)
        facilityMarkers.addTo(this.mapObject)

        const countItems = (o) => {
            let count = 0
            for (let countryCode in o) {
                for (let zipCode in o[countryCode]) {
                    count += o[countryCode][zipCode].count
                }
            }
            return count
        }

        let overlays = {}
        overlays[this.options.createFacilitiesCountText(countItems(facilities))] = facilityMarkers
        overlays[this.options.createSupportersCountText(countItems(supporters))] = supporterMarkers

        facilityMarkers.addTo(this.mapObject)

        L.control.layers(null, overlays, { collapsed: false, position: 'topright' }).addTo(this.mapObject)
    }

    createMapMarkers(markers, createMarkerFunction) {
        let markerArray = []

        for (let countryCode in markers) {
            for (let zipCodeKey in markers[countryCode]) {
                let zipCode = markers[countryCode][zipCodeKey]
                markerArray.push(createMarkerFunction(zipCode.latitude, zipCode.longitude, countryCode, zipCode.city, zipCode.plz, zipCode.count))
            }
        }

        return markerArray
    }

}
