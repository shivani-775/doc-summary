import { useState } from 'react'
import { FileText, Sparkles, LoaderCircle, RotateCcw } from 'lucide-react'
import Uploader from './components/Uploader'
import DeviceToggle from './components/DeviceToggle'
import Results from './components/Results'
import Chat from './components/Chat'
import { uploadDocument, summarize } from './services/api'
import './styles.css'

type Device='desktop'|'phone'
export default function App(){
 const [device,setDevice]=useState<Device>('desktop'); const [file,setFile]=useState<File|null>(null); const [doc,setDoc]=useState<any>(null); const [length,setLength]=useState('medium'); const [result,setResult]=useState<any>(null); const [loading,setLoading]=useState(''); const [error,setError]=useState('')
 async function handleFile(f:File){setError('');setResult(null);setFile(f);setLoading('Reading document…');try{const d=await uploadDocument(f);setDoc(d)}catch(e:any){setFile(null);setError(e.message)}finally{setLoading('')}}
 async function generate(){if(!doc)return;setError('');setLoading('Generating insights…');try{setResult(await summarize(doc.document_id,length))}catch(e:any){setError(e.message)}finally{setLoading('')}}
 return <div className={`app ${device}`}>
  <header><div className="brand"><div className="logo"><Sparkles size={18}/></div><div><strong>DocuMind</strong><span>Document Intelligence Assistant</span></div></div><DeviceToggle device={device} setDevice={setDevice}/></header>
  <main>
   {!doc ? <><div className="hero"><div className="eyebrow">UPLOAD · UNDERSTAND · ASK</div><h1>Understand your documents<br/><em>in seconds.</em></h1><p>Turn PDFs and scanned documents into clear summaries, key points, and answers.</p></div><Uploader onFile={handleFile}/></>:
   <div className="workspace">
    <div className="document-bar"><div className="file-meta"><FileText size={20}/><div><b>{doc.filename}</b><span>{doc.pages} page{doc.pages!==1?'s':''} · {Math.round(doc.characters/1000)}k characters</span></div></div><button className="ghost" onClick={()=>{setDoc(null);setFile(null);setResult(null)}}><RotateCcw size={15}/> New document</button></div>
    <div className="controls"><div><span>Summary length</span><div className="lengths">{['small','medium','large'].map(x=><button key={x} className={length===x?'selected':''} onClick={()=>setLength(x)}>{x[0].toUpperCase()+x.slice(1)}</button>)}</div></div><button className="primary generate" onClick={generate} disabled={!!loading}><Sparkles size={17}/>{loading||'Generate summary'}</button></div>
    {error&&<div className="error">{error}</div>}
    {result&&<div className="content-grid"><div><Results data={result}/></div><Chat documentId={doc.document_id}/></div>}
    {!result&&!loading&&<div className="ready"><Sparkles/><h3>Your document is ready.</h3><p>Choose a summary length and generate your insights.</p></div>}
    {loading&&<div className="processing"><LoaderCircle className="spin"/><h3>{loading}</h3><p>This can take a few seconds.</p></div>}
   </div>}
  </main>
  <footer>DocuMind · Built for document understanding</footer>
 </div>
}
