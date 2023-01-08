import React,{useEffect, useState} from 'react'
import axios from 'axios'
import Card from 'react-bootstrap/Card';
import { useParams } from 'react-router-dom';
import InfiniteScroll from 'react-infinite-scroller';


const box = {
  fontSize: '23px',
  textAlign: 'center', 
  color : 'ivory',
  fontFamily: 'Arial',
}

const DisplayPage = ({tt}) => {
  const params = useParams()
  let title = params.title
  if (title==='') title=tt;
  
  
  
  
  const perPage = 3;
  const [lastObjectPosition , setLastObjectPosition ] = useState(0);
  const [dbmovies,setMovies] = useState([])
  const [movies, setLoadedmovies] = useState([]);
  
  useEffect(()=> {
    getdata()
  }, [] ) 

  let getdata = async() => {
    let response = await axios.get('http://127.0.0.1:8000?title=' + title)
    console.log('Response',response)
    setMovies(response.data)
    
  }

  const loadMovies = () => {
    setLoadedmovies(movies => {
        return movies.concat(dbmovies.slice(lastObjectPosition, lastObjectPosition+perPage))
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

  return(
    <div>
    <h4 style={box}> Search Results for "{title.substring(0, 1).toUpperCase() + title.substring(1).toLowerCase()}" </h4>
    
    <div className="movie-history">
    { dbmovies.length > 0 ?

    <InfiniteScroll
      pageStart={0}
      loadMore={loadMovies}
      hasMore={lastObjectPosition < dbmovies.length}
      loader={loader} >

      {movies.map((movie,index) =>
        <div>
          <div>

          </div>
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
                  
                    <a href = {movie.imdbid} target="_blank" rel="noreferrer">
                      <h3 class="btn mr-2">{movie.title}</h3>
                    </a>
                    

                    <div>
                      {movie.adult===false ?
                      <h6 className="mb-2 text-muted"> Child Safe</h6>
                      :
                      <h6 className="mb-2 text-muted">Adult</h6>
                      }
                    </div>
                    <p style = {{color : "#F4D03F"}}> {movie.genres.replace(/[^a-zA-Z ]/g, "")}</p>
                  
                    <p style={{fontFamily: "cursive"}} > {movie.overviews} </p>
                  
                </Card.Body>
                </Card>
              
              </div>
            }
            </div>
              
          )}
        </InfiniteScroll>
        : ''
        }
        </div> 
      </div>  
  )           
}
  
export default DisplayPage