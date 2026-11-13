const API=process.env.NEXT_PUBLIC_API_URL||"http://localhost:8000";
export async function getData(path:string){const res=await fetch(`${API}/api/v1/${path}`,{cache:"no-store"});if(!res.ok)throw new Error(`API request failed: ${res.status}`);return res.json();}
