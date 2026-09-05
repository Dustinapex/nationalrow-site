# -*- coding: utf-8 -*-
"""Interactive approved-route map + address proximity check.

Route geometry is fetched at page load from Oncor's own public ArcGIS feature
service — the same service that powers Oncor's landowner map viewer — so the
map stays current as Oncor updates it. If the service is unreachable the map
degrades to a clear message plus links to Oncor's official viewer.

Address lookup uses the U.S. Census Bureau geocoder (free, no API key, JSONP).
"""

MAP_HEAD = """<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>"""


def map_section(project_ids, title, blurb, oncor_viewer_url, constraints_pdf_url, default_center, default_zoom):
    """project_ids: list of Oncor ArcGIS project_id ints for this page."""
    ids = ",".join(str(p) for p in project_ids)
    return """
<section class="section-alt" id="map">
  <div class="container">
    <h2>%s</h2>
    <p class="section-sub">%s</p>

    <div class="map-wrap">
      <div class="map-bar">
        <input id="addrInput" type="text" placeholder="Enter your property address, or the nearest crossroads" autocomplete="off">
        <button id="addrBtn" type="button">Check my location</button>
      </div>
      <div id="routeMap"></div>
      <div class="map-legend">
        <span><i class="swatch" style="background:#c9a227"></i> PUCT-approved route</span>
        <span><i class="swatch" style="background:#94a3b8"></i> Other routes studied (not approved)</span>
        <span><i class="swatch" style="background:#b91c1c;height:10px;width:10px;border-radius:50%%"></i> Your location</span>
      </div>
      <div class="map-result" id="mapResult"></div>
      <div class="map-note">
        Route data is loaded live from Oncor's public project mapping service, the same data behind Oncor's own landowner map viewer. The line shown is the approved <em>centerline</em>; the easement is a corridor roughly 200 feet wide centered on it, and the final surveyed alignment can shift within the approved corridor. <strong>This tool is an approximation, not a survey and not legal advice.</strong> Distances are straight-line estimates. Addresses you type are sent to the U.S. Census Bureau's public geocoder to find coordinates. If we find a match, we drop the address and county into the review form lower down so you do not have to retype them — nothing reaches National ROW unless you actually submit that form. Confirm your status against
        <a href="%s" target="_blank" rel="noopener">Oncor's official interactive map</a> and the
        <a href="%s" target="_blank" rel="noopener">filed constraints map</a>.
      </div>
    </div>
  </div>
</section>

<script>
(function(){
  var SVC='https://services6.arcgis.com/4U8AckBJXzVfzxBF/arcgis/rest/services/CCN_Data_AGOL/FeatureServer/2/query';
  var PIDS='%s';
  var map, approvedLayer=null, marker=null, approvedCoords=[];

  function initMap(){
    map = L.map('routeMap', {scrollWheelZoom:false}).setView(%s, %d);
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',{
      maxZoom:19,
      attribution:'Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ, USGS | Route data: Oncor Electric Delivery (public CCN viewer)'
    }).addTo(map);
    map.on('click', function(){ map.scrollWheelZoom.enable(); });
    loadRoutes();
  }

  function q(where, cb){
    var url = SVC + '?f=geojson&outSR=4326&resultRecordCount=2000&maxAllowableOffset=0.0004'
            + '&outFields=link_id,Status,project_id&where=' + encodeURIComponent(where);
    fetch(url).then(function(r){ return r.json(); }).then(cb).catch(function(){ cb(null); });
  }

  function loadRoutes(){
    // Other studied routes first, so the approved route draws on top.
    q("project_id IN (" + PIDS + ") AND Status<>'Approved'", function(g){
      if(g && g.features && g.features.length){
        L.geoJSON(g, {style:{color:'#94a3b8', weight:2, opacity:.65, dashArray:'4,5'}}).addTo(map);
      }
    });
    q("project_id IN (" + PIDS + ") AND Status='Approved'", function(g){
      if(!g || !g.features || !g.features.length){
        document.getElementById('routeMap').insertAdjacentHTML('beforeend',
          '<div style="position:absolute;inset:0;z-index:500;display:flex;align-items:center;justify-content:center;background:rgba(255,255,255,.94);padding:24px;text-align:center;font-size:15px;line-height:1.7;color:#334155">'
          + "The live route map couldn't load right now. View the approved route on <a href='%s' target='_blank' rel='noopener' style='color:#1d4ed8;text-decoration:underline'>Oncor's official map viewer</a>."
          + '</div>');
        return;
      }
      approvedLayer = L.geoJSON(g, {style:{color:'#c9a227', weight:5, opacity:.95}}).addTo(map);
      g.features.forEach(function(f){
        var c = f.geometry && f.geometry.coordinates;
        if(!c) return;
        if(typeof c[0][0] === 'number'){ approvedCoords.push(c); }
        else { c.forEach(function(part){ approvedCoords.push(part); }); }
      });
      try{ map.fitBounds(approvedLayer.getBounds(), {padding:[24,24]}); }catch(e){}
    });
  }

  // ---- geometry helpers (equirectangular, fine at these distances) ----
  function projPt(lon, lat, lat0){
    var R=6371000, r=Math.PI/180;
    return [R*lon*r*Math.cos(lat0*r), R*lat*r];
  }
  function segDist(p, a, b){
    var dx=b[0]-a[0], dy=b[1]-a[1];
    var L2=dx*dx+dy*dy;
    var t = L2 ? ((p[0]-a[0])*dx + (p[1]-a[1])*dy)/L2 : 0;
    t = Math.max(0, Math.min(1, t));
    var cx=a[0]+t*dx, cy=a[1]+t*dy;
    return Math.hypot(p[0]-cx, p[1]-cy);
  }
  function distanceToRouteMeters(lat, lon){
    if(!approvedCoords.length) return null;
    var best = Infinity, p = projPt(lon, lat, lat);
    for(var i=0;i<approvedCoords.length;i++){
      var line = approvedCoords[i];
      for(var j=1;j<line.length;j++){
        var a = projPt(line[j-1][0], line[j-1][1], lat);
        var b = projPt(line[j][0], line[j][1], lat);
        var d = segDist(p, a, b);
        if(d < best) best = d;
      }
    }
    return best;
  }

  // ---- address lookup via Census geocoder (JSONP) ----
  // 'geographies' rather than 'locations' so we get the county back too — it fills
  // the form's county field and tells us which docket the owner belongs to.
  function geocode(addr, cb){
    var cbName = 'nrGeo' + Date.now();
    var s = document.createElement('script');
    var to = setTimeout(function(){ cleanup(); cb(null); }, 12000);
    function cleanup(){ clearTimeout(to); try{ delete window[cbName]; }catch(e){ window[cbName]=undefined; } if(s.parentNode) s.parentNode.removeChild(s); }
    window[cbName] = function(data){ cleanup(); cb(data); };
    s.src = 'https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress?address='
          + encodeURIComponent(addr)
          + '&benchmark=Public_AR_Current&vintage=Current_Current&layers=Counties'
          + '&format=jsonp&callback=' + cbName;
    s.onerror = function(){ cleanup(); cb(null); };
    document.body.appendChild(s);
  }

  // ---- carry what we learned into the lead form ----
  function set(id, val){
    var el = document.getElementById(id);
    if(!el || !val) return;
    if(!el.__nrWired){
      el.__nrWired = true;
      el.addEventListener('input', function(){ el.dataset.nrAuto = ''; });
    }
    // Fill when empty, or overwrite a value we put there ourselves on an earlier check.
    if(!el.value || el.dataset.nrAuto === '1'){
      el.value = val;
      el.dataset.nrAuto = '1';
    }
  }
  function setHidden(name, val){
    var f = document.getElementById('leadForm');
    if(!f) return;
    var el = f.querySelector('[name="' + name + '"]');
    if(!el){
      el = document.createElement('input');
      el.type = 'hidden'; el.name = name;
      f.appendChild(el);
    }
    el.value = val;
  }
  function carryToForm(match, lat, lon, miles){
    var county = '';
    try{
      var c = match.geographies && match.geographies.Counties && match.geographies.Counties[0];
      if(c && c.BASENAME) county = c.BASENAME + ', TX';
    }catch(e){}
    set('propAddress', match.matchedAddress || '');
    set('countyState', county);
    setHidden('checked_address', match.matchedAddress || '');
    setHidden('checked_county', county);
    setHidden('route_distance_miles', miles.toFixed(2));
    setHidden('property_latlon', lat.toFixed(6) + ',' + lon.toFixed(6));
    setHidden('checked_project', PIDS === '1015' ? 'Dinosaur-Longshore (Docket 59315)'
                              : PIDS === '1019' ? 'Longshore-Drill Hole (Docket 59029)'
                              : 'Texas 765kV corridor');
  }

  function show(cls, html){
    var el = document.getElementById('mapResult');
    el.className = 'map-result ' + cls;
    el.innerHTML = html;
    el.style.display = 'block';
  }

  function run(){
    var addr = document.getElementById('addrInput').value.trim();
    if(!addr){ return; }
    if(!approvedCoords.length){
      show('err','<strong>Route data is still loading.</strong>Give it a moment and try again, or call or text us at (469) 484-7960 and we will check it for you.');
      return;
    }
    var btn = document.getElementById('addrBtn');
    btn.disabled = true; btn.textContent = 'Checking…';
    geocode(addr, function(data){
      btn.disabled = false; btn.textContent = 'Check my location';
      var m = data && data.result && data.result.addressMatches && data.result.addressMatches[0];
      if(!m){
        show('err','<strong>We could not place that address.</strong>Rural addresses often are not in the public geocoder. Try the nearest crossroads or town, or just <a href="#contact" style="color:inherit;text-decoration:underline">send us your parcel number</a> and we will look it up by hand.');
        return;
      }
      var lat = m.coordinates.y, lon = m.coordinates.x;
      if(marker) map.removeLayer(marker);
      marker = L.circleMarker([lat,lon], {radius:8, color:'#fff', weight:2, fillColor:'#b91c1c', fillOpacity:1}).addTo(map);
      map.setView([lat,lon], 11);
      var d = distanceToRouteMeters(lat, lon);
      var mi = d/1609.34;
      var pretty = mi < 0.5 ? (Math.round(d*3.28084/10)*10).toLocaleString() + ' feet' : mi.toFixed(1) + ' miles';
      carryToForm(m, lat, lon, mi);
      if(window.gtag) gtag('event','route_proximity_check',{distance_miles: Math.round(mi*10)/10});
      if(mi < 0.5){
        show('near','<strong>That location is about ' + pretty + ' from the approved centerline.</strong>'
          + 'Property this close is very likely inside or adjacent to the 200-foot easement corridor. If you have not been contacted yet, you probably will be. Do not sign a survey permission form or an easement before someone independent reviews it. <a href="#contact" style="color:inherit;text-decoration:underline"><strong>Get a free review →</strong></a> — we have already filled your address and county into the form.');
      } else if(mi < 3){
        show('near','<strong>That location is about ' + pretty + ' from the approved centerline.</strong>'
          + 'You are close to the corridor but likely outside the easement itself. The final alignment can still shift, and nearby lines can affect value. Worth a free look. <a href="#contact" style="color:inherit;text-decoration:underline"><strong>Have us check it →</strong></a> — your address and county are already filled in below.');
      } else {
        show('far','<strong>That location is about ' + pretty + ' from the approved centerline.</strong>'
          + 'It is probably not on this route. Oncor has several other 765 kV and 345 kV projects moving through the same region — if you received a letter, <a href="#contact" style="color:inherit;text-decoration:underline">tell us what it says</a> and we will identify which project it belongs to.');
      }
    });
  }

  function boot(){
    if(typeof L === 'undefined'){
      document.getElementById('routeMap').innerHTML =
        "<div style='padding:28px;text-align:center;font-size:15px;line-height:1.7;color:#334155'>The map could not load. View the approved route on <a href='%s' target='_blank' rel='noopener' style='color:#1d4ed8;text-decoration:underline'>Oncor's official map viewer</a>.</div>";
      return;
    }
    initMap();
    document.getElementById('addrBtn').addEventListener('click', run);
    document.getElementById('addrInput').addEventListener('keydown', function(e){ if(e.key === 'Enter'){ e.preventDefault(); run(); } });
  }

  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
</script>
""" % (title, blurb, oncor_viewer_url, constraints_pdf_url, ids,
       default_center, default_zoom, oncor_viewer_url, oncor_viewer_url)


