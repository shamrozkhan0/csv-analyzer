import { useState } from "react"

const App = () => {

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

      const data  = await response.json()

      setFilename(data.filename)

    } catch (error) {
      console.log(error)
    }


  }



  return (
    <>

      <form onSubmit={sendFile}>
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <button type="submit">Submit</button>
      </form>

   <button onClick={() => window.open(`${downloadUrl + filename}`, "_blank")}>
  Open Cleaned File
</button>

    </>
  )
}

export default App;

