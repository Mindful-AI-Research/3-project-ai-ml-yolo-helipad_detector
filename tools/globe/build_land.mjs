// npm i world-atlas@2 topojson-client@3 d3-geo@3  &&  node build_land.mjs
import fs from 'fs';
import {feature} from 'topojson-client';
import {geoContains} from 'd3-geo';
const topo = JSON.parse(fs.readFileSync('node_modules/world-atlas/land-110m.json','utf8'));
const land = feature(topo, topo.objects.land);
const STEP = 1.6;                       // graus de latitude (~178 km)
const pts = [];
for (let lat = -58; lat <= 84; lat += STEP) {          // sem Antártida
  const c = Math.max(Math.cos(lat*Math.PI/180), 0.2);
  const dlon = STEP / c;                                 // espaçamento ~igual em área
  for (let lon = -180; lon < 180; lon += dlon) {
    if (geoContains(land, [lon, lat])) pts.push([Math.round(lat*10), Math.round(lon*10)]);
  }
}
fs.writeFileSync('land_real.json', JSON.stringify(pts.flat()));
// checagem: SP e arredores
const near = pts.filter(([a,b]) => Math.abs(a/10+23.55)<2.6 && Math.abs(b/10+46.63)<2.6);
console.log('pontos:', pts.length, '| bytes:', JSON.stringify(pts.flat()).length, '| perto de SP:', near.length);
console.log('SP contido em terra?', geoContains(land, [-46.6333, -23.5505]));
