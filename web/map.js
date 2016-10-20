    var BingLayer = L.TileLayer.extend({
    getTileUrl: function (tilePoint) {
        this._adjustTilePoint(tilePoint);
        return L.Util.template(this._url, {
            s: this._getSubdomain(tilePoint),
            q: this._quadKey(tilePoint.x, tilePoint.y, this._getZoomForUrl())
        });
    },
    _quadKey: function (x, y, z) {
        var quadKey = [];
        for (var i = z; i > 0; i--) {
            var digit = '0';
            var mask = 1 << (i - 1);
            if ((x & mask) != 0) {
                digit++;
            }
            if ((y & mask) != 0) {
                digit++;
                digit++;
            }
            quadKey.push(digit);
        }
        return quadKey.join('');
        }
    });

    var Bing = new BingLayer('http://t{s}.tiles.virtualearth.net/tiles/a{q}.jpeg?g=1398', {
        subdomains: ['0', '1', '2', '3', '4'],
        attribution: '&copy; <a href="http://bing.com/maps">Bing Maps</a>'
    });

    var Google = new L.Google();

    var map = new L.Map(document.querySelector('#map'), {
        layers: [Bing],
        center: new L.LatLng(50.97715591108954, 100.50481796264648),
        zoom: 3
    });

    var baseMaps = {
        "Google": Google,
        "Bing": Bing
    };
    //var overlayMaps = null;
    //var layercontrol = L.control.layers(baseMaps, overlayMaps);
    //layercontrol.collapsed = false;
    //layercontrol.addTo(map);

    var areaSelect = L.areaSelect({width:480, height:320});
    areaSelect.addTo(map);

    function getBboxArray() {
        var bbox = areaSelect.getBounds();
        return [
            bbox._southWest.lat,
            bbox._southWest.lng,
            bbox._northEast.lat,
            bbox._northEast.lng
          ];
    }

    function changeLayer(layer) {
        for (var fry in baseMaps) {
            if (baseMaps.hasOwnProperty(fry)) {
                if (map.hasLayer(baseMaps[fry])) {
                    map.removeLayer(baseMaps[fry])
                }
            }
        }
        map.addLayer(baseMaps[layer]);
    }