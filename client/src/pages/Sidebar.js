import React, { useState } from "react";
import "./Sidebar.css";

const Sidebar = ({ categories, onFilter }) => {
  const [isActive, setIsActive] = useState(false); // Estado para controlar el despliegue de categorías

  const toggleCategories = () => {
    setIsActive(!isActive); // Alterna el estado entre true y false
  };

  const sortedCategories = [...categories].sort((a, b) =>
    a.name.localeCompare(b.name)
  );

  return (
    <div className="sidebar">
      {/* Contenedor de categorías */}
      <div className={`categories ${isActive ? "active" : ""}`}>
        <button className="categories-toggle" onClick={toggleCategories}>
          Categories
        </button>
        <ul className={`category-list ${isActive ? "active" : ""}`}>
          {sortedCategories.map((category) => (
            <li
              key={category.id}
              className="category-item"
              onClick={() => onFilter("category", category.name)}
            >
              {category.name}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default Sidebar;
