import { useState } from "react";
import { useParams } from "react-router-dom";


const Agent = () => {
    
    const {file_id} = useParams();
    const [prompt, setPrompt] = useState(null)

    const getResponse = async (id) =>{
        
        const URL =`http://localhost:8000/ai/${id}`

        const formData = new FormData()
        formData.append("file_id", id)
        formData.append("prompt", prompt)


        try{
            const response = await fetch(URL,{
            method: 'POST',
            body: formData
        })


        const data = await response.json();


        if (response.ok){
            console.log(data.response)
        } else{
            console.error(data.message)
        }


        } catch (error){
            console.error(error)
        }


    }

    return (
        <div>
            <h1>Enter a Prompt!</h1>
            <form onSubmit={(e) =>
            {
                e.preventDefault();
                 getResponse(file_id)
            }}>
                <input type="text" name="prompt" onChange={e => setPrompt(e.target.value)}/>
                <button type="submit">send</button>
            </form>
        </div>
    )
}

export default Agent;