def map_compact(project_ids, title, blurb, oncor_viewer_url, detail_url, detail_label):
    """Compact, non-qualifying route map for PAID-TRAFFIC LANDING PAGES.

    Deliberately has NO address checker. On a paid landing page a checker can
    tell a visitor they are not affected and kill a lead we already paid for -
    and the filed corridor is not the final surveyed alignment anyway, so a
    'no match' answer would not even be reliable. Here the map is proof that
    we know the project, not a qualifier. It auto-fits to the approved route
    so it reads at a glance on a phone.
    """
    ids = ",".join(str(p) for p in project_ids)
    return """
<section class="lp-map" id="route">
  <div class="container">
    <h2>%s</h2>
    <p class="lp-map-sub">%s</p>
    <div class="map-wrap">
      <div id="routeMapC"></div>
      <div class="map-legend">
        <span><i class="swatch" style="background:#c9a227"></i> Approved route</span>
        <span><i class="swatch" style="background:#94a3b8"></i> Studied, not selected</span>
      </div>
      <div class="map-note">
        Loaded live from Oncor&rsquo;s public project mapping service. The gold line is the approved
        <em>centerline</em>; the easement is a corridor roughly 200 feet wide centered on it, and the final
        surveyed alignment can still shift within the approved corridor. <strong>Not a survey and not legal
        advice.</strong> Confirm against <a href="%s" target="_blank" rel="noopener">Oncor&rsquo;s official map viewer</a>.
      </div>
    </div>
    <p class="lp-map-more"><a href="%s">%s</a></p>
  </div>
</section>

<script>
(function(){
  var SVC='https://services6.arcgis.com/4U8AckBJXzVfzxBF/arcgis/rest/services/CCN_Data_AGOL/FeatureServer/2/query';
  var PIDS='%s';
  var map;

  function q(where, cb){
    var url = SVC + '?f=geojson&outSR=4326&resultRecordCount=2000&maxAllowableOffset=0.0004'
            + '&outFields=link_id,Status,project_id&where=' + encodeURIComponent(where);
    fetch(url).then(function(r){ return r.json(); }).then(cb).catch(function(){ cb(null); });
  }

  function fail(){
    var el = document.getElementById('routeMapC');
    if(!el) return;
    el.insertAdjacentHTML('beforeend',
      '<div style="position:absolute;inset:0;z-index:500;display:flex;align-items:center;justify-content:center;'
      + 'background:rgba(255,255,255,.94);padding:20px;text-align:center;font-size:14px;line-height:1.7;color:#334155">'
      + "Route map couldn't load. View it on <a href='%s' target='_blank' rel='noopener' style='color:#1d4ed8;text-decoration:underline'>Oncor's official map viewer</a>."
      + '</div>');
  }

  function init(){
    // Touch devices: dragging off so the map never traps the page scroll.
    map = L.map('routeMapC', {
      scrollWheelZoom:false,
      dragging: !L.Browser.mobile,
      tap: false,
      zoomControl: true
    }).setView([31.6,-100.4], 6);
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}',{
      maxZoom:19,
      attribution:'Tiles &copy; Esri | Route data: Oncor Electric Delivery (public CCN viewer)'
    }).addTo(map);

    q("project_id IN (" + PIDS + ") AND Status<>'Approved'", function(g){
      if(g && g.features && g.features.length){
        L.geoJSON(g, {style:{color:'#94a3b8', weight:2, opacity:.6, dashArray:'4,5'}}).addTo(map);
      }
    });
    q("project_id IN (" + PIDS + ") AND Status='Approved'", function(g){
      if(!g || !g.features || !g.features.length){ fail(); return; }
      var layer = L.geoJSON(g, {style:{color:'#c9a227', weight:5, opacity:.95}}).addTo(map);
      try{
        map.fitBounds(layer.getBounds(), {padding:[18,18]});
      }catch(e){}
      setTimeout(function(){ map.invalidateSize(); }, 200);
    });
  }

  if(document.readyState === 'loading'){ document.addEventListener('DOMContentLoaded', init); }
  else { init(); }
})();
</script>
""" % (title, blurb, oncor_viewer_url, detail_url, detail_label, ids, oncor_viewer_url)
