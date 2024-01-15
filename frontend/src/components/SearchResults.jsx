import PropTypes from "prop-types";
import React from "react";
import '../assets/SearchResults.css';

function getColorClass(category) {
  switch (category.toLowerCase()) {
    case 'men\'s clothing':
      return 'bg-primary'; // Puedes cambiar esto a otro color según tu preferencia
    case 'women\'s clothing':
      return 'bg-success';
    case 'electronics':
      return 'bg-warning';
    case 'jewelery':
      return 'bg-danger';
    default:
      return 'bg-secondary';
  }
}

function SearchResults({ results }) {
  try {
    if (!results || results.length === 0) {
      return <div id="no-result-div"><p id="no-results">No hay resultados.</p></div>;
    }

    return (
        <div id="result-div">
          <h3 id="resultado-title">Resultados de la búsqueda:</h3>
          <ul className="list-group">
            {results.map(({ title, category, description }, index) => (
              <li key={index} className="list-group-item">
                <h4 className="title">{title}</h4>
                <p>
                  <span className={`badge ${getColorClass(category)}`}>{category}</span>
                </p>
                <p>
                  {description}
                </p>
              </li>
            ))}
          </ul>
        </div>
      );
  } catch (error) {
    console.error('Error al procesar los resultados:', error);
    return <p>Error al procesar los resultados.</p>;
  }
}


SearchResults.propTypes = {
  results: PropTypes.array.isRequired,
};

export default SearchResults;