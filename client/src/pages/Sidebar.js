import React from "react";
import "./Sidebar.css";
import { FaHome, FaHeart, FaShoppingCart, FaClock, FaPlay, FaBookmark, FaCog } from "react-icons/fa";

const Sidebar = () => {
  const menuItems = [
    { name: "Home", icon: <FaHome /> },
    { name: "Favorite", icon: <FaHeart /> },
    { name: "Purchase", icon: <FaShoppingCart /> },
    { name: "Reminder", icon: <FaClock /> },
    { name: "Playlist", icon: <FaPlay /> },
    { name: "Bookmarks", icon: <FaBookmark /> },
    { name: "Settings", icon: <FaCog /> },
  ];

  return (
      <div className="sidebar">
          <div className="sidebar-header">
              <h1>
                  <span className="clip">Clip</span>
                  <span className="board">.board</span>
              </h1>
          </div>
          <ul className="menu-list">
              {menuItems.map((item, index) => (
                  <li key={index} className="menu-item">
                      {item.icon}
                      <span>{item.name}</span>
                  </li>
              ))}
          </ul>
      </div>
  );
};

export default Sidebar;
