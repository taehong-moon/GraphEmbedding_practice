<h1> Node2Vec </h1>

<h2> 1. Theoretical Analysis </h2>  

<h3> Problem Definition </h3>

- In the paper, author proposed an algorithmic framework for learning continuous feature representations  
  for nodes in networks. In Node2Vec, we learn a mapping function by maximizing the likelihood of preserving  
  network neighborhoods of nodes.
    
    - __Empty__ 
 
    - __Empty__
    
    - __Empty__
   
   
<h3> Method & Solution </h3>

- __Empty__
  
    - __Empty__
    
    - __Empty__
    
    - __Empty__
    
<h3> Comparison with Related Techniues & Recent Works </h3>

- Classic approaches based on linear and non-linear dimensionality reduction techniques optimize an objective that  
  transforms a representative data matrix of the network such that it maximizes the variance of the data representation  
  --> result in <span style ="color:red"> expensive computation for a large real networks </span>
 
- New Approach seeks to preserve local neighborhoods of nodes. Especially, our approach returns feature representations    
  that maximize the likelihood of preserving network neighborhoods of nodes in a d-dimensional feature space.  
  --> <span style ="color:red"> 1. flexible notion of a node's network neighborhood </span>  
  --> <span style ="color:red"> 2. Using random walk approach in order to explore local area </span>   
  
    - __While Node2Vec is a semi-supervised algorithm, DeepWalk is an unsupervised algorithm.__  
      __What's the difference between two algorithms?__
    
    - __Empty__
    
    - __Empty__
    

<h3> Limitation </h3>

- __Empty__ 
    
    - __Empty__ 
    
    - __Empty__
    
    - __Empty__
    
<h3> My Suggestion </h3>





<h2> 2. Implementation </h2>
<h3> </h3>
.