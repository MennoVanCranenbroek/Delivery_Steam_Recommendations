import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open('pickles/Content_filtering.pkl', 'rb') as f1, open('pickles/Collaborative_filtering.pkl', 'rb') as f2, open('pickles/Full_Trainset.pkl', 'rb') as f3, open('pickles/Indices.pkl', 'rb') as f4:
    cosine_similarities = pickle.load(f1)

    collaborative_similarities = pickle.load(f2)

    trainset = pickle.load(f3)

    indices = pickle.load(f4)




games = pd.read_csv("../data/clean_game_data.csv")

def recommend(game_titles,df):

    titles = game_titles.split(',')
    
    
    return weighted_recommend_on_library(titles)


def weighted_recommend_on_library(titles):
    all_recommendations = {}
    
    for title in titles:
           
        # Call the recommend_content() function with the current title
        recommended_content = weighted_recommend_content(title)
            
        # Remove titles that the user already has
        recommended_content = {item:score for item, score in recommended_content if item not in titles}

            
        # Unpack the recommended_content tuple into separate variables
        for recommended_item, score in recommended_content.items():
        
            # Add the recommendation and similarity score to all_recommendations
            if recommended_item in all_recommendations:
                all_recommendations[recommended_item] += score
            else:
                all_recommendations[recommended_item] = score

    # Sort the recommendations by their total score and extract the titles
    sorted_recommendations = sorted(all_recommendations.items(), key=lambda x: x[1], reverse=True)        
              

    return sorted_recommendations[:10]
    
def weighted_recommend_content(title, cosine_sim = cosine_similarities, knn_sim = collaborative_similarities):

    # Cosine recommendations
    content_similar_scores = recommend_content(title, cosine_sim)

    # KNN recommendations
    knn_similar_scores = get_knn_similar(title, knn_sim)
    
    #remove the games already owned
    content_similar_scores = {item:score for item, score in content_similar_scores.items() if item != title}
    # knn_similar_scores = {item:score for item, score in knn_similar_scores.items() if item != title}

    # content_similar_scores = {item:score for item, score in content_similar_scores.items() if score >= 0.1}
    # knn_similar_scores = {item:score for item, score in knn_similar_scores.items() if score >= 0.1}

    # COMBINE STUFF
    weighted_scores = {}
    
    for key, value in content_similar_scores.items():
        if key == "Warframe":
            print(len(content_similar_scores))
            knn_value = knn_similar_scores[key]
            weighted_scores[key] = value * 0.15 + knn_value * 0.85
        else:
            knn_value = knn_similar_scores[key]
            weighted_scores[key] = value * 0.15 + knn_value * 0.85
        

    sorted_weighted_scores = sorted(weighted_scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_weighted_scores[1:21]

def recommend_content(title, sim_matrix = cosine_similarities):
    # get index for our game
    idx = indices[title]
    # get pairwise similarity scores of all games w.r.t to our game
    sim_scores = list(enumerate(sim_matrix[idx]))
    # sort scores based on similarity
    sorted_sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # make a dictionary with title as key and score as value
    content_similar_scores = {indices.index[i[0]]: i[1] for i in sorted_sim_scores[1:]}
    return content_similar_scores

def get_knn_similar(title, knn_sim = collaborative_similarities):
    '''Get k nearest neighbors using the similarity matrix'''
    
    idx = get_innerid(title)
    
    # get pairwise similarity scores of all games w.r.t to our game
    sim_scores = list(enumerate(knn_sim[idx]))
    
    # sort scores based on similarity
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # make dictionary with title as key and similarity score as value
    similar_games = {get_title(i[0]): i[1] for i in sorted_scores[1:]}

    return similar_games

# function that takes game title and returns the knn model inner id
def get_innerid(title):
    appid = games[games['title'] == title]['id'].values[0]
    inner_id = trainset.to_inner_iid(title)
    return inner_id

# function that takes knn model innerid and returns the game title
def get_title(inner_id):
    steam_id = trainset.to_raw_iid(inner_id)
    title = games[games['title'] == steam_id].iloc[0]['title']
    return title

