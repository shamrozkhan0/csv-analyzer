import { useState } from "react";
import { useParams } from "react-router-dom";


const Agent = () => {
    
    const {file_id} = useParams();
    const [prompt, setPrompt] = useState(null)
    const [answer, setAnswer] = useState(null)
    const [conversation, setConversation] = useState([])

    const addConversation = (prompt, response) =>{
        setConversation(e => e.append({"prompt":prompt, "content" : response}))
    }
 
    const getConversation = async (file_id) => {
        const conversationURL = `http://localhost:8000/get-conversation/${file_id}`
        const response = fetch(conversationURL,{
            method:'GET',
        })

        if(!response.ok){
            console.error("Unable to fetch conversation from database")
        }
        
        
    }

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

        if (!response.ok){
            console.error(data.message)
        }


        console.log(data.body.response)
        setAnswer(data.body.response )

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

            <div className="conversation">
                
            </div>

        </div>
    )
}

export default Agent;