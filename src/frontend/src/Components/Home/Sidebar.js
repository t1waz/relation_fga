// Sidebar.js
import React, { useState } from 'react';
import './Home.css';
import { FaProjectDiagram } from "react-icons/fa";
import { MdStackedLineChart } from "react-icons/md"; // Przykładowa zamiana na dostępną ikonę
import { VscAccount } from "react-icons/vsc";
import { IoDocumentsOutline } from "react-icons/io5"; // Przykładowa zamiana na dostępną ikonę
import { RiLogoutBoxRLine } from "react-icons/ri";
import logo_big from "../../Assets/RelFGA-logo.png"; // Przykładowa zamiana na dostępną ikonę

const Sidebar = ({ isOpen, toggleSidebar }) => {

    return (
        <div className={`sidebar ${isOpen ? 'open' : 'closed'}`} onClick={toggleSidebar}>
            <div className='logo'>
                <img src={logo_big} alt=""/>
            </div>
            <div className="sidebar-content" onClick={e => e.stopPropagation()}>
                {/* Linki wewnątrz sidebar-content nie będą już propagować kliknięcia do rodzica */}
                <a href="#" className="sidebar-item"><FaProjectDiagram/><span>Stores</span></a>
                <a href="#" className="sidebar-item"><MdStackedLineChart/><span>Snapshots</span></a>
                <a href="#" className="sidebar-item"><VscAccount/><span>Account</span></a>
                <a href="#" className="sidebar-item"><IoDocumentsOutline/><span>Documentation</span></a>
                <a href="#" className="sidebar-item"><RiLogoutBoxRLine/><span>Log Out</span></a>
            </div>
        </div>
    );
};

export default Sidebar;