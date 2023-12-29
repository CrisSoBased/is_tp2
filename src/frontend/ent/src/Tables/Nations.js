import {useEffect, useState} from "react";
import {
    CircularProgress,
    Pagination,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";

function Nations() {

    const PAGE_SIZE = 10;
    const [page, setPage] = useState(1);
    const [procData, setProcData] = useState(null);
    const [maxDataSize, setMaxDataSize] = useState(null);    

    useEffect(() => {
      console.log("Fetching data...");
      fetch(`http://localhost:20001/nations`)
        .then((response) => response.json())
        .then((data) => {
          setMaxDataSize(data.length)
          setProcData(data);
        })
        .catch((error) => console.error("Error fetching data:", error));
    }, []);

    return (
        <>
            <h1>Nations</h1>

            <TableContainer component={Paper}>
                <Table sx={{minWidth: 650}} aria-label="simple table">
                    <TableHead>
                        <TableRow>
                            <TableCell>Nation Name</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {
                            procData ?
                                procData.map((row) => (
                                    <TableRow
                                        key={row.id}
                                        style={{background: "gray", color: "black"}}
                                    >
                                        <TableCell component="td" scope="row">
                                            {row.name}
                                        </TableCell>
                                    </TableRow>
                                ))
                                :
                                <TableRow>
                                    <TableCell colSpan={3}>
                                        <CircularProgress/>
                                    </TableCell>
                                </TableRow>
                        }
                    </TableBody>
                </Table>
            </TableContainer>
            {
                maxDataSize && <div style={{background: "black", padding: "1rem"}}>
                    <Pagination style={{color: "black"}}
                                variant="outlined" shape="rounded"
                                color={"primary"}
                                onChange={(e, v) => {
                                    setPage(v)
                                }}
                                page={page}
                                count={Math.ceil(maxDataSize / PAGE_SIZE)}
                    />
                </div>
            }


        </>
    );
}

export default Nations;
