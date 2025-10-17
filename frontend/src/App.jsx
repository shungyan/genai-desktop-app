import { useState, useEffect } from "react"; 

function App() {
  const [videoSrc, setVideoSrc] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [history, setHistory] = useState([]); 

  useEffect(() => {
    loadMessages();
  }, []);

  const loadMessages = async () => {
    try {
      const res = await fetch("http://localhost:1234/history");
      const data = await res.json();

      console.log("History response:", data);

      const parsed = Array.isArray(data)
        ? data.map(msg => ({
            text: msg.message,
            sender: msg.sender
          }))
        : Array.isArray(data.messages)
        ? data.messages.map(msg => ({
            text: msg.message,
            sender: msg.sender
          }))
        : [];

      setHistory(parsed); 
    } catch (err) {
      console.error("Failed to load messages:", err);
      setHistory([]);
    }
  };

  const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      const videoURL = URL.createObjectURL(file);
      setVideoSrc(videoURL);

      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("http://localhost:1234/upload_video", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      console.log(data.message); // "Video saved successfully."
    }
  };

  const handleSend = async () => {
    if (input.trim() === "") return;
    setMessages(prev => [...prev, { text: input, sender: "user" }]);

    const userMessage = input;
    setInput("");

    try {
      const res = await fetch("http://localhost:1234/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      const data = await res.json();
      setMessages(prev => [...prev, { text: data.reply, sender: "llm" }]);
    } catch (err) {
      console.error(err);
    }
  };



  return (
    <div
      style={{
        display: "flex",
        height: "100vh",
        width: "100vw", // Ensure full width
        backgroundColor: "#f9fafb",
        color: "#111",
        fontFamily: "sans-serif",
      }}
    >
      {/* Left side - video */}
      <div
        style={{
          width: "300px",
          borderRight: "1px solid #ddd",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "20px",
        }}
      >
        <h2>Upload Video</h2>
        <input type="file" accept="video/*" onChange={handleUpload} />
        {videoSrc && (
          <video
            src={videoSrc}
            controls
            style={{ width: "100%", marginTop: "20px", borderRadius: "10px" }}
          />
        )}
      </div>

      {/* Right side - chat */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
          padding: "20px",
        }}
      >

      {/* chat history bar */}
        <div
          style={{
            flex: 1,
            overflowY: "auto",
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "10px",
            marginBottom: "10px",
            backgroundColor: "white", 
          }}
        >
          <b>Chat History</b>
          {history.length === 0 ? (
            <p style={{ fontSize: "14px", color: "#666" }}>No history yet</p>
          ) : (
            history.map((msg, i) => (
              <div key={i} style={{ marginBottom: "8px" }}>
                <b>{msg.sender}:</b> {msg.text}
              </div>
            ))
          )}
        </div>
        {/* End of chat history bar */}

        <h2>Chat</h2>
        <div
          style={{
            flex: 1,
            overflowY: "auto",
            border: "1px solid #ddd",
            borderRadius: "8px",
            padding: "10px",
            marginBottom: "10px",
            backgroundColor: "white",
          }}
        >
          {messages.map((msg, index) => (
            <div key={index} style={{ marginBottom: "8px" }}>
              <b>{msg.sender}:</b> {msg.text}
            </div>
          ))}
        </div>

        <div style={{ display: "flex" }}>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type a message..."
            style={{
              flex: 1,
              padding: "8px",
              border: "1px solid #ccc",
              borderRadius: "6px",
            }}
          />
          <button
            onClick={handleSend}
            style={{
              marginLeft: "10px",
              padding: "8px 16px",
              backgroundColor: "#2563eb",
              color: "white",
              border: "none",
              borderRadius: "6px",
              cursor: "pointer",
            }}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
