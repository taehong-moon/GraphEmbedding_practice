<h1> Random Walks Approaches </h1>


<h2> Why Random Walk? </h2>

<h3> 1. Expressivity </h3>

- Flexible stochastic definition of node similarity that incorporates both local and higher order neighborhood information.  

<h3> 2. Efficiency </h3>

- Do not need to consider all node pairs when training: only need to consider pairs that co-occur on random walks.  


<h2> Approaches about capturing the graph structure </h2>

- In order to do Random-Walk approach, we have to decide __the length of each walk__ ,__the number of generating random walk__,  
  and __the policy that traverse the neighborhood nodes__. Before making a decision about those factors, we have to make an reasonable  
  assumption about graph structure. For example....
  
  - __t-SNE__ case 
  
    - In t-SNE, they assume that neighborhood nodes will follow Gaussian distribution and distinguish between dense region  
      and sparse region by controlling variance of Gaussian distribution. Therefore, they introduce a concept named, "Perplexity."
    
  - __DeepWalk__ case
  
    - In DeepWalk, they observe that the frequency which vertices appear in the short random walks wil also follow a power-law  
      distribution if the degree distribution of a connected graph follows a power law.(i.e. ___scale-free___)
  
  - __Node2Vec__ case
  
    - Comparing with previous two approaches, they do not make an assumption about node's distribution. However, they design a  
      flexible objective that is not tied to a particular sampling strategy and provides parameters to tune the search space.

- __In conclusion, we can intuitively get two principles from above papers.__ 

    1. Determining the length of each walk and the number of generating a random walk, etc is the secondary part of algorithm.  
       The most critical issue in Random_Walk_Approach is to decide a proper policy to traverse another node.
    
    2. When we consider the learning the continuous features, it is more tractable if we assume a specific distribution about  
       nodes or edges. However, it may be intractable to optimize the objective function that we decide a policy regardless of  
       distribution.
       
. 
