import { UploadCloud, FileText } from 'lucide-react'
import { useRef, useState } from 'react'
export default function Uploader({onFile}:{onFile:(f:File)=>void}){
 const ref=useRef<HTMLInputElement>(null); const [over,setOver]=useState(false)
 const accept='.pdf,.png,.jpg,.jpeg,.webp'
 return <div className={`dropzone ${over?'over':''}`} onDragOver={e=>{e.preventDefault();setOver(true)}} onDragLeave={()=>setOver(false)} onDrop={e=>{e.preventDefault();setOver(false);const f=e.dataTransfer.files[0];if(f)onFile(f)}}>
  <input ref={ref} hidden type="file" accept={accept} onChange={e=>{const f=e.target.files?.[0];if(f)onFile(f)}}/>
  <div className="upload-icon"><UploadCloud/></div><h2>Drop your document here</h2><p>PDF, PNG, JPG, JPEG or WEBP · up to 10 MB</p><button className="primary" onClick={()=>ref.current?.click()}><FileText size={17}/> Choose file</button>
 </div>
}
