import { useState } from "react"
import { BrowserRouter, Route, Routes, useNavigate } from "react-router-dom"
import Agent from "./components/Agent"


const Home = () => {
  
  const url = "http://localhost:8000/uploads"
  const [file, setFile] = useState(null)


  const navigate = useNavigate()


  const sendFile = async (e) => {

    e.preventDefault();

    const formData = new FormData();
    formData.append("file", file);

    try {

      let response = await fetch(url, {
        method: 'POST',
        body: formData
      })
        .catch(error => console.error(error))

      const data = await response.json()

      // file_id = data.body.id

      console.log(`${data.status} ${data.body.id} ${data.body.content}`)

      navigate(`/ai/${data.body.id}`)

    } catch (error) {
      console.log(error)
    }
  }


  return <>
    <form onSubmit={sendFile}>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />

      {/* <Link to="/ai"> */}
      <button type="submit">Submit</button>
      {/* </Link> */}
    </form>
  </>
}


const App = () => {
  return (
    <BrowserRouter>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/ai/:file_id" element={<Agent />} />
      </Routes>

    </BrowserRouter>
  )
}

export default App;

