import React,{useEffect, useState,} from 'react'
import axios from 'axios'
import InfiniteScroll from 'react-infinite-scroller';
import Card from 'react-bootstrap/Card';
import "bootstrap/dist/css/bootstrap.min.css";
import { useLocation } from "react-router";

const Results = () => {
  
  const perPage = 3;
  const [lastObjectPosition , setLastObjectPosition ] = useState(0);
  const [movies, setLoadedmovies] = useState([]);
  const [dbmovies,setMovies] = useState([]);
  const [sending_array,set_sending_array] = useState([]);
  console.log(1);
  const location = useLocation()
  const { from } = location.state
  console.log(2);
  
  // console.log(data);
  // console.log(data.state);
  //console.log(data.state.sending_array);
  // if (props.location!==undefined) {
  //   console.log(5)
  //   set_sending_array(props.location.state.sending_array)
  //   console.log(sending_array)}

  // useEffect(()=> {
  //     console.log(1)
  //     getdata()
  //   }, [] ) 
    
  //   let getdata = async() => {

  //     console.log(sending_array)
  //     if (sending_array.length===0) return
  //     await axios ({
  //       method : 'post',
  //       url : 'http://127.0.0.1:8000/form/',
  //       data : sending_array,
  //     }).then((response)=> {
  //       console.log(2)        
  //       setMovies(response.data)  
  //     })    
  // }

 

  return (
    <div>
        
        <h2>
          Our Recommendations!
        </h2>
        
    
     
      
    </div>
  )
}

export default Results