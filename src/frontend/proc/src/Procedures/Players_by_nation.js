import React, { useState } from "react";
import {
  Box,
  CircularProgress,
  Container,
  FormControl,
  InputLabel,
  Input,
  Button,
} from "@mui/material";

function Players_by_nation() {
  const [selectedNation, setselectedNation] = useState("");
  const [procData, setProcData] = useState(null);

  const handleFetchData = () => {
    console.log("Fetching data...");
    if (selectedNation) {
      fetch(`http://localhost:20004/api/players_by_nation/${selectedNation}`)
        .then((response) => response.json())
        .then((data) => {
          setProcData(data);
        })
        .catch((error) => console.error("Error fetching data:", error));
    } else {
      setProcData(null);
    }
  };

  return (
    <>
      <h1>Players by Nation</h1>

      <Container
        maxWidth="100%"
        sx={{
          backgroundColor: "background.default",
          padding: "2rem",
          borderRadius: "1rem",
        }}
      >
        <Box>
          <h2 style={{ color: "white" }}>Options</h2>
          <FormControl fullWidth>
            <InputLabel htmlFor="nation-input">Nation</InputLabel>
            <Input
              id="nation-input"
              value={selectedNation}
              onChange={(e) => setselectedNation(e.target.value)}
            />
          </FormControl>
          <Button
            variant="contained"
            onClick={handleFetchData}
            sx={{ marginTop: "1rem" }}
          >
            Fetch Data
          </Button>
        </Box>
      </Container>

      <Container
        maxWidth="100%"
        sx={{
          backgroundColor: "info.dark",
          padding: "2rem",
          marginTop: "2rem",
          borderRadius: "1rem",
          color: "white",
        }}
      >
        <h2>
          Results <small>(PROC)</small>
        </h2>
        {procData ? (
          <ul>
            {procData.map((data) => (
              <li>{data}</li>
            ))}
          </ul>
        ) : selectedNation ? (
          <CircularProgress />
        ) : (
          "--"
        )}
      </Container>
    </>
  );
}

export default Players_by_nation;
