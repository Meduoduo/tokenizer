import axios from 'axios'

export class Response {}

export const api_base = (url: string, method: string, args: any) => new Promise<Response | boolean>((resolve) => {
    (async function(){
        args = args || ''
        switch(method.toLowerCase()){
            case 'post':
                try{
                    const data = await axios.post<Response>(url, args)
                    resolve(typeof data === 'string' ? false : data.data)
                }catch(e){
                    resolve(false)
                }
                break
            case 'get':
                try{
                    const data = await axios.get<Response>(url + '?' + args)
                    resolve(typeof data === 'string' ? false : data.data)
                }catch(e){
                    resolve(false)
                }
                break
        }
    })()
})