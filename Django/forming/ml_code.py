from scipy import spatial
from math import sqrt
import pandas as pd
import os

        

class Predictions():
    
    def __init__(self,user_given_rat):
        #self.user = userId
        BASE_D = os.path.dirname(os.path.dirname(__file__))

        self.ratings = pd.read_csv(os.path.join(os.path.dirname(BASE_D), "ratings_pred.csv"))
        self.movies = pd.read_csv(os.path.join(os.path.dirname(BASE_D), "movies_pred.csv"))
        self.user_giv = user_given_rat  #dct to store current user ratings
        self.seen = list(user_given_rat.keys()) # lst to store all seen movies of user
        self.best = list(user_given_rat.keys()) # lst to store best movies of user 
        self.mov_score = None  # dct To store movie ratings calculated, as per movie
        self.user_score = None #dct to store movie ratings based on users
        self.fin_scores = None #dct to store final scores
        #self.user_rat = None #dct to store ratings of top movies  
            
    def distance(self, a, b):
        lstA = a['genres_vector'][1:-1]
        lstB = b['genres_vector'][1:-1]
        genresA = []
        genresB = []
        for i in lstA:
            if i=='0':
                genresA.append(0)
            elif i=='1':
                genresA.append(1)
                
        for i in lstB:
            if i=='0':
                genresB.append(0)
            elif i=='1':
                genresB.append(1)
            
        score = 1-spatial.distance.cosine(genresA, genresB)
        if a['Collection'] == b['Collection']:
            score+=1
        return score
    
    def Calculate_Movies(self):
        dct = {}       
        med = 0
        lst = []

        for i in self.user_giv:
            lst.append(self.user_giv[i])
        
        if (len(lst)>0):
            med = (lst[len(lst)//2]//1)
        
        self.best = []
        for i in self.user_giv:
            if self.user_giv[i]>med:
                self.best.append(i)

        best_data = self.movies.loc[self.movies['movieId'].isin(self.best)]
        for index, row in self.movies.iterrows():
            if row['movieId'] not in self.seen:                
                score = ((row['Average_Vote_TMDB']*row['Vote_Count_TMDB']) + row['Popularity'])
                for index2,row2 in best_data.iterrows():
                    score += self.distance(row,row2)*(self.user_giv[row2['movieId']]/5)
                dct[row['movieId']] = score
        self.mov_score = dct
    
    
    
    def user_recommendation(self):
        dct = {}
        #dk = self.ratings[self.ratings["userId"]==self.user]
        users = self.ratings[self.ratings['movieId'].isin(self.seen)]
        
        subset = users.groupby(['userId'])
        subset = sorted(subset,  key=lambda x: len(x[1]), reverse=True)
        subset = subset[0:100]
        
        pearsonCorDict = {}
        users = users.sort_values(by='movieId')        
        for name, group in subset:
            group = group.sort_values(by='movieId')
            n = len(group) 
            temp = users[users['movieId'].isin(group['movieId'].tolist())]    
            tempRatingList = temp['rating'].tolist()
            tempGroupList = group['rating'].tolist()
            
                
            Sxx = sum([i**2 for i in tempRatingList]) - pow(sum(tempRatingList),2)/float(n)
            
            Syy = (sum([i**2 for i in tempGroupList]) - pow(sum(tempGroupList),2))/float(n)
            Sxy = sum( i*j for i, j in zip(tempRatingList, tempGroupList)) - sum(tempRatingList)*sum(tempGroupList)/float(n)
            
            if (Sxx*Syy) != 0:
                pearsonCorDict[name] = -Sxy/sqrt(abs(Sxx))
            else:
                pearsonCorDict[name] = 0
        
        pearsonDF = pd.DataFrame.from_dict(pearsonCorDict, orient='index')
        pearsonDF.columns = ['similarityIndex']
        pearsonDF['userId'] = pearsonDF.index
        topUsers = pearsonDF.sort_values(by='similarityIndex', ascending=False)[0:50]
        
        user_ratings = topUsers.merge(self.ratings, left_on='userId', right_on='userId', how='inner')
        user_ratings['weightedRating'] = user_ratings['similarityIndex']*user_ratings['rating']
        recommend = user_ratings.groupby('movieId').sum()[['similarityIndex','weightedRating']]
        
        recommend.columns = ['sum_similarityIndex','sum_weightedRating']
        recommend['recommendation score'] = recommend['sum_weightedRating']/recommend['sum_similarityIndex']
        recommend = recommend.drop(['sum_similarityIndex','sum_weightedRating'],axis = 1)
        #print(recommend)
        recommend = recommend.fillna(0)
        
        recommend = recommend.sort_values(by='recommendation score', ascending=False)
        
        for index,row in recommend.iterrows():
            dct[index] = row[0]/5
            
        self.user_score = dct
        
        
              
    
    def predict_movies(self):
        
        fin_arr = []
        
        for i in self.mov_score:
            score = self.mov_score[i]
            if i in self.user_score:
                
                
                score += (self.user_score[i])
                
            fin_arr.append([i,score])
        fin_arr = sorted(fin_arr, key=lambda x:x[1],reverse=True)
        self.final_scores = fin_arr
        
        out = []
        for i in range(100):
            out.append(fin_arr[i][0])
            
        
        return out
        
    
    
        
    
    def run(self):
               
        self.Calculate_Movies()
        self.user_recommendation()
        return self.predict_movies()
        
       

   


