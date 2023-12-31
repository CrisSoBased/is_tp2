import Nations from "../Tables/Nations";
import Clubs from "../Tables/Clubs";
import Players from "../Tables/Players";

const Sections = [

    {
        id: "players",
        label: "Players",
        content: <Players/>
    },

    {
        id: "clubs",
        label: "Clubs",
        content: <Clubs/>
    },

    {
        id: "nations",
        label: "Nations",
        content: <Nations/>
    }

];

export default Sections;