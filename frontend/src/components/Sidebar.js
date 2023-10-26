import React from 'react';
import '../styles/Sidebar.css';
import { FiSearch, FiFileText, FiInbox, FiUser} from 'react-icons/fi';
import { Link } from 'react-router-dom'; 

const Sidebar = () => {
    return (
        <div className="sidebar">
            <div className="title">
                <h2>Trace AI</h2>
            </div>
            <div className="menu-items">
                <Link to="/document-search"><FiSearch className="menu-icon" />Document Search</Link>
                <Link to="/document-chat"><FiFileText className="menu-icon" />Document Chat</Link>
                <Link to="/incident-reports"><FiInbox className="menu-icon" />Operator Reporting</Link>
                <hr />
                <Link to="/account-management"><FiUser className="menu-icon" />Account Management</Link>
            </div>
        </div>
    );
};

export default Sidebar;
