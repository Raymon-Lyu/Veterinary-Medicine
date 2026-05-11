var c=Object.defineProperty;var u=Object.getOwnPropertyDescriptor;var f=Object.getOwnPropertyNames;var w=Object.prototype.hasOwnProperty;var b=(r,e)=>{for(var t in e)c(r,t,{get:e[t],enumerable:!0})},g=(r,e,t,n)=>{if(e&&typeof e=="object"||typeof e=="function")for(let i of f(e))!w.call(r,i)&&i!==t&&c(r,i,{get:()=>e[i],enumerable:!(n=u(e,i))||n.enumerable});return r};var y=r=>g(c({},"__esModule",{value:!0}),r);var k={};b(k,{default:()=>l});module.exports=y(k);var a=require("obsidian"),p=require("@xterm/xterm"),x=require("@xterm/addon-fit"),h=require("child_process"),v=`
.xterm { cursor: text; position: relative; user-select: none; -ms-user-select: none; -webkit-user-select: none; }
.xterm.focus, .xterm:focus { outline: none; }
.xterm .xterm-helpers { position: absolute; top: 0; z-index: 5; }
.xterm .xterm-helper-textarea { padding: 0; border: 0; margin: 0; position: absolute; opacity: 0; left: -9999em; top: 0; width: 0; height: 0; z-index: -5; white-space: nowrap; overflow: hidden; resize: none; }
.xterm .composition-view { background: #000; color: #FFF; display: none; position: absolute; white-space: nowrap; z-index: 1; }
.xterm .composition-view.active { display: block; }
.xterm .xterm-viewport { background-color: #000; overflow-y: scroll; cursor: default; position: absolute; right: 0; left: 0; top: 0; bottom: 0; }
.xterm .xterm-screen { position: relative; }
.xterm .xterm-screen canvas { position: absolute; left: 0; top: 0; }
.xterm-char-measure-element { display: inline-block; visibility: hidden; position: absolute; top: 0; left: -9999em; line-height: normal; }
.xterm.enable-mouse-events { cursor: default; }
.xterm.xterm-cursor-pointer, .xterm .xterm-cursor-pointer { cursor: pointer; }
.xterm.column-select.focus { cursor: crosshair; }
.xterm .xterm-accessibility:not(.debug), .xterm .xterm-message { position: absolute; left: 0; top: 0; bottom: 0; right: 0; z-index: 10; color: transparent; pointer-events: none; }
.xterm .xterm-accessibility-tree:not(.debug) *::selection { color: transparent; }
.xterm .xterm-accessibility-tree { font-family: monospace; user-select: text; white-space: pre; }
.xterm .xterm-accessibility-tree > div { transform-origin: left; width: fit-content; }
.xterm .live-region { position: absolute; left: -9999px; width: 1px; height: 1px; overflow: hidden; }
.xterm-dim { opacity: 1 !important; }
.xterm-underline-1 { text-decoration: underline; }
.xterm-underline-2 { text-decoration: double underline; }
.xterm-underline-3 { text-decoration: wavy underline; }
.xterm-underline-4 { text-decoration: dotted underline; }
.xterm-underline-5 { text-decoration: dashed underline; }
.xterm-overline { text-decoration: overline; }
.xterm-strikethrough { text-decoration: line-through; }
.xterm-screen .xterm-decoration-container .xterm-decoration { z-index: 6; position: absolute; }
.xterm-screen .xterm-decoration-container .xterm-decoration.xterm-decoration-top-layer { z-index: 7; }
.xterm-decoration-overview-ruler { z-index: 8; position: absolute; top: 0; right: 0; pointer-events: none; }
.xterm-decoration-top { z-index: 2; position: relative; }

.terminal-container { 
    height: 100%; 
    width: 100%; 
    background-color: #1e1e1e;
    padding: 5px;
}
`,s="gemini-view",d=class extends a.ItemView{terminal;fitAddon;process=null;constructor(e){super(e),this.terminal=new p.Terminal({cursorBlink:!0,fontSize:14,fontFamily:'Menlo, Monaco, "Courier New", monospace',theme:{background:"#1e1e1e",foreground:"#cccccc"},allowProposedApi:!0}),this.fitAddon=new x.FitAddon,this.terminal.loadAddon(this.fitAddon)}getViewType(){return s}getDisplayText(){return"Gemini CLI Terminal"}async onOpen(){let e=this.containerEl.children[1];e.empty(),e.style.padding="0",e.style.overflow="hidden";let t=document.createElement("style");t.innerHTML=v,e.appendChild(t);let n=e.createDiv({cls:"terminal-container"});this.terminal.open(n),setTimeout(()=>{this.fitAddon.fit(),this.terminal.writeln("\x1B[32mSystem: Ready. Type your prompt and press Enter.\x1B[0m"),this.terminal.write(`\r
> `)},100);let i="";this.terminal.onData(o=>{if(o==="\r"){this.terminal.write(`\r
`);let m=i.trim();m?this.process?this.process.stdin.write(m+`
`):this.startProcess(m):this.terminal.write("> "),i=""}else o==="\x7F"?i.length>0&&(i=i.slice(0,-1),this.terminal.write("\b \b")):o===""?this.process&&(this.process.kill(),this.terminal.writeln("^C")):(i+=o,this.terminal.write(o))}),window.addEventListener("resize",()=>this.fitAddon.fit())}startProcess(e){this.terminal.writeln("\x1B[33mSystem: Calling Gemini...\x1B[0m");try{this.process=(0,h.spawn)("powershell.exe",["-NoProfile","-Command",`gemini "${e.replace(/"/g,'`"')}"`],{shell:!0}),this.process.stdout.on("data",t=>{let n=t.toString().replace(/\n/g,`\r
`);this.terminal.write(n)}),this.process.stderr.on("data",t=>{this.terminal.write(`\x1B[31m${t.toString().replace(/\n/g,`\r
`)}\x1B[0m`)}),this.process.on("close",t=>{this.terminal.write(`\r
> `),this.process=null})}catch(t){this.terminal.writeln(`\x1B[31mSystem: Error: ${t.message}\x1B[0m`),this.terminal.write(`\r
> `)}}async onClose(){this.process&&this.process.kill()}},l=class extends a.Plugin{async onload(){this.registerView(s,e=>new d(e)),this.addRibbonIcon("terminal","Open Gemini Terminal",()=>{this.activateView()}),this.addCommand({id:"open-gemini-terminal",name:"Open Gemini Terminal",callback:()=>this.activateView()})}async activateView(){let{workspace:e}=this.app,t=null,n=e.getLeavesOfType(s);n.length>0?t=n[0]:(t=e.getRightLeaf(!1),t&&await t.setViewState({type:s,active:!0})),t&&e.revealLeaf(t)}};
