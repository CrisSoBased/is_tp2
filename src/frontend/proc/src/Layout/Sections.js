import Clubs from "../Procedures/Clubs";
import Players_from_portugal from "../Procedures/Players_from_portugal";
import Players_cm_from_france from "../Procedures/Players_cm_from_france";
import Players_by_nation from "../Procedures/Players_by_nation";

const Sections = [

    {
        id: "clubs",
        label: "Clubs",
        content: <Clubs />
    },
    {
        id: "players_from_portugal",
        label: "Players_from_portugal",
        content: <Players_from_portugal />
    },
    {
        id: "players_cm_from_france",
        label: "Players_cm_from_france",
        content: <Players_cm_from_france />
    },
    {
        id: "players_by_nation",
        label: "Players_by_nation",
        content: <Players_by_nation />
    }

];

export default Sections;