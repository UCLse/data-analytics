import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { pathToFileURL } from 'node:url';
let marked;
try { ({marked} = await import('marked')); }
catch (error) {
 if (!process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES) throw error;
 ({marked} = await import(pathToFileURL(path.join(process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES,'marked/lib/marked.esm.js')).href));
}

const project = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const source = path.join(project, 'heat-cascade');
const dist = path.resolve(process.env.HEAT_COURSE_OUTPUT || path.join(project,'docs'));
const base = (process.env.HEAT_COURSE_BASE ?? '/data-analytics').replace(/\/$/,'');
const withBase = html => html.replace(/\b(href|src)="\/(?!\/)/g, '$1="'+base+'/');
fs.mkdirSync(dist, {recursive:true});
function walk(directory) {
 const excluded = new Set(['.venv', 'venv', 'node_modules', '__pycache__', '.ipynb_checkpoints', '.git']);
 return fs.readdirSync(directory, {withFileTypes:true})
  .filter(entry => !excluded.has(entry.name))
  .flatMap(entry => entry.isDirectory()
   ? walk(path.join(directory, entry.name))
   : [path.join(directory, entry.name)]);
}
for (const file of ['styles.css','app.js','ucl-logo.svg']) fs.copyFileSync(path.join(project,'site-assets',file),path.join(dist,file));
fs.writeFileSync(path.join(dist,'.nojekyll'),'');
const lessons = [{number:0,stem:'00-setup',title:'Setup with VS Code or GitHub Codespaces',hours:1}, ...JSON.parse(fs.readFileSync(path.join(source,'docs/lesson_manifest.json'),'utf8'))];
const shortTitles = ['Setup your workspace','Python fundamentals','Read and explore data','Clean and audit data','Join the system layers','Explore and visualise','Build a transparent index','Linear regression','Trees and logistic regression','Neighbourhood clustering','Time-series evaluation','Decisions under uncertainty','Game and text analysis','Final analytical brief'];
const h = s => String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const groups = [{name:'01 / FOUNDATIONS',start:0,end:4},{name:'02 / ANALYTICAL METHODS',start:5,end:10},{name:'03 / DECISIONS & EVIDENCE',start:11,end:13}];
const lessonUrl = lesson => '/course/lessons/'+lesson.stem+'.html';
const activeNumber = url => lessons.findIndex(l=>lessonUrl(l)===url);

function nav(url){
 return `<a class="brand" href="/" aria-label="Heat Cascade course home"><span class="brand-mark" aria-hidden="true">HC</span><span>HEAT CASCADE<small>Python data analytics</small></span></a><div class="sidebar-intro">A guided route from your first line of Python to an evidence-led decision.</div><nav aria-label="Workshop route">${groups.map(group=>`<div class="nav-group"><p>${group.name}</p>${lessons.filter(l=>l.number>=group.start&&l.number<=group.end).map(l=>`<a href="${lessonUrl(l)}" ${url===lessonUrl(l)?'aria-current="page"':''}><span class="nav-number">${String(l.number).padStart(2,'0')}</span><span>${h(shortTitles[l.number])}</span><span class="completion-dot" data-completed="${l.stem}" aria-hidden="true"></span></a>`).join('')}</div>`).join('')}</nav><div class="side-bottom"><a href="/course/docs/data-dictionary.html">Data dictionary ↗</a><a href="/course/instructor/teaching-guide.html">Instructor guide ↗</a><p>Fictional city. Real analytical practice.<br>Every supplied record is synthetic.</p></div>`;
}

function layout(title,url,content,description='A UCL Python data analytics teaching activity for the Centre for Systems Engineering, Department of Space and Climate Physics.'){
return withBase(`<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="author" content="Sayara Beg"><meta name="description" content="${h(description)}"><meta name="theme-color" content="#361a54"><title>${h(title)} | UCL Heat Cascade</title><link rel="stylesheet" href="/styles.css"><script src="/app.js" defer></script></head><body><a class="skip-link" href="#main-content">Skip to content</a><header class="ucl-masthead" aria-label="UCL and department identity"><a class="ucl-logo-link" href="https://www.ucl.ac.uk/" aria-label="University College London"><img class="ucl-logo" src="/ucl-logo.svg" alt="UCL (University College London)" width="1394" height="391"></a><div class="ucl-department"><p class="ucl-university">University College London</p><a class="ucl-department-title" href="https://www.ucl.ac.uk/mathematical-physical-sciences/mssl">Department of Space and Climate Physics</a><p class="ucl-centre">UCL Centre for Systems Engineering</p><p class="ucl-faculty">Faculty of Mathematical and Physical Sciences</p></div></header><aside class="sidebar" id="sidebar">${nav(url)}</aside><div class="workspace"><header class="topbar"><button class="menu-button" type="button" aria-controls="sidebar" aria-expanded="false">☰ <span>Workshops</span></button><div class="top-links"><a href="/" ${url==='/'?'aria-current="page"':''}>Course</a><a href="/course/docs/data-dictionary.html">Data</a><a href="/resources.html" ${url==='/resources.html'?'aria-current="page"':''}>Resources</a></div><a class="setup-link" href="https://github.com/UCLse/data-analytics/fork">Fork the course <span aria-hidden="true">↗</span></a></header><main id="main-content">${content}</main><footer class="footer"><div><strong>Course author and research lead: <a href="https://profiles.ucl.ac.uk/106848-sayara-beg">Sayara Beg</a></strong><br>Lecturer, UCL Centre for Systems Engineering, Department of Space and Climate Physics,<br>Faculty of Mathematical and Physical Sciences.<br>Credit Sayara Beg when reusing or adapting these materials.</div><div><a href="/attribution.html">Attribution & public-release boundary</a><br><a href="/course/docs/verification.html">Verification & limitations</a></div></footer></div></body></html>`);
}

const hero = `<section class="hero"><div class="eyebrow"><span></span> UCL / SPACE & CLIMATE PHYSICS</div><h1>Turn heat data<br>into <em>decisions.</em></h1><p>Learn Python one step at a time. Explore how ecosystem change, heat and community vulnerability connect, then test what the evidence supports.</p><div class="hero-actions"><a class="button" href="${lessonUrl(lessons[0])}">Start with Workshop 00 <span aria-hidden="true">→</span></a><a class="quiet-link" href="/attribution.html">Authorship & attribution ↗</a></div><div class="hero-facts"><div><strong>14</strong><span>guided workshops</span></div><div><strong>28h</strong><span>indicative workload</span></div><div><strong>0</strong><span>Python prerequisites</span></div></div><div class="hero-art" aria-hidden="true"><div class="art-title">A CITY AS A CONNECTED SYSTEM</div><svg viewBox="0 0 350 280"><defs><linearGradient id="heat" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#993bff"/><stop offset="1" stop-color="#361a54"/></linearGradient></defs><rect x="22" y="30" width="306" height="220" rx="8" fill="#eedeff"/><path d="M22 100H328M22 178H328M112 30V250M230 30V250" stroke="#fafafa" stroke-width="15"/><rect x="32" y="40" width="70" height="50" rx="4" fill="#ddbdff"/><rect x="123" y="40" width="96" height="50" rx="4" fill="url(#heat)"/><rect x="241" y="40" width="77" height="50" rx="4" fill="#eedeff"/><rect x="32" y="111" width="70" height="56" rx="4" fill="#993bff"/><rect x="123" y="111" width="96" height="56" rx="4" fill="#ddbdff"/><rect x="241" y="111" width="77" height="56" rx="4" fill="#eedeff"/><rect x="32" y="190" width="70" height="50" rx="4" fill="#ddbdff"/><rect x="123" y="190" width="96" height="50" rx="4" fill="#eedeff"/><rect x="241" y="190" width="77" height="50" rx="4" fill="url(#heat)"/><circle cx="68" cy="64" r="15" fill="#361a54"/><circle cx="67" cy="213" r="14" fill="#361a54"/><circle cx="171" cy="214" r="14" fill="#361a54"/><circle cx="279" cy="138" r="15" fill="#361a54"/><path d="M69 67C128 57 144 127 175 141S240 132 280 212" fill="none" stroke="#361a54" stroke-width="2" stroke-dasharray="5 5"/><circle cx="175" cy="141" r="5" fill="#361a54"/><circle cx="280" cy="212" r="5" fill="#361a54"/></svg><div class="art-legend"><span><i class="ecosystem-colour"></i>Ecosystem</span><span><i class="heat-colour"></i>Heat & services</span></div><p>Illustrative map / synthetic teaching system</p></div></section>`;
const courseCards = groups.map(group=>`<section class="course-section"><div class="section-heading"><div><span class="eyebrow">${group.name}</span><h2>${group.start===0?'Build the foundations':group.start===5?'Make the analysis defensible':'Connect evidence to decisions'}</h2></div><span>${group.end-group.start+1} workshops</span></div><div class="lesson-grid">${lessons.filter(l=>l.number>=group.start&&l.number<=group.end).map(l=>`<a class="lesson-card" data-search="${h(shortTitles[l.number]+' '+l.title)}" href="${lessonUrl(l)}"><div class="card-top"><span class="lesson-number">${String(l.number).padStart(2,'0')}</span><span class="duration">${l.hours} ${l.hours===1?'hour':'hours'}</span></div><h3>${h(shortTitles[l.number])}</h3><p>${h(l.question??'Open your notebook, find the course files and run the first setup checks.')}</p><div class="card-bottom"><span data-card-state="${l.stem}">Open workshop</span><span aria-hidden="true">→</span></div></a>`).join('')}</div></section>`).join('');
fs.writeFileSync(path.join(dist,'index.html'),layout('Course home','/',`${hero}<section class="author-panel"><span class="eyebrow">UCL TEACHING ACTIVITY / COURSE AUTHOR</span><h2><a href="https://profiles.ucl.ac.uk/106848-sayara-beg">Sayara Beg</a></h2><p>This UCL teaching activity is delivered through the Centre for Systems Engineering within the Department of Space and Climate Physics, Faculty of Mathematical and Physical Sciences.</p><p>Course author and research lead: Sayara Beg, Lecturer.</p><p><strong>Heat Cascade is currently unfunded.</strong> This public release shares general teaching examples and synthetic data. Detailed proposal architecture and work-package plans are withheld.</p><a href="/attribution.html">Credit Sayara Beg when reusing or adapting the material →</a></section><section class="course-intro"><div><span class="eyebrow">YOUR LEARNING ROUTE</span><h2>One system. A complete workflow.</h2><p>Each workshop explains what to do, why it matters and how to read the result. Start with your own GitHub fork. Run the code in Codespaces or a local clone in VS Code, then commit and push each workshop checkpoint.</p></div><div class="progress-panel"><div><span>Your progress</span><strong id="progress-text">0 / 14</strong></div><progress id="course-progress" max="14" value="0">0 of 14 workshops</progress><small>Stored in this browser. No student records are submitted.</small></div></section><div class="route-tools"><label for="lesson-search">Find a workshop</label><input id="lesson-search" type="search" placeholder="Try regression, data or uncertainty"><button id="reset-progress" type="button">Reset progress</button></div><p id="search-empty" hidden>No workshops match that search.</p>${courseCards}<section class="boundary-panel"><span class="eyebrow">THE EVIDENCE BOUNDARY</span><h2>Fictional data. Explicit assumptions.</h2><p>The exercises use 12 invented neighbourhoods and small, reproducible datasets. Their patterns are teaching examples. A model result, questionnaire change or scenario ranking needs further evidence before it can support a research or operational claim.</p><a href="/course/docs/research-alignment.html">Read the research alignment →</a></section>`));

function rewrittenMarkdown(text,relativePath){
 return text.replace(/\[([^\]]+)\]\(([^)]+)\)/g,(match,label,link)=>{
  if(link.includes('://')||link.startsWith('#')) return match;
  const [clean,fragment] = link.split('#');
  const resolved = path.posix.normalize(path.posix.join(path.posix.dirname(relativePath),clean));
  let target;
  if(resolved.endsWith('.md')) target='/course/'+resolved.slice(0,-3)+'.html';
  else if(fs.existsSync(path.join(source,resolved))&&fs.statSync(path.join(source,resolved)).isDirectory()) target='/course/'+resolved.replace(/\/$/,'')+'/index.html';
  else return label+' (`'+resolved+'`)';
  return '['+label+']('+target+(fragment?'#'+fragment:'')+')';
 });
}

