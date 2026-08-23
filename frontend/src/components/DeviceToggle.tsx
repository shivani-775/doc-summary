import { Monitor, Smartphone } from 'lucide-react'
export default function DeviceToggle({device, setDevice}:{device:'desktop'|'phone',setDevice:(v:'desktop'|'phone')=>void}){
 return <div className="device-toggle"><button className={device==='desktop'?'active':''} onClick={()=>setDevice('desktop')}><Monitor size={15}/> Desktop</button><button className={device==='phone'?'active':''} onClick={()=>setDevice('phone')}><Smartphone size={15}/> Phone</button></div>
}
