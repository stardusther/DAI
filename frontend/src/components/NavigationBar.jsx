import React, {useState} from "react";
import PropTypes from "prop-types";

function NavigationBar({ onSearch }) {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    onSearch(searchTerm);
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light fixed-top">
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

export default NavigationBar;