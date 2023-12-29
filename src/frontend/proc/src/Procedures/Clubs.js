import React, {useEffect, useState} from "react";
import {CircularProgress, Container} from "@mui/material";


function Clubs() {
    const [procData, setProcData] = useState(null);
    // const [gqlData, setGQLData] = useState(null);

    useEffect(() => {
      console.log("Fetching data...");
      fetch(`http://localhost:20004/api/clubs`)
        .then((response) => response.json())
        .then((data) => {
          setProcData(data);
        })
        .catch((error) => console.error("Error fetching data:", error));
    }, []);
  

    return (
        <>
            <h1>Clubs</h1>

            <Container maxWidth="100%" sx={{
                backgroundColor: 'info.dark',
                padding: "2rem",
                marginTop: "2rem",
                borderRadius: "1rem",
                color: "white"
            }}>
                <h2>Results <small>(PROC)</small></h2>
                {
                    procData ?
                        <ul>
                            {
                                procData.map(data => <li>{data}</li>)
                            }
                        </ul> :
                        <CircularProgress/>
                }
                {/* <h2>Results <small>(GraphQL)</small></h2>
                {
                    gqlData ?
                        <ul>
                            {
                                gqlData.map(data => <li>{data.team}</li>)
                            }
                        </ul> :
                        <CircularProgress/>
                } */}
            </Container>
        </>
    );
}

export default Clubs;
