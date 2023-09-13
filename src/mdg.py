# Libraries
import os, glob, datetime, tqdm, pickle, warnings, argparse
import pandas as pd

# Mobility
import skmob
from skmob.models.markov_diary_generator import MarkovDiaryGenerator
from skmob.models.epr import Ditras

# Geospatial (for the tessellation)
import geopandas as gpd
from shapely.geometry import Polygon

warnings.filterwarnings('ignore')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    # Add argument definitions
    parser.add_argument("--path", default='/data_1/mobility/task1_dataset.csv', type=str, help="Path to the input csv file.")
    parser.add_argument("--seed", default=42, type=int, help="Random seed.")
    parser.add_argument("--uid_start", default=80000, type=int, help="User ID number in the test dataset (first ID to be predicted)")
    parser.add_argument("--uid_end", default=99999, type=int, help="User ID number in the test dataset (last ID to be predicted).")
    parser.add_argument("--start_datetime", default='1970/02/21 07:00:00', type=str, help="Starting datetime of prediction (relative to '1970/01/01 00:00:00'")
    parser.add_argument("--save", default=False, type=bool, help="Save diary to file (True)")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the parsed arguments
    path = args.path
    seed = args.seed
    uid_start = args.uid_start
    uid_end = args.uid_end
    start_datetime = args.start_datetime
    save_option = args.save

    # Load dataset 
    task1 = pd.read_csv(path)

    # Split train/test
    task1_train = task1[task1['x'] != 999] # Days 0-59
    task1_test = task1[task1['x'] == 999] # Days 60-74

    # Copy data (for clean data handling)
    data = task1_train

    # Combine 'd' and 't' columns to create a single timestamp column
    data['datetime'] = pd.to_datetime(data['d'] * 24 * 60 * 60 + data['t'] * 30 * 60, unit='s')

    # Add "cluster ID" as a string to feed into skmob function
    data['cluster_id'] = [str(x) + '_' + str(y) for x, y in zip(data['x'], data['y'])]

    # Create a TrajDataFrame
    traj_df = skmob.TrajDataFrame(data[['uid','cluster_id','datetime']], datetime='datetime', user_id='user')

    # Create a Markov Diary for each user
    def create_mdg(user_id=None, n_days=15, n_hours=24, seed=42):
        
        # Initiate 
        mdg = MarkovDiaryGenerator()
        
        # Create MDG for a single user
        mdg.fit(traj_df[traj_df.uid == user_id], 1, lid='cluster_id');

        start_time = pd.to_datetime(start_datetime)
        diary = mdg.generate(n_days*n_hours, start_time, seed)
        # print(diary)
        
        return diary

    mdg_full = []

    # Loop through all users (From uid 80K to 99,999)
    for user_id in tqdm.tqdm(range(uid_start, uid_end+1)): 
        mdg = create_mdg(user_id=user_id, seed=seed)
        instance = {'uid': user_id, 
                    'datetime': mdg['datetime'],
                    'abstract_location': mdg['abstract_location']}
        mdg_full.append(instance)
        
    # Save
    if save_option:
        with open("mdg_full_task1.pkl", "wb") as fp:
            pickle.dump(mdg_full, fp)