import streamlit as st
import pickle
import numpy as np 
import pandas as pd

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
      data = pickle.load(file)
    return data

data = load_model()

model = data["model1"] 

def recommend_movies(user, num_recommended_movies, df, df1):
    
  user1 = str(user)
   
  lst=[]
  recommended_movies = []
  
  for m in df[df[user1] == 0].index.tolist():
    
    index_df = df1.index.tolist().index(m)
     
    predicted_rating = df1.iloc[index_df, df1.columns.tolist().index(user1)]
    op = df1.iloc[index_df, 0]
    recommended_movies.append((op, predicted_rating))

  sorted_rm = sorted(recommended_movies, key=lambda x:x[1], reverse=True)
  rank = 1
  for recommended_movie in sorted_rm[:num_recommended_movies]:
    
    lst.append((rank, recommended_movie[0], recommended_movie[1]))
    rank = rank + 1 
  return lst

def movie_recommender(user, num_neighbors, num_recommendation , model , df):
      
  number_neighbors = num_neighbors
  
  
  df1=df.copy()
  df2 = df.copy()
  df3 = df2.drop('title',axis=1)
  user1=str(user)
  
  user_index = df.columns.tolist().index(user1)
  distances, indices = model.kneighbors(df3, n_neighbors = 10)
  for m,t in list(enumerate(df.index)):
    if df.iloc[m, user_index] == 0:
      sim_movies = indices[m].tolist()
      movie_distances = distances[m].tolist()
    
      if m in sim_movies:
        id_movie = sim_movies.index(m)
        sim_movies.remove(m)
        movie_distances.pop(id_movie) 

      else:
        sim_movies = sim_movies[:num_neighbors-1]
        movie_distances = movie_distances[:num_neighbors-1]
           
      movie_similarity = [1-x for x in movie_distances]
      movie_similarity_copy = movie_similarity.copy()
      nominator = 0

      for s in range(0, len(movie_similarity)):
        if df.iloc[sim_movies[s], user_index] == 0:
          if len(movie_similarity_copy) == (number_neighbors - 1):
            movie_similarity_copy.pop(s)
          
          else:
            movie_similarity_copy.pop(s-(len(movie_similarity)-len(movie_similarity_copy)))
            
        else:
          nominator = nominator + movie_similarity[s]*df.iloc[sim_movies[s],user_index]
          
      if len(movie_similarity_copy) > 0:
        if sum(movie_similarity_copy) > 0:
          predicted_r = nominator/sum(movie_similarity_copy)
          
        else:
          predicted_r = 0
      else:
        predicted_r = 0
        
      df1.iloc[m,user_index] = predicted_r
      

  return recommend_movies(user,num_recommendation, df, df1)

def show_predict_page():
    st.title("Movie Recommender")
    st.write("""###need info""")
    
    UserId = (range(1,611,1))      
    No_of_recommendations = (5,10,20,50)

    UserId = st.selectbox("UserId", UserId)
    No_of_recommendations = st.selectbox("No of recommendations", No_of_recommendations)

    ok = st.button("Find Recommendations")
    if ok:
        X = np.array([[UserId, 10, No_of_recommendations]])
        X = X.astype(float)
        df = pd.read_csv("data.csv")
        Y = movie_recommender(UserId, 10, No_of_recommendations , model , df)
        
        st.header(f"List of Recommended Movies :")
        for u in range(No_of_recommendations):
            st.subheader(str(u+1)+ ' ' + str( Y[u][1])+ ' ' + str(Y[u][2]))



