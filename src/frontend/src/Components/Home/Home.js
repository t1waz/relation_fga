import React, { useState } from 'react';
import Sidebar from './Sidebar';
import Table from './Table'

const data = [
    {
        projectName: 'Store Name',
        region: 'REGION',
        ramSize: 'RAM SIZE',
        mgVersion: 'v2.14.0',
    },
    {
        projectName: 'Projekt Alpha',
        region: 'Europa (Frankfurt)',
        ramSize: '4 GB RAM',
        mgVersion: 'v2.14.0',
    },
];


export function Home() {
    const [isSidebarOpen, setSidebarOpen] = useState(false);

    // Ta funkcja zmienia stan sidebara
    const toggleSidebar = () => {
        setSidebarOpen(!isSidebarOpen);
    };

    return (
        <div className="home-layout">
            <Sidebar isOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
            <div className={`content ${isSidebarOpen ? '' : 'closed'}`}>
                <div className={`table-container ${isSidebarOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
                    <Table data={data} />
                </div>
                <button className="add-store-button">Add Store</button>
            </div>
        </div>
    );
}