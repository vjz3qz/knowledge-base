import React from "react";
import "../styles/DocumentCard.css";

function DocumentCard(props) {
  return (
    <div className="card" onClick={props.onClick}>
      <h2 className="style">{props.documentName}</h2>
      <p card="date">{props.date}</p>
      <p card="summary">{props.summary}</p>
    </div>
  );
}

export default DocumentCard;
