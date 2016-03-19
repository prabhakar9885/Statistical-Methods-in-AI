# K-nearest neighbour (kNN) classifier 
This assignment requires you to implement (a baby first
step into the world of data classification!) and test it on three different datasets from the [UCI
Machine learning repository]. Given below are the instructions
for downloading the datasets and carrying out the experiment. Once you conduct the
experiments, calculate the metrics described and answer the questions below.

Experimental Procedure:
1. Download any three datasets from the UCI ML repository, one of them being the [Iris
dataset].

2. Randomly partition each dataset into two parts of equal size named Training set and
Testing set.

3. Use the training set as labelled examples and do K-nearest neighbor classification (do
with K=1 and 3) of the Testing set samples. Deal with any ties appropriately but mention
this in observations part of the report.

4. Compute the accuracy (percentage of correct classification) using the labels of the Test
samples and the output from your classifier.

5. Repeat steps 2 - 4 for ten times, each time dividing the dataset differently. Report the
mean and standard deviation of the accuracy over the ten test runs.

6. Report the confusion matrix of each dataset, which depicts the classes that are most
confused.

7. The process described in steps 2-5 is Random subsampling approach. Repeat this with 5-
fold cross validation and report the mean and standard deviation of each fold as well as
the grand mean of all the folds.

[UCI Machine learning repository]:<http://archive.ics.uci.edu/ml/>
[Iris dataset]:<http://archive.ics.uci.edu/ml/datasets/Iris>


### How to run the code?
- KNN with Random-Subsampling
  ```sh
   $ python driver_Random_Sampling.py <numberOfTrials> <k> <file-name> <feature-count>
   ```
- KNN with Random subsampling
    ```sh
    $ python driver_kFold_Sampling.py <k> <file-name> <feature-count>
    ```
- Decision boundary for Iris dataset :
    ```sh
    $ python plot_iris.py <file-name> 
    ```

For more information check [README.pdf]

[README.pdf]: <https://github.com/prabhakar9885/Statistical-Methods-in-AI/blob/master/1%20KNN/Code/README.pdf>
