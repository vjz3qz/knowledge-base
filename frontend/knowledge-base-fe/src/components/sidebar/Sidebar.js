import React from 'react';
import './Sidebar.css';
import { FiSearch, FiFileText, FiBox, FiUser, FiBarChart, FiAlertTriangle } from 'react-icons/fi';
import { Link } from 'react-router-dom'; // Import the Link component

const Sidebar = () => {
    return (
        <div className="sidebar">
            <div className="title">
                <FiUser size={30} />
                <h2>Trace AI</h2>
            </div>
            <div className="search-section">
                <FiSearch className="search-icon"/>
                <input type="text" placeholder="Search" className="search-bar" />
            </div>
            <div className="menu-items">
                <Link to="/dashboard"><FiBarChart className="menu-icon" />Dashboard</Link>
                <Link to="/chat"><FiFileText className="menu-icon" />Chat</Link>
                <Link to="/incident-reports"><FiAlertTriangle className="menu-icon" />Incident Reporting</Link>
                <hr />
                <Link to="/automations"><FiBox className="menu-icon" />Automations</Link>
                <Link to="/account-management"><FiUser className="menu-icon" />Account Management</Link>
            </div>
        </div>
    );
};

export default Sidebar;
