from forming.models import movies
import csv
import requests



def run():
    with open('forming_data.csv',encoding="utf8") as file:
        reader = csv.reader(file)
        next(reader)  

        movies.objects.all().delete()
        api_key = "" ##Get this key from tmdb api
        c = 0
        for row in reader:
            
            overview = ''
            imdb = "https://www.imdb.com/"
            imdb1 = "https://www.imdb.com/title/tt0" + row[2]
            tmdb1 = str="https://api.themoviedb.org/3/find/tt0{}?api_key={}&external_source=imdb_id".format(row[2],api_key)
            
            imdb2 = "https://www.imdb.com/title/tt" + row[2]
            tmdb2="https://api.themoviedb.org/3/find/tt{}?api_key={}&external_source=imdb_id".format(row[2],api_key)
            
            k = requests.get(tmdb1).json()
            k1 = k['movie_results']
            k2 = k['tv_results']
            k3 = k['tv_episode_results']
            k4 = k['tv_season_results']
            
            if (k1!=[]):
                imdb = imdb1
                overview = k1[0]['overview']
            
            elif (k2!=[]):
                imdb = imdb1
                overview = k2[0]['overview']

            elif (k3!=[]):
                imdb = imdb1
                overview = k3[0]['overview']
            
            elif (k4!=[]):
                imdb = imdb1
                overview = k4[0]['overview']
            
            else:
                k = requests.get(tmdb2).json()
                k1 = k['movie_results']
                k2 = k['tv_results']
                k3 = k['tv_episode_results']
                k4 = k['tv_season_results']
                
                if (k1!=[]):
                    imdb = imdb2
                    overview = k1[0]['overview']
            
                elif (k2!=[]):
                    imdb = imdb2
                    overview = k2[0]['overview']

                elif (k3!=[]):
                    imdb = imdb2
                    overview = k3[0]['overview']
            
                elif (k4!=[]):
                    imdb = imdb2
                    overview = k4[0]['overview']
    
                
            

            genre = row[5] + "|"
            genre = list(genre.split("|"))[:-1]   
            print(c)
            c+=1
            movie = movies(movieId=row[0],
                        title=row[1],
                        imdbid = imdb,
                        adult = row[3],
                        backdrop = row[4],
                        genres = genre,
                        overviews = overview
                        )
            movie.save()