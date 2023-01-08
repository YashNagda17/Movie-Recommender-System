import React,{useEffect, useState} from 'react'
import axios from 'axios'
import Select from 'react-select';
import {FaStar} from 'react-icons/fa';
//import {Link } from "react-router-dom";
import InfiniteScroll from 'react-infinite-scroller';
import Card from 'react-bootstrap/Card';

const Forms = () => {
  
  const perPage = 3;
  const [Rt,set_rated_mov] = useState([]);
  const [sending_array,set_sending_array] = useState([]);
  const [rating, setRating] = useState(0);
  const [hover, setHover] = useState(0);
  const [mov_select,set_mov] = useState(useState({'value':-1,'label':''}));
  const [options,setOptions] = useState([]);  
  const [ratings,setRatings] = useState([]);
  const [dbmovies,setMovies] = useState([]);
  const [results,set_results] = useState([]);
  const [lastObjectPosition , setLastObjectPosition ] = useState(0);
  const [movies, setLoadedmovies] = useState([]);

  useEffect(()=> {
    getdata()
  }, [] ) 
  
  let getdata = async() => {
  let response = await axios.get('http://127.0.0.1:8000/not/')
  setMovies(response.data)   
  }
  

  useEffect(() => {
    if(dbmovies.length>0) {
      
      setOptions  (options=>{ 
        
        dbmovies.forEach(movie=> {
          
          var dct = {value:movie.movieId, label:movie.title}
          if (!(options.indexOf(dct)) > -1){
            options.push(dct);
          }
          })
        
        return options;
        })
      }
  },[dbmovies])
    
  const mystyle = {
    color: "white",
    backgroundColor: "DodgerBlue",
    padding: "5px",
    fontFamily: "Arial",
    textAlign: "center",
  };

  const styleObj = {
    fontSize: 20,
    fontFamily: "Arial",
    color: "chartreuse",
    fontStyle: 'italic',
  }
  
  const loadMovies = () => {
    setLoadedmovies(movies => {
        return movies.concat(results.slice(lastObjectPosition, lastObjectPosition+perPage))
    });
    
    setLastObjectPosition(currentValue => {
        return currentValue + perPage
    })
  }
  
  const loader = (
    <div key="loader" className="loader">
      Loading ...
    </div>
  );

  const SendMovData = async () => {
    if (sending_array.length===0) return
    await axios ({
      method : 'post',
      url : 'http://127.0.0.1:8000/form/',
      data : sending_array,

    }).then((response)=> {
      set_results(response.data)
      console.log(results)
    })

  }
  
  
  return (
    
    <div>
      { results.length===0 ?
          <div>
            <h2>
          Which of the Following Movies are you fan of?
            </h2>
            <div>
              <form>
              <Select options={options} 
                  autoFocus={true}
                  defaultMenuIsOpen={true}
                  size = "30"
                  onChange={(e) => {
                    set_mov(e)
                  }}
                />
                      
          
              
                
                <div className="star-rating">
            {[...Array(5)].map((star, index) => {
              index += 1;
              return (
              
                <label>
                  <input name="rating" 
                  type="radio" value={index} 
                  onClick = {()=> {
                    setRating(index)
                    
                    if (mov_select.label===undefined) return
                    let d = Rt.indexOf(mov_select.label)
                    if (d > -1)
                    {
                      
                      ratings[d].rating = index
                      sending_array[d].rating = index
                      
                    }
                    else 
                      {setRatings(prevRat=>{
                        return [...prevRat,{title: mov_select.label, rating : index}]
                      })

                      set_sending_array(prevRat=>{
                        return [...prevRat,{title: mov_select.value, rating : index}]
                      })

                      set_rated_mov(prevRat=>{
                        
                        return [...prevRat, mov_select.label]
                      })}
                    
                    
                  }}

                  />

                  <FaStar size = "40" className="star"
                  color = {index <= (hover || rating) ? "#ffc107": "#e4e5e9"}
                  onMouseEnter = {()=> setHover(index)}
                  onMouseLeave = {()=> setHover(null)}
                  />
                </label>  
              );})}
        
            </div>        
          </form> 
              
              <p> &nbsp; </p>
              <input type="submit" value="Get Recommendations!" onClick={SendMovData} />

              <p> &nbsp; </p>
              <h4 style={mystyle}> Your Rated Movies : {ratings.length}</h4>
              <ul >
              
              {ratings.map(mov=> 
                <div>

                  <li style={styleObj}> {mov.title + ' : '}     {mov.rating}/5 </li>
                  
                </div>
              )}
              </ul>
            </div>
          </div>

            :

            <div>
             <h2> Our Recommendations!</h2>
              
          <InfiniteScroll
            pageStart={0}
            loadMore={loadMovies}
            hasMore={lastObjectPosition < results.length}
            loader={loader} >
      
      
            {movies.map((movie,index) =>
              <div>
            
          
          
                {index>2 && 
                <div>
                <Card class="card mr-2" style={{ width: '31.2rem' }} >
                  <div >
                    {movie.backdrop==="" ?
                      <Card.Img variant="top" style={{ objectFit: 'contain', marginTop: '10px' }} src={"https://images.pexels.com/photos/20787/pexels-photo.jpg?auto=compress&cs=tinysrgb&h=350"} />
                      :
                      <Card.Img variant="top" style={{ objectFit: 'contain', marginTop: '10px' }}src={"https://image.tmdb.org/t/p/w500/" + movie.backdrop} />
                    }
                  </div>

                    <Card.Body style={{ textAlign: 'center' }}>
                      
                      <a href = {movie.imdbid} target="_blank" rel="noreferrer" >
                        <h3 class="btn mr-2">{movie.title} </h3>
                        
                      </a>
                        

                      <div>
                        {movie.adult===false ?
                        <h6 className="mb-2 text-muted"> Child Safe</h6>
                        :
                        <h6 className="mb-2 text-muted">Adult</h6>
                        }
                        </div>
                      <p style = {{color : "#F4D03F"}}> {movie.genres.replace(/[^a-zA-Z ]/g, "")}</p>
                      <p></p>
        
                      <p style={{fontFamily: "cursive"}} > {movie.overviews} </p>
                      
                        
                  
                  </Card.Body>
                  </Card>
                  
                </div>
              }
              </div>
                  
                
              )}
              </InfiniteScroll>
            </div> 
      }

    </div>
      
    
  )
}


export default Forms