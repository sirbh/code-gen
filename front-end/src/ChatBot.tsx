import { Box, Button, LinearProgress, TextField } from "@mui/material";
import axios from "axios";
import { useState } from "react";

const ChatBot = () => {

    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [response, setResponse] = useState("");


    const clickHanlder = () => {
        setLoading(true);
        axios.get("http://localhost:5000/tester?message=" + input).then((res) => {
            setLoading(false);
            setResponse(res.data.message);
            console.log(res.data);
        }).catch((err) => {
            setLoading(false);
            console.log(err);
        });
    }

    return <>
        {loading && <LinearProgress />}
        <Box
            sx={{
                width: "100vw",
                minHeight: "100vh",
                padding: "20px",
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
            }}
        >
            <TextField
                label="Ask me about the API eg. show me list of user in html with styles"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                multiline
                minRows={3}
                maxRows={3}
                sx={{
                    width: "80%",
                }} />
            <Button
                sx={{ width: "80%", marginTop: "20px" }}
                variant="contained"
                onClick={() => {
                    clickHanlder();
                }}
                disabled={loading}
            >
                ASK
            </Button>

            {/* <div style={{ marginTop: "40px", padding:"5rem" }} dangerouslySetInnerHTML={{ __html: response }}></div> */}
            <Box sx={{
                width: "80%",
                height: "70vh",
                marginTop: "40px",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
            }}>
                <iframe width={"100%"} style={{border:0}} height={"100%"} srcDoc={response}></iframe>
            </Box>
        </Box>
    </>
}

export default ChatBot
