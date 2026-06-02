import { useState } from "react"
import { BrowserRouter, Link, Route, Routes } from "react-router-dom"
import Agent from "./components/Agent"

const Home = () => {
  const url = "http://localhost:8000/uploads"
  const downloadUrl = "http://localhost:8000/download/"
  const [file, setFile] = useState(null)
  const [filename, setFilename] = useState(null)

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

      console.log(data.body.summary)
      setFilename(data.body.filename)


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

      <Link to="/ai">
        <button type="submit">Submit</button>
      </Link>
    </form>

    <button onClick={() => window.open(`${downloadUrl + filename}`, "_blank")}>
      Open Cleaned File
    </button></>
}


const App = () => {
  return (
    <BrowserRouter>

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/ai" element={<Agent />} />
      </Routes>

    </BrowserRouter>
  )
}

export default App;

