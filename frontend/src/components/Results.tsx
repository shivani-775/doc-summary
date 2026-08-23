import { CheckCircle2, Lightbulb, ListChecks } from 'lucide-react'
export default function Results({data}:{data:any}){
 return <div className="results">
  <section className="card"><div className="card-title"><CheckCircle2/> Summary</div><p className="summary">{data.summary}</p></section>
  <section className="card"><div className="card-title"><ListChecks/> Key points</div><ul>{data.key_points?.map((x:string,i:number)=><li key={i}>{x}</li>)}</ul></section>
  <section className="card"><div className="card-title"><Lightbulb/> Improvement suggestions</div><ul>{data.improvements?.map((x:string,i:number)=><li key={i}>{x}</li>)}</ul></section>
 </div>
}
