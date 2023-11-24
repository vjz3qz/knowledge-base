import React from "react";
import "../styles/FeatureBox.css";

const FeatureBox = ({ icon, title, description }) => (
  <div className="feature-box">
    <div className="feature-icon-wrapper">{icon}</div>
    <h2>{title}</h2>
    <p>{description}</p>
  </div>
);

export default FeatureBox;
