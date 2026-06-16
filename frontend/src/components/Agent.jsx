import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

const Agent = () => {
    const { file_id } = useParams();

    const [prompt, setPrompt] = useState("");
    const [conversationArr, setConversationArr] = useState([]);

    useEffect(() => {
        console.log("Conversation updated:", conversationArr);
    }, [conversationArr]);


    const GetConversation = async (file_id) => {
        try {
            console.log(`id from conversation ${file_id}`);

            const conversationURL = `http://localhost:8000/get-conversation/${file_id}`;

            const response = await fetch(conversationURL, {
                method: "GET",
            });

            if (!response.ok) {
                console.error("Unable to fetch conversation from database");
                return;
            }

            const data = await response.json();

            console.log("Conversation data:", data);

            setConversationArr(data.messages || []);
        } catch (error) {
            console.error("Error fetching conversation:", error);
        }
    };

        useEffect(() => {
        if (file_id) {
            GetConversation(file_id);
        }
    }, [file_id]);



    
    const getResponse = async (id) => {
        const URL = `http://localhost:8000/ai/${id}`;

        const formData = new FormData();
        formData.append("file_id", id);
        formData.append("prompt", prompt);

        try {
            const response = await fetch(URL, {
                method: "POST",
                body: formData,
            });

            const data = await response.json();

            if (!response.ok) {
                console.error(data.message);
                return;
            }

            console.log(data.body.response);
            console.log("Answer is set");
            console.log("id is giving to conversation", id);

            // Refresh conversation after getting AI response
            await GetConversation(id);

            // Clear input
            setPrompt("");
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div>
            <h1>Enter a Prompt!</h1>

            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    getResponse(file_id);
                }}
            >
                <input
                    type="text"
                    name="prompt"
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                />

                <button type="submit">Send</button>
            </form>

            <div className="conversation">
                {conversationArr.length === 0 ? (
                    <p>No conversation yet.</p>
                ) : (
                    conversationArr.map((message, index) => (
                        <div key={index}>
                            <p>
                                <strong>You:</strong> {message.prompt}
                            </p>

                            <p>
                                <strong>AI:</strong> {message.response}
                            </p>

                            <hr />
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default Agent;