import {Avatar, List, ListItem, ListItemIcon, ListItemText} from "@mui/material";
import FlagIcon from '@mui/icons-material/Flag';
import React from "react";
import {Marker, Popup} from 'react-leaflet';
import {icon as leafletIcon, point} from "leaflet";

const LIST_PROPERTIES = [
    {"key": "nation", label: "Nation", Icon: FlagIcon}
];

export function ObjectMarker({geoJSON}) {
    const properties = geoJSON?.properties
    const {id, name} = properties || {};
    const imgUrl = process.env.PUBLIC_URL + '/marker_icon.jpg';
    const coordinates = geoJSON?.geometry?.coordinates || [];
    const markerIcon = imgUrl
  ? leafletIcon({
      iconUrl: imgUrl,
      iconRetinaUrl: imgUrl,
      iconSize: point(50, 50),
    })
  : null;

    console.log("imgUrl:", imgUrl);
    console.log("name:", name);
    console.log("coordinates:", coordinates);


    return (
        <Marker
            position={coordinates}
            icon={markerIcon}
        >
            <Popup>
                <List dense={true}>
                    <ListItem>
                        <ListItemIcon>
                            <Avatar alt={name} src={imgUrl}/>
                        </ListItemIcon>
                        <ListItemText primary={name}/>
                    </ListItem>
                    {
                        LIST_PROPERTIES
                            .map(({key, label, Icon}) =>
                                <ListItem key={key}>
                                    <ListItemIcon>
                                        <Icon style={{color: "black"}}/>
                                    </ListItemIcon>
                                    <ListItemText
                                        primary={<span>
                                        {properties[key]}<br/>
                                        <label style={{fontSize: "xx-small"}}>({label})</label>
                                    </span>}
                                    />
                                </ListItem>
                            )
                    }

                </List>

            </Popup>
        </Marker>
    )
}