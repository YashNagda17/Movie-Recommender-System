import { BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import React from 'react'
import Homepage from './pages/homepage';
import Forms from './pages/forms';
import Results from './pages/results';
import DisplayPage from './pages/movie_disp';
import Navbar from "./navigation/Navbar";
import './App.css'; 
import "bootstrap/dist/css/bootstrap.min.css";




function App() { 
    
    return (
        
    <div>
        
        <Navbar marginTop="100"/>
        <p>&nbsp;</p>
        <Router>
            <Routes>
                <Route path = "/" element = { < Homepage  /> } />    
                <Route element = { < Forms /> } path = "/forms" />
                <Route element = { < Results /> } path = "/results" />
                <Route element = { < DisplayPage /> } path = "/title/:title" />
                         
            </Routes>
        </Router>
    
    
    </div>);
} export default App;