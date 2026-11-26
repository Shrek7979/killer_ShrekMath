const katex=require('/home/claude/ks/src/katex.min.js');const d=JSON.parse(require('fs').readFileSync('/tmp/_k.json','utf8'));
const walk=o=>{if(typeof o==='string'){const re=/\$\$([\s\S]+?)\$\$|\$([^$]+?)\$/g;let m;while((m=re.exec(o))){try{katex.renderToString(m[1]||m[2],{throwOnError:true})}catch(e){console.log('KaTeX: '+(m[1]||m[2]).slice(0,60)+' | '+e.message.slice(0,60))}}
 if((o.match(/\$/g)||[]).length%2)console.log('$ 짝 안맞음: '+o.slice(0,60))}else if(o&&typeof o==='object')Object.values(o).forEach(walk)};walk(d);
