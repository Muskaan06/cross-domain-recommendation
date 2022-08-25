
# Cross-domain Recommendation System

## Table of Content
1. Our Proposed work
2. Dataset
3. Preprocessing
4. Algorithm
5. Testing
6. Result
7. References

## Our proposed work

Our work on CDR includes the following steps:
1. Proposed an approach for recommending items from one domain depending on user’s rating behaviour in another related domain (movies from books).
2. Designed an item-based collaborative filtering algorithm for predicting ratings in both single and cross-domain situations.
3. Performed genre mapping and successfully obtained cross domain recommendation for book and movie domains.
4. Tested our model using Amazon review datasets and compiled the results.
5. Analysed the results to verify if our cross-domain system is an improvement over single domain recommendation systems.

## Dataset

We have used 5-core and metadata from [Amazon Product Dataset](http://jmcauley.ucsd.edu/data/amazon/index.html) for testing. 

## Preprocessing

  a. Feature extraction:  
  
     We filtered all the available data to keep only the information that we would require for further processing.
     
     Columns in ‘5-Core’ data files before filtering : 
        ['overall', 'verified', 'reviewTime', 'reviewerID', 'asin', 'style', 'reviewerName', 'reviewText', 'summary', 'unixReviewTime','vote', 'image']
     Columns in ‘5-Core’ after feature selection : 
        [‘asin’, ‘reviewerID’, ‘reviewText’, ‘overall’]
     Columns in ‘metadata’ files before filtering : 
        ['category', 'tech1', 'description', 'fit', 'title',  'also_buy', 'tech2', 'brand', 'feature', 'rank', 'also_view', 'details',       
        'main_cat','similar_item', 'date', 'price', 'asin', 'imageURL',  'imageURLHighRes']
     Columns in ‘metadata’ after feature selection : 
        [‘asin’, ‘category’]
       
  b. Sentiment Analysis:
  
     To obtain the sentiment associated with each item, we perform sentiment analysis on the reviews given to each item by each user. In order to do this,    
     we use the VADER (Valence Aware Dictionary and sEntiment Reasoner) lexicon.
  
  c. One-hot encoding of categories:
  
     Next, we create columns for each genre category for both movies and books in their respective datasets and then perform one-hot encoding for every 
     item. We do this so that every item has a corresponding value of 1 in the genre to which it belongs and 0s in all the other genre category columns. 
     
  d. Intersection of Users:
  
    Now, we find an intersection from the set of users of both domains to identify the users who have rated at least one book and at least one movie.
    
  e. Reduction and Filtering of users:
  
     We now perform reduction and filtering on these datasets and create consolidated data frames of kindle and movie items. Here, we select the 
     intersection of common user datasets such that the users selected must have rated at least 20 books and at least 20 movies, and at most 500 movies and 
     at most 500 books. 
     
  f. Filtering of items for corresponding user:
  
    Once we have the reduced set of users who have rated a minimum and a maximum number of items, and rated items from both domains, we use this set of 
    users to filter out the items that have been rated by these resulting users in order to remove the items that have never been rated from our dataset. 
    Now, we merge both data frames as ‘item_final’ (movie and kindle item data) and ‘user_item_rating’(from kindle_common and movie_common data).
    
  g. Genre mapping:
  
    From the list of movie genres, we filtered out a list of classic genres that remain generally consistent across domains. This list was then used to     
    find 4 similar genres for each item and then we perform one-hot encoding for them as well. Then we took the unfiltered list of book genres and mapped 
    it to this list of classic genres to ensure we have all items mapped to a consistent set of features in order to be able to calculate item similarities 
    and perform recommendations thereafter.

    To find the list of similar genres we used the spaCy package which calculates the similarity between two-word vectors, and then takes the top results.

    This mapped dataset was then fed to the algorithm to obtain recommendation results from both domains i.e, movies and music for each user.
    (Note: If a new domain is added then we will also map it to the list of classic genres (here: movies))
    
    

## Algorithm

  1. Phase 1: For each of the domains, to make a recommendation, we need to compute the **item-item similarity** between all the items depending on their respective feature scores. Here, we have used cosine similarity for this. 
  2. Phase 2: We employ item-based collaborative filtering to predict ratings for all items in our dataset. Once the pairwise similarity s between all items is calculated, the final step is to generate recommendations for the target user U, based on their already rated items.
  3. Phase 3. After prediction of ratings, the user item matrix gets filled with these predicted ratings and once we have the predicted ratings for all items in our dataset, we can recommend items to each user depending on these ratings. 


## Testing

  1. Paratmeter tuning: The parameters are item similarity threshold and the manner in which test items are selected from the set of items. The variations  
  in these parameters are as follows : 
                                    !(/cross-domain-recommendation/images/parameter_tuning.png)
  2. Manner of Testing :
  
    Using the parameters defined above, we perform testing to obtain results which we use to draw conclusions regarding the efficacy of our model. Testing 
    on our model is conducted in the following ways :
    
    a.  Single Domain recommendation testing: movie to movie, book to book 
    b.  Cross-Domain recommendation testing: both to movie, both to book, both to both
    c.  Separated 5-6 rated items (actual ratings) from each user and kept those items as test items.
    d.  These now act as unrated items and we run our model to get the predicted ratings of those items
    e.  Calculated RMSE, MAE, Hit Ratio, precision, recall, f1 score based on the actual and predicted test ratings
    

## Results 
    
   After testing our algorithm on the available data and tuning the parameters to obtain results for varying test conditions, we can draw the following 
   inferences: 

    --> Top-rated items by users are predicted better than randomly rated items
    --> Keeping a higher threshold value for item-item similarity slightly improves overall results as the less similar items are removed from 
    consideration in the weighted average calculation
    --> Movie recommendation is most enhanced in CASE 1: Similarity Threshold → 0.5, Test Item Ratings → Random by ~11% when multi-domain recommendation is 
    used
    --> Book recommendation is most enhanced in CASE 2: Similarity Threshold → 0.8, Test Item Ratings → Random by ~2% when multi-domain recommendation is
    used
    --> Multi-Target CDR (both to both) gives the best results in all cases.
  

## References

1.  Zhu, Feng & Wang, Yan & Chen, Chaochao & Zhou, Jun & Li, Longfei & Liu, Guanfeng. (2021). *Cross-Domain Recommendation: Challenges, Progress, and Prospects.* 10.24963/ijcai.2021/639. 


2.  Kumar, Sudhanshu & Halder, Shirsendu & De, Kanjar & Roy, Partha. (2018). *Movie Recommendation System using Sentiment Analysis from Microblogging Data.* 


3.  Hutto, C.J. & Gilbert, E.E. (2014). *VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14).* Ann Arbor, MI, June 2014.
 
4. Honnibal, M., & Montani, I. (2017). *spaCy 2: Natural language understanding with Bloom embeddings, convolutional neural networks and incremental parsing.*

5. *Ups and downs: Modelling the visual evolution of fashion trends with one-class collaborative filtering - R.* He, J. McAuley, WWW, 2016

6. *Image-based recommendations on styles and substitutes* J. McAuley, C. Targett, J. Shi, A. van den Hengel SIGIR, 2015





