// import { useState } from "react"
// import { BrowserRouter, Route, Routes, useNavigate } from "react-router-dom"
// import Agent from "./components/Agent"


// const Home = () => {
  
//   const url = "http://localhost:8000/uploads"
//   const [file, setFile] = useState(null)


//   const navigate = useNavigate()


//   const sendFile = async (e) => {

//     e.preventDefault();

//     const formData = new FormData();
//     formData.append("file", file);

//     try {

//       let response = await fetch(url, {
//         method: 'POST',
//         body: formData
//       })
//         .catch(error => console.error(error))

//       const data = await response.json()


//       console.log(`${data.status} ${data.body.id}`)

//       navigate(`/ai/${data.body.id}`)

//     } catch (error) {
//       console.log(error)
//     }
//   }


//   return <>
//     <form onSubmit={sendFile}>
//       <input
//         type="file"
//         accept=".csv"
//         onChange={(e) => setFile(e.target.files[0])}
//       />

//       {/* <Link to="/ai"> */}
//       <button type="submit">Submit</button>
//       {/* </Link> */}
//     </form>
//   </>
// }


// const App = () => {
//   return (
//     <BrowserRouter>

//       <Routes>
//         <Route path="/" element={<Home />} />
//         <Route path="/ai/:file_id" element={<Agent />} />
//       </Routes>

//     </BrowserRouter>
//   )
// }

// export default App;


import { useState } from "react"
// Sales Analyzer Chatbot — Home UI
import { BrowserRouter, Route, Routes, useNavigate } from "react-router-dom"
import Agent from "./components/Agent"


const styles = {
  page: {
    minHeight: "100vh",
    background: "#f9fafb",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontFamily: "Inter, system-ui, sans-serif",
    padding: "2rem 1rem",
  },
  card: {
    background: "#ffffff",
    borderRadius: "16px",
    border: "1px solid #e5e7eb",
    padding: "2.5rem 2rem",
    maxWidth: "480px",
    width: "100%",
    textAlign: "center",
  },
  badge: {
    display: "inline-flex",
    alignItems: "center",
    gap: "6px",
    fontSize: "12px",
    fontWeight: "500",
    background: "#EAF3DE",
    color: "#3B6D11",
    borderRadius: "20px",
    padding: "4px 14px",
    marginBottom: "1.25rem",
  },
  title: {
    fontSize: "26px",
    fontWeight: "600",
    color: "#111827",
    margin: "0 0 0.75rem",
    lineHeight: "1.3",
  },
  desc: {
    fontSize: "14px",
    color: "#6b7280",
    lineHeight: "1.75",
    margin: "0 0 2rem",
  },
  dropzone: (isDragging, hasFile) => ({
    border: `1.5px dashed ${isDragging ? "#1D9E75" : hasFile ? "#1D9E75" : "#d1d5db"}`,
    borderRadius: "12px",
    padding: "1.75rem 1.25rem",
    background: isDragging ? "#E1F5EE" : hasFile ? "#f0fdf4" : "#f9fafb",
    cursor: "pointer",
    transition: "all 0.2s",
    marginBottom: "0.75rem",
  }),
  dropIcon: {
    fontSize: "28px",
    marginBottom: "0.5rem",
    display: "block",
    color: "#1D9E75",
  },
  dropText: {
    fontSize: "14px",
    color: "#6b7280",
    margin: "0 0 4px",
  },
  dropHint: {
    fontSize: "12px",
    color: "#9ca3af",
    margin: "0",
  },
  fileName: (hasFile) => ({
    fontSize: "13px",
    color: hasFile ? "#0F6E56" : "#9ca3af",
    marginBottom: "1.25rem",
    minHeight: "18px",
  }),
  btn: (disabled) => ({
    width: "100%",
    padding: "11px",
    background: disabled ? "#f3f4f6" : "#1D9E75",
    color: disabled ? "#9ca3af" : "#ffffff",
    border: disabled ? "1px solid #e5e7eb" : "none",
    borderRadius: "8px",
    fontSize: "15px",
    fontWeight: "500",
    cursor: disabled ? "not-allowed" : "pointer",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "8px",
    transition: "background 0.15s",
  }),
  divider: {
    display: "flex",
    alignItems: "center",
    gap: "12px",
    margin: "1.75rem 0 1.25rem",
  },
  hr: {
    flex: "1",
    border: "none",
    borderTop: "1px solid #e5e7eb",
  },
  dividerLabel: {
    fontSize: "12px",
    color: "#9ca3af",
  },
  features: {
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)",
    gap: "10px",
  },
  feat: {
    background: "#f9fafb",
    borderRadius: "8px",
    padding: "0.85rem 0.5rem",
    border: "1px solid #f3f4f6",
  },
  featIcon: {
    fontSize: "18px",
    color: "#1D9E75",
    display: "block",
    marginBottom: "6px",
  },
  featText: {
    fontSize: "12px",
    color: "#6b7280",
    margin: "0",
    lineHeight: "1.45",
  },
  privateNote: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "6px",
    fontSize: "12px",
    color: "#9ca3af",
    marginTop: "1.5rem",
  },
}

