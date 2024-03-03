import React from 'react';
import Tile from './Tile';
import './Table.css';

const Table = ({ data }) => {
    return (
        <div className="grid-table">
            <div className="grid-header">
                <div className="header-item">STORE NAME</div>
                <div className="header-item">TYPE COUNT</div>
                <div className="header-item">RELATION COUNT</div>
                <div className="header-item">TUPLE COUNT</div>
            </div>

            {data.map((item) => (
                <Tile
                    key={item.id}
                    projectName={item.projectName}
                    region={item.region}
                    ramSize={item.ramSize}
                    mgVersion={item.mgVersion}
                    active={item.active}
                />
            ))}
        </div>
    );
};

export default Table;