function renderMarkdown(text,relativePath){
 let html = marked.parse(rewrittenMarkdown(text,relativePath),{gfm:true});
 const used = new Map();
 html = html.replace(/<h([1-6])>(.*?)<\/h\1>/gs,(match,level,label)=>{
  let id=label.replace(/<[^>]*>/g,'').toLowerCase().replace(/[^a-z0-9 -]/g,'').trim().replace(/ +/g,'-');
  const count = used.get(id)||0;used.set(id,count+1);if(count)id+='-'+count;
  return `<h${level} id="${id}">${label}</h${level}>`;
 });
 html = html.replace(/<table>/g,'<div class="table-wrap" role="region" aria-label="Data table" tabindex="0"><table>').replace(/<\/table>/g,'</table></div>');
 html = html.replace(/<pre><code class="language-mermaid">.*?<\/code><\/pre>/gs,'<div class="system-boundary"><strong>System boundary</strong><p>Ecosystem condition influences heat exposure. Heat connects to infrastructure pressure and community vulnerability. Governance and adaptation feed back into ecosystem condition, supported by data stewardship and assurance.</p><p>These are hypothesised pathways for inquiry, not validated synthetic-data findings.</p></div>');
 return html;
}


for(const file of walk(source).filter(file=>file.endsWith('.md'))){
 const relativePath=path.relative(source,file).split(path.sep).join('/');
 const text=fs.readFileSync(file,'utf8');
 const url='/course/'+relativePath.slice(0,-3)+'.html';
 const title=text.match(/^# (.*)/m)?.[1]??'Course resource';
 const index=activeNumber(url); const lesson=index>=0?lessons[index]:null;
 const notebook=lesson&&lesson.number>0?`<a class="button secondary" href="${lessonUrl(lessons[0])}#2-create-an-account-and-fork-the-course">Work in your own fork →</a>`:'';
 const pager=lesson?`<nav class="lesson-pager" aria-label="Workshop navigation">${index>0?`<a href="${lessonUrl(lessons[index-1])}">← ${h(shortTitles[index-1])}</a>`:'<a href="/">← Course home</a>'}${index<lessons.length-1?`<a href="${lessonUrl(lessons[index+1])}">${h(shortTitles[index+1])} →</a>`:'<a href="/resources.html">Assessment resources →</a>'}</nav>`:'';
 const content=`<div class="document-top"><a href="/">Course home</a><span>/</span><span>${lesson?'Workshop '+String(lesson.number).padStart(2,'0'):'Resource'}</span></div><div class="document-actions">${notebook}${lesson?`<button type="button" class="completion-button" data-mark="${lesson.stem}" aria-pressed="false">Mark complete</button>`:''}</div><article class="prose">${renderMarkdown(text,relativePath)}</article>${pager}`;
 const destination=path.join(dist,'course',relativePath.slice(0,-3)+'.html');fs.mkdirSync(path.dirname(destination),{recursive:true});fs.writeFileSync(destination,layout(title,url,content));
}

const rawFiles=fs.readdirSync(path.join(source,'data/raw')).filter(file=>file.endsWith('.csv'));
const rawIndex=path.join(dist,'course/data/raw/index.html');fs.mkdirSync(path.dirname(rawIndex),{recursive:true});fs.writeFileSync(rawIndex,layout('Raw teaching tables','/course/data/raw/index.html',`<div class="document-top"><a href="/">Course home</a><span>/</span><span>Data</span></div><article class="prose"><h1>Raw teaching tables</h1><p>All eight files contain fictional records or invented scenario assumptions. Create your own fork of <a href="https://github.com/UCLse/data-analytics/fork">UCLse/data-analytics</a>, then follow Workshop 00. These tables are available inside the fork and its Codespaces or local clone.</p><p><a href="${lessonUrl(lessons[0])}">Student setup →</a> · <a href="/course/docs/data-dictionary.html">Read the data dictionary →</a></p><ul class="resource-list">${rawFiles.map(file=>`<li class="resource-file"><strong>${h(file)}</strong><span>In your fork: <code>heat-cascade/data/raw/${h(file)}</code></span></li>`).join('')}</ul></article>`));

const resources=[['Student setup','lessons/00-setup','Create a GitHub account, fork the course and choose Codespaces or local VS Code.'],['Data dictionary','docs/data-dictionary','Keys, units, observation levels and synthetic-data boundaries.'],['Code-reading guide','docs/code-reading-guide','Read recurring Python syntax before changing it.'],['Troubleshooting','docs/troubleshooting','Diagnose common errors and recover a working notebook.'],['Research alignment','docs/research-alignment','Authorship, unfunded status and the public teaching boundary.'],['Assessment brief','docs/assessment','Deliverables, suggested rubric and submission checks.'],['Final-brief template','templates/final-brief','A structured route to a conditional recommendation.'],['Real-data readiness','templates/real-data-readiness','Review measurement and assurance before using observations.'],['Instructor guide','instructor/teaching-guide','Delivery, differentiation and assessment stewardship.'],['Practice answers','instructor/practice-answers','Check independent tasks after attempting them.'],['Source provenance','docs/sources','Checked software documentation and the synthetic-data boundary.'],['Course verification','docs/verification','Reference execution, structural checkpoints and limits.']];
fs.writeFileSync(path.join(dist,'resources.html'),layout('Resources','/resources.html',`<section class="resource-header"><span class="eyebrow">SUPPORT FOR THE WHOLE WORKFLOW</span><h1>Course resources.</h1><p>Use these guides alongside the workshops. Keep the data boundary visible from the first input to the final recommendation.</p><a class="button" href="https://github.com/UCLse/data-analytics/fork">Create your course fork ↗</a></section><div class="resource-grid">${resources.map(([title,url,description])=>`<a class="resource-card" href="/course/${url}.html"><h2>${title} <span aria-hidden="true">↗</span></h2><p>${description}</p></a>`).join('')}</div>`));

console.log(JSON.stringify({workshops:lessons.length,html_pages:walk(dist).filter(file=>file.endsWith('.html')).length}));

const attribution=fs.readFileSync(path.join(project,'ATTRIBUTION.md'),'utf8');
fs.writeFileSync(path.join(dist,'attribution.html'),layout('Authorship and attribution','/attribution.html',`<div class="document-top"><a href="/">Course home</a><span>/</span><span>Authorship</span></div><article class="prose">${renderMarkdown(attribution,'ATTRIBUTION.md')}</article>`));
console.log(JSON.stringify({base_path:base,author:'Sayara Beg',output:dist}));

// Public pages must not direct visitors to the author's source repository.
const forbiddenRepositoryUrl = /https?:\/\/(?:github\.com\/|raw\.githubusercontent\.com\/|api\.github\.com\/repos\/|codeload\.github\.com\/)sbeg88\b/i;
const repositoryLinks = walk(dist).filter(file=>file.endsWith('.html')&&forbiddenRepositoryUrl.test(fs.readFileSync(file,'utf8')));
if(repositoryLinks.length) throw new Error('Remove source repository links from public pages: '+repositoryLinks.join(', '));