const Home = () => {

  const url = "http://localhost:8000/uploads"
  const [file, setFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  const [loading, setLoading] = useState(false)

  const navigate = useNavigate()

  const sendFile = async () => {
    if (!file) return
    setLoading(true)

    const formData = new FormData()
    formData.append("file", file)

    try {
      let response = await fetch(url, {
        method: "POST",
        body: formData,
      }).catch((error) => console.error(error))

      const data = await response.json()
      console.log(`${data.status} ${data.body.id}`)
      navigate(`/ai/${data.body.id}`)
    } catch (error) {
      console.log(error)
      setLoading(false)
    }
  }

  const handleFileInput = (e) => {
    const selected = e.target.files[0]
    if (selected) setFile(selected)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const dropped = e.dataTransfer.files[0]
    if (dropped && dropped.name.endsWith(".csv")) {
      setFile(dropped)
    }
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => setIsDragging(false)

  const openPicker = () => document.getElementById("csv-input").click()

  return (
    <div style={styles.page}>
      <div style={styles.card}>

        <div style={styles.badge}>
          🔒 Private access only
        </div>

        <h1 style={styles.title}>Sales Analyzer<br />Chatbot</h1>

        <p style={styles.desc}>
          Upload your Shopify sales export to unlock automated insights,
          revenue breakdowns, and trend analysis — all in a single conversation.
          No dashboards to configure, no spreadsheets to maintain.
        </p>

        <div
          style={styles.dropzone(isDragging, !!file)}
          onClick={openPicker}
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
        >
          <span style={styles.dropIcon}>📂</span>
          <p style={styles.dropText}>
            <span style={{ color: "#1D9E75", fontWeight: "500" }}>Click to upload</span>
            {" "}or drag & drop your file
          </p>
          <p style={styles.dropHint}>Shopify orders export · .csv only</p>
        </div>

        <input
          id="csv-input"
          type="file"
          accept=".csv"
          style={{ display: "none" }}
          onChange={handleFileInput}
        />

        <p style={styles.fileName(!!file)}>
          {file ? `📄 ${file.name}` : "No file selected"}
        </p>

        <button
          style={styles.btn(!file || loading)}
          disabled={!file || loading}
          onClick={sendFile}
        >
          {loading ? "Uploading…" : "✦ Analyze my sales"}
        </button>

        <div style={styles.divider}>
          <hr style={styles.hr} />
          <span style={styles.dividerLabel}>What you get</span>
          <hr style={styles.hr} />
        </div>

        <div style={styles.features}>
          <div style={styles.feat}>
            <span style={styles.featIcon}>📊</span>
            <p style={styles.featText}>Revenue charts & trends</p>
          </div>
          <div style={styles.feat}>
            <span style={styles.featIcon}>💡</span>
            <p style={styles.featText}>AI-powered insights</p>
          </div>
          <div style={styles.feat}>
            <span style={styles.featIcon}>💬</span>
            <p style={styles.featText}>Ask anything about sales</p>
          </div>
        </div>

        <div style={styles.privateNote}>
          🛡️ This tool is for authorized use only and is not publicly available
        </div>

      </div>
    </div>
  )
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