## The folder `weekday_user` has 3 files

### 1. `cluster_x.npy` gives the ids of the users that belong to each cluster. There are about a dozen users that do not belong to any cluster

### 2. `cluster_label.npy` shows the labels that each cluster is representative of. `h`, `w`, `R`, and `E` stand for home, work, OR, and OE respectively.

### 3. `transition_matrix.npy` is an array of shape (5,3,4,4). The first dimension is the cluster id. The second dimension of the 3 time periods under which the transition matrices are built upon. The first to the third periods are respectively 10pm to 8am, 8am to 5pm, and 5pm to 10pm. The third and the fourth dimensions are the transition matrices. The states in the transition matrices are in the order of `h`, `w`, `R`, and `E`. 
