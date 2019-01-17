<h1> t - SNE </h1>

<h2> 1. Theoretical Analysis </h2>  

<h3> Problem Definition </h3>

- In the paper, author aimed to display high-dimensional data on low-dimension(especially d=2,3)  
    
    - __How can we preserve both local structure and global structure in embedding process?__ 
 
    - __What is the Crowd problem?__
    
    - __What is the Short-circuiting problem?__
   
   
<h3> Method & Solution </h3>

- The main idea is to convert the high-dimensional __Euclidean distances__ between datapoints into  
  __conditional probabilities__ that represent similarities.
    
    - __What is Stochatic Neighbor Embedding?__
    
    - __What is t-Distributed Stochastic Neighbor Embedding?__
    
    - __How can t-SNE capture much of the local structure of the high-dimensional data very well,__  
      __while also revealing global structure such as the presence of clusters at several scales?__
    
    
<h3> Comparison with Related Techniques & Recent Works </h3>


<h3> Limitation </h3>

- __t-SNE had three potential weaknesses__  
    
    - __Is it still a valid method when embedding dimension is relatively large?__  
    
    - __Applying t-SNE to large data set?__
    
    - __Is it guarantted to converge to a global optimum of its cost function?__

<h3> My Suggestion </h3>





<h2> 2. Implementation </h2>
<h3> </h3>
.