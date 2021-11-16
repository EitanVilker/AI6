<h1>
  
  CS 76
  
  21F
  
  PA6
  
  Eitan Vilker
  
</h1>

### Description
I implemented my HMM by attempting to do as much work as possible before the problem began; this was mostly put in the MazeProblem.py file. 
First, I implemented a 1D list of squares, starting from the bottom left and going to the top right, along with functions to convert 1D to 2D and back. 
This made iterating much, much simpler.
Next, I created a transition matrix of the odds of getting from one square to another for all squares. 
In the same vein, I created an observation matrix, which had a row for each color with the entries in that rows corresponding to the odds of identifying a square given that the current color was seen.
I used the Maze.py file from PA2, with a few minor modifications to account for letters as squares.
Finally, the actual algorithm was executed using for loops to sum the product of the posterior, observation, and transition probabilities and store it in the probability matrix to be used for future posterior probabilities.


### Evaluation
My results almost perfectly matched the results posted in the Slack, with what amounts to a few rounding errors of difference. 
I'm not sure why it's not exactly the same, but the results are clearly meaningful.

I also made a more randomized version, where the robot starts in a random location (including possibly in a wall, which causes early termination as it is illegal).
It then moves in a random direction at each time step.
Using this testing method, I found that the robot's success was heavily dependent upon whether or not the last measurement was accurate.
Inaccurate measurements often led the progr am to believe there was a single digit percent chance of the robot being in its actual square.
However, in every other instance, the correct square was pretty much always in the top two most likely candidates, so it seems like it worked pretty well.
I assume that if I were to implement forward-backward and/or Viterbi I could lessen the impact of inaccurate readings.
It would probably also help if the algorithm were adjusted to account for more than the previous time step like we did in CS 10, but that would undoubtedly be a huge amount of work.
