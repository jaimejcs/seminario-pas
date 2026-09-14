const $ = s => document.querySelector(s);
const api = new URLSearchParams(location.search).get('api') || `${location.protocol}//${location.hostname}:8000`;
const colors = ['#409c7c','#d4ad48','#e98f4c','#de6571'];
const weatherNames = {clear:'Céu aberto',light_rain:'Chuva leve',heavy_rain:'Chuva forte'};
const architectures = {
 blackboard:{name:'Blackboard',description:'Especialistas independentes publicam fatos no quadro compartilhado. A decisão reúne as contribuições, preservando sua autoria.',nodes:['Sensores','Quadro ⇄ Especialistas','Decisão','Recomendação']},
 mvc:{name:'MVC',description:'O Controller coordena a interação, o Model calcula o trânsito e a View apresenta o resultado. Cards e tabela compartilham o mesmo Model.',nodes:['View','Controller','Model','Controller','View']},
 multitiers:{name:'Multitiers',description:'A apresentação consome a API por HTTP. Serviços executam as regras de negócio e um repositório isolado persiste os sensores no SQLite.',nodes:['Frontend','HTTP / API','Business Tier','Repository / SQLite']}
};
let roads = [], initial = [], selected = 1, architecture = 'blackboard', response = null, tableMode = false, reading = 0, busy = false, toastTimer;
function escapeHtml(value){return String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function toast(message){$('#toast').textContent=message;$('#toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').hidden=true,3200);}
async function request(path, body){const res=await fetch(api+path,{...(body?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}:{}),signal:AbortSignal.timeout(10000)});const data=await res.json();if(!res.ok)throw Error(data.error || 'Falha na API');return data;}
function errorMessage(error){$('#error').textContent=`Não foi possível consultar a API. Verifique se “python3 server.py” está em execução na porta 8000. ${error.message}`;$('#error').hidden=false;$('#connection').textContent='API indisponível';$('#connection-dot').style.background=colors[3];}
function lock(value){busy=value;document.querySelectorAll('button, form input, form select, #road-select').forEach(el=>el.disabled=value);}
async function analyze(nextRoads=roads,nextArch=architecture,message=''){
 if(busy)return;lock(true);
 try{const data=await request('/api/analyze',{architecture:nextArch,roads:nextRoads});roads=structuredClone(nextRoads);architecture=nextArch;response=data;$('#error').hidden=true;$('#connection').textContent='API conectada';$('#connection-dot').style.background=colors[0];render();if(message)toast(message);}
 catch(error){errorMessage(error);}finally{lock(false);}
}
function badge(r){return `<span class="status" style="--road-color:${colors[r.level]}">${r.congestion}</span>`;}
function render(){
 const analyzed=response.roads;
 document.querySelectorAll('[data-arch]').forEach(el=>{const active=el.dataset.arch===architecture;el.classList.toggle('selected',active);el.setAttribute('aria-selected',active);});
 const critical=analyzed.filter(r=>r.level===3).length, speed=Math.round(analyzed.reduce((sum,r)=>sum+r.average_speed,0)/4), volume=analyzed.reduce((sum,r)=>sum+r.vehicles_per_minute,0);
 $('#metrics').innerHTML=[['Vias monitoradas','04','vias','Todas as leituras disponíveis','⌘'],['Velocidade média',speed,'km/h','Média simples das quatro vias','↗'],['Fluxo total',volume,'veíc/min','Soma do volume monitorado','≋'],['Vias em estado crítico',String(critical).padStart(2,'0'),'vias',critical?'<span class="red-text">Atenção do operador recomendada</span>':'Nenhuma via em estado crítico','△']].map(([label,value,unit,foot,icon])=>`<div class="metric"><div class="metric-top"><span>${label}</span><span>${icon}</span></div><div class="metric-value">${value} <small>${unit}</small></div><div class="metric-foot">${foot}</div></div>`).join('');
 $('#reading').textContent=reading?`Leitura ${String(reading).padStart(2,'0')}`:'Leitura inicial';
 $('#roads').classList.toggle('table-mode',tableMode);
 $('#roads').innerHTML=tableMode?`<table><thead><tr><th>Via</th><th>Estado</th><th>km/h</th><th>Veíc/min</th><th>Clima</th><th>Verde</th><th>Ação</th></tr></thead><tbody>${analyzed.map(r=>`<tr><td><button class="button" data-road="${r.id}">${r.road}</button></td><td>${badge(r)}</td><td>${r.average_speed}</td><td>${r.vehicles_per_minute}</td><td>${weatherNames[r.weather]}</td><td>${r.traffic_light_green_time} s</td><td>${r.recommendation}</td></tr>`).join('')}</tbody></table>`:analyzed.map(r=>`<article class="road-card ${r.id===selected?'selected':''}" style="--road-color:${colors[r.level]}" data-road="${r.id}" tabindex="0" role="button" aria-label="Inspecionar ${r.road}"><div class="road-top"><h3>${r.road}</h3>${badge(r)}</div><div class="road-values"><div><b>${r.average_speed}</b><small>km/h</small><label>Velocidade média</label></div><div><b>${r.vehicles_per_minute}</b><small>veíc/min</small><label>Volume de veículos</label></div></div><div class="road-meta"><span>☁ ${weatherNames[r.weather]}</span><span>${r.accident?'△ Acidente':'✓ Sem incidente'}</span><span>◉ Verde: ${r.traffic_light_green_time} s</span>${r.event?'<span>⚑ Evento esportivo</span>':''}</div><div class="recommendation"><strong>↳ Ação recomendada</strong><br>${r.recommendation}</div></article>`).join('');
 analyzed.forEach(r=>{$(`#route-${r.id}`).setAttribute('stroke',colors[r.level]);});
 const positions=[[310,104],[125,61],[406,183],[610,263]];
 $('#map-labels').innerHTML=analyzed.map((r,i)=>{const [x,y]=positions[i];return `<g data-road="${r.id}" tabindex="0" role="button" aria-label="Selecionar ${r.road}" style="cursor:pointer"><rect x="${x}" y="${y-15}" width="112" height="28" rx="5" fill="white" stroke="${r.id===selected?'#a998df':'#e0e6e1'}"/><circle cx="${x+12}" cy="${y-1}" r="3" fill="${colors[r.level]}"/><text x="${x+23}" y="${y+3}" fill="#66746d" font-size="10">${r.road}</text></g>`;}).join('');
 $('#road-select').innerHTML=roads.map(r=>`<option value="${r.id}" ${r.id===selected?'selected':''}>${r.road}</option>`).join('');
 renderInspector();
}
function renderInspector(){
 const r=roads.find(r=>r.id===selected);if(!r)return;
 $('#speed').value=r.average_speed;$('#volume').value=r.vehicles_per_minute;$('#weather').value=r.weather;$('#green').value=r.traffic_light_green_time;$('#accident').checked=r.accident;$('#event').checked=!!r.event;updateOutputs();
 const a=architectures[architecture];$('#flow-title').textContent=a.name;$('#architecture-description').textContent=a.description;$('#duration').textContent=`${response.duration_ms.toLocaleString('pt-BR')} ms · servidor`;$('#diagram').innerHTML=a.nodes.map((node,i)=>`${i?'<span class="arrow">→</span>':''}<span class="node">${node}</span>`).join('');
 $('#trace-road').textContent=`/ ${r.road}`;$('#trace').innerHTML=response.traces[String(selected)].map((step,i)=>`<li><span class="step">${String(i+1).padStart(2,'0')}</span><b>${escapeHtml(step.component)}</b><span class="message">${escapeHtml(step.message)}</span></li>`).join('');
 $('#raw-data').textContent=JSON.stringify(response.boards?.[String(selected)] || response.roads.find(r=>r.id===selected),null,2);
}
function updateOutputs(){$('#speed-value').textContent=`${$('#speed').value} km/h`;$('#volume-value').textContent=`${$('#volume').value} veíc/min`;}
$('#speed').oninput=updateOutputs;$('#volume').oninput=updateOutputs;
$('#sensor-form').onsubmit=async e=>{e.preventDefault();const next=structuredClone(roads),r=next.find(r=>r.id===selected);Object.assign(r,{average_speed:Number($('#speed').value),vehicles_per_minute:Number($('#volume').value),traffic_light_green_time:Number($('#green').value),weather:$('#weather').value,accident:$('#accident').checked,event:$('#event').checked});reading++;await analyze(next,architecture,'Sensores aplicados. Decisão atualizada.');};
$('#road-select').onchange=e=>{selected=Number(e.target.value);render();};
document.addEventListener('click',e=>{const target=e.target.closest('[data-road]');if(target&&!busy){selected=Number(target.dataset.road);render();}});
document.addEventListener('keydown',e=>{if((e.key==='Enter'||e.key===' ')&&e.target.matches('[data-road]:not(button)')){e.preventDefault();e.target.dispatchEvent(new MouseEvent('click',{bubbles:true}));}});
document.querySelectorAll('[data-arch]').forEach(el=>el.onclick=()=>analyze(roads,el.dataset.arch));
$('#simulate').onclick=()=>{reading++;const next=roads.map(r=>({...r,average_speed:10+Math.floor(Math.random()*56),vehicles_per_minute:25+Math.floor(Math.random()*86),accident:Math.random()<.15,weather:['clear','clear','light_rain','heavy_rain'][Math.floor(Math.random()*4)]}));analyze(next,architecture,'Nova leitura gerada para as quatro vias.');};
$('#reset').onclick=()=>{reading=0;analyze(structuredClone(initial),architecture,'Dataset inicial restaurado.');};
document.querySelectorAll('[data-scenario]').forEach(el=>el.onclick=()=>{const next=structuredClone(initial);if(el.dataset.scenario==='clear'){next.forEach(r=>Object.assign(r,{average_speed:50,vehicles_per_minute:35,accident:false,weather:'clear',event:false}));}else{selected=el.dataset.scenario==='rush'?1:3;}reading++;analyze(next,architecture,`Cenário aplicado: ${el.querySelector('strong').textContent}.`);});
$('#cards-view').onclick=()=>setView(false);$('#table-view').onclick=()=>setView(true);
function setView(table){tableMode=table;$('#cards-view').classList.toggle('active',!table);$('#table-view').classList.toggle('active',table);$('#cards-view').setAttribute('aria-pressed',!table);$('#table-view').setAttribute('aria-pressed',table);if(response)render();}
document.querySelectorAll('[data-page]').forEach(el=>el.onclick=()=>{document.querySelectorAll('[data-page]').forEach(x=>x.classList.toggle('active',x===el));['monitor','compare','guide'].forEach(page=>$(`#${page}-page`).hidden=page!==el.dataset.page);});
$('#compare').onclick=async()=>{if(busy)return;lock(true);try{const snapshot=structuredClone(roads),all=[];for(const key of Object.keys(architectures))all.push(await request('/api/analyze',{architecture:key,roads:snapshot}));const equal=all.every(r=>JSON.stringify(r.roads)===JSON.stringify(all[0].roads));$('#comparison-results').innerHTML=`<div class="${equal?'comparison-success':'comparison-fail'}">${equal?'✓ Resultados equivalentes nas três arquiteturas.':'△ Divergência detectada nos resultados.'} Leitura ${reading} · comparação de todos os campos retornados.</div><div class="table-scroll"><table><thead><tr><th>Via</th>${all.map(r=>`<th>${architectures[r.architecture].name}<br><small>${r.duration_ms} ms de servidor</small></th>`).join('')}</tr></thead><tbody>${snapshot.map((road,i)=>`<tr><td>${road.road}</td>${all.map(r=>`<td>${badge(r.roads[i])}<p>${r.roads[i].recommendation}</p></td>`).join('')}</tr>`).join('')}</tbody></table></div>`;$('#error').hidden=true;}catch(error){errorMessage(error);}finally{lock(false);}};
async function init(){lock(true);try{const data=await request('/api/roads');initial=structuredClone(data.roads);roads=structuredClone(initial);}catch(error){errorMessage(error);}finally{lock(false);}if(roads.length)await analyze();else{document.querySelectorAll('#monitor-page button,#compare').forEach(el=>el.disabled=true);$('#error').append(' Recarregue a página após iniciar a API.');}}
init();
