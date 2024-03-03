import React from 'react';
import './Tile.css';

const Tile = ({ projectName, region, ramSize, mgVersion, active }) => {
    return (
        <div className="tile">
            <div>{projectName}</div>
            <div>{region}</div>
            <div>{ramSize}</div>
            <div>{mgVersion}</div>
        </div>
        // <div className="tile tile-content">
        //     <div><p>{projectName}</p></div>
        //     <div><p>{region}</p></div>
        //     <div><p>{ramSize}</p></div>
        //     <div><p>{mgVersion}</p></div>
        // </div>
    );
};

export default Tile;
