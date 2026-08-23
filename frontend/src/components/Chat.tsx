import { Bot, Send } from 'lucide-react'
import { useState } from 'react'
import { chat } from '../services/api'
export default function Chat({documentId}:{documentId:string}){
 const [q,setQ]=useState(''); const [messages,setMessages]=useState<{role:'user'|'ai',text:string,sources?:number[]}[]>([]); const [loading,setLoading]=useState(false)
 async function ask(){if(!q.trim()||loading)return; const question=q.trim();setQ('');setMessages(m=>[...m,{role:'user',text:question}]);setLoading(true);try{const a=await chat(documentId,question);setMessages(m=>[...m,{role:'ai',text:a.answer,sources:a.sources}])}catch(e:any){setMessages(m=>[...m,{role:'ai',text:e.message||'Something went wrong.'}])}finally{setLoading(false)}}
 return <section className="chat card"><div className="card-title"><Bot/> Ask your document</div><div className="chat-messages">{messages.length===0&&<div className="empty-chat">Ask things like <b>“What is the meeting about?”</b> or <b>“What deadlines are mentioned?”</b></div>}{messages.map((m,i)=><div className={`bubble ${m.role}`} key={i}><span>{m.text}</span>{m.sources&&m.sources.length>0&&<small>Source: page {m.sources.join(', ')}</small>}</div>)}{loading&&<div className="bubble ai">Thinking…</div>}</div><div className="chat-input"><input value={q} onChange={e=>setQ(e.target.value)} onKeyDown={e=>{if(e.key==='Enter')ask()}} placeholder="Ask anything about this document…"/><button onClick={ask} disabled={loading||!q.trim()}><Send size={17}/></button></div></section>
}
