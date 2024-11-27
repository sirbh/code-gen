import { useState } from "react";
import "./App.css";
import { Box, Button, LinearProgress, TextField } from "@mui/material";
import axios from "axios";
import { useNavigate } from "react-router-dom";


function App() {
  const [spec, setSpec] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  // useEffect(() => {
  //   axios.get("http://localhost:5000/spec?message=this%20is%20the%20message")
  //   // axios.get("api/spec?message=this")
  //   .then((res) => {
  //     console.log(res);
  //   })
  //   .catch((err) => {
  //     console.log(err);
  //   })
  // }
  // , []);

  // useEffect(() => {
  //   setLoading(true);
  //   axios
  //     .get("/read-file")
  //     .then((res) => {
  //       setLoading(false);
  //       console.log(res.data);
  //       setFunctions(res.data['api.py']);
  //       setSpec(res.data['spec.yml']);
  //     })
  //     .catch((err) => {
  //       setLoading(false);
  //       console.log(err);
  //     });
  // }, []);




  // const clickHanlder = () => {
  //   setLoading(true);
  //   axios
  //     .post("/generate", { openapi_spec: spec })
  //     .then((res) => {
  //       setLoading(false);
  //       setFunctions(res.data['api.py']);
  //       setSpec(res.data['spec.yml']);
  //     })
  //     .catch((err) => {
  //       setLoading(false);
  //       console.log(err);
  //     });
  // }

  const sendHanlder = () => {
    setLoading(true);
    axios
      .get("http://localhost:5000/spec?message=" + message)
      .then((res) => {
        setLoading(false);
        console.log(res.data);
        setSpec(res.data);
      })
      .catch((err) => {
        setLoading(false);
        console.log(err);
      });
  }

  const handleGenerate = () => {
    setLoading(true);
    axios
      .get("http://localhost:5000/generate")
      .then((res) => {
        setLoading(false);
        console.log(res.data);
        navigate("/app");
      })
      .catch((err) => {
        setLoading(false);
        console.log(err);
        alert("Server could not generate the code");
      });
  }

  return (
    <>
      {loading && <LinearProgress sx={{ width: "100%" }} />}
      <Box
        sx={{
          width: "100vw",
          height: "100vh",
          padding: "20px",
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-between",
        }}
      >
        <Box
          sx={{
            width: "43%",
            height: "100%",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <TextField
            label="Spec Generator"
            sx={{ width: "100%", height: "90%", marginBottom: "50px" }}
            multiline
            minRows={15}
            maxRows={15}
            value={spec}
            onChange={(e) => {
              setSpec(e.target.value);
            }}
            disabled
          />
          {/* <Button
            sx={{ width: "100%" }}
            variant="contained"
            onClick={() => {
              clickHanlder();
            }}
          >
            Deploy
          </Button> */}
        </Box>
        <Box
          sx={{
            width: "23%",
            height: "100%",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <TextField
            label="User Prompt"
            sx={{ width: "100%", height: "60%", marginBottom: "50px" }}
            multiline
            minRows={15}
            maxRows={15}
            value={message}
            onChange={(e) => {
              setMessage(e.target.value);
            }}
          />
          <Button
            sx={{ width: "100%" }}
            variant="contained"
            onClick={() => {
              sendHanlder();
            }}
          >
            Send
          </Button>
        </Box>
        <Box
          sx={{
            width: "25%",
            height: "100%",
            display: "flex",
            flexDirection: "column",
          }}
        >
          <Button sx={{ width: "100%", marginTop: "50px" }} variant="contained" onClick={()=>{
            handleGenerate();
          }}>
            Generate
          </Button>
        </Box>
      </Box>
    </>
  );
}

export default App;
