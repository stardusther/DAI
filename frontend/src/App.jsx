import React, { useEffect, useState } from 'react';
import NavigationBar from './components/NavigationBar.jsx';
import SearchResults from './components/SearchResults.jsx'

import './assets/NavigationBar.css'; // Archivo de estilos para la barra de navegación


function App() {
  const [products, setProducts] = useState([]);

  const fetchProducts = async (searchTerm) => {
    try {
      const url = `http://localhost:8000/api/product/filter?search_term=${searchTerm}`;
      const response = await fetch(url);
      const data = await response.json();
      setProducts(data);
    } catch (error) {
      console.error('Error fetching products:', error.message);
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



export default App;
