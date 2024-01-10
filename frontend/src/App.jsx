import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';

import './assets/NavigationBar.css'; // Archivo de estilos para la barra de navegación


function App() {
  const [products, setProducts] = useState([]);

  const fetchProducts = async (searchTerm) => {
    try {
      const url = `/api/product/filter?search_term=${searchTerm}`;
      const response = await fetch(url);

      if (!response.ok) {
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
      }

      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        throw new Error('Response is not in JSON format');
      }

      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };


  return (
    <div className="main-body">
      <NavigationBar onSearch={fetchProducts} />
      <br />
      <SearchResults results={products} />
    </div>
  );
}

function NavigationBar({ onSearch }) {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    onSearch(searchTerm);
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="d-flex align-items-center">
        <a className="navbar-brand" href="/">
          Etienda DAI
        </a>
        <form className="d-flex" method="get" onSubmit={handleSearch}>
          <input
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="form-control me-2"
            type="search"
            placeholder="Buscar"
            aria-label="Search"
          />
          <button className="btn btn-outline-success" type="submit">
            Buscar
          </button>
        </form>
      </div>
    </nav>
  );
}

NavigationBar.propTypes = {
  onSearch: PropTypes.func.isRequired,
};

function SearchResults({ results }) {
  return (
    <div>
      <h2>Resultados de la búsqueda:</h2>
      <ul>
        {results.map((result) => (
          <li key={result.id}>
            <h3>{result.title}</h3>
            <p>{result.description}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

SearchResults.propTypes = {
  results: PropTypes.array.isRequired,
};

export default App;
