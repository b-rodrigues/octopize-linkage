"""Script performing linkage under different settings for a given dataset."""

import pandas as pd

from linkage import Distance, link_datasets, LinkingAlgorithm
from pre_linkage_metrics import ImputeMethod, contribution_score, get_unicity_score

# Select common/shared columns
shared_columns = ['sex', 'nationality', 'age', 'province', 'place_birth']
# shared_columns = ['search_work', 'household_duties', 'main_prof_situation', 'place_birth', 'search_months', 'search_method', 'age']

# LINK_ORI_AVA = ["original", "avatars"]
LINK_ORI_AVA = ["avatars"]

linkage_algos = [LinkingAlgorithm.LSA] # [LinkingAlgorithm.LSA, LinkingAlgorithm.MIN_ORDER]
# distances = [Distance.GOWER, Distance.PROJECTION_DIST_ALL_SOURCES, Distance.ROW_ORDER, Distance.RANDOM]
# distances = [Distance.GOWER, Distance.PROJECTION_DIST_FIRST_SOURCE, Distance.PROJECTION_DIST_SECOND_SOURCE, Distance.PROJECTION_DIST_ALL_SOURCES, Distance.ROW_ORDER, Distance.RANDOM]
distances = [Distance.PROJECTION_DIST_ALL_SOURCES]
should_shuffle_before_linkage = True

for ori_ava in LINK_ORI_AVA:
    if ori_ava == "avatars":
        # load avatars from both sources
        df1 = pd.read_csv("data/pra_A_unshuffled_avatars.csv")
        df2 = pd.read_csv("data/pra_B_unshuffled_avatars.csv")
    else:
        df1 = pd.read_csv("data/pra_A.csv")
        df2 = pd.read_csv("data/pra_B.csv")

    should_be_categorical_columns_1 = ['nationality', 'place_birth', 'sex', 'province', 'household_duties', 'relation_to_activity1', 'relation_to_activity2']
    should_be_categorical_columns_2 = ['nationality', 'place_birth', 'sex', 'province', 'relationship', 'main_occupation', 'availability', 'search_work', 'search_reason', 'search_steps', 'search_method', 'main_activity', 'main_prof_situation' ,'main_sector' ,'contract_type']

    for col in should_be_categorical_columns_1:
        df1[col] = df1[col].astype(object)
    for col in should_be_categorical_columns_2:
        df2[col] = df2[col].astype(object)

    # ################################
    # # Pre-linkage metrics
    # ################################
    # # ?? How representative of the dataset at source 1 are my common variables ?
    # contribution_score_dict1 = contribution_score(
    #     df=df1, 
    #     shared_columns=shared_columns, 
    #     target_explained_variance=0.9,
    #     impute_method=ImputeMethod.MEDIAN,
    #     should_consider_missing=True,
    #     seed=None)

    # # ?? How representative of the dataset at source 2 are my common variables ?
    # contribution_score_dict2 = contribution_score(
    #     df=df2, 
    #     shared_columns=shared_columns, 
    #     target_explained_variance=0.9,
    #     impute_method=ImputeMethod.MEDIAN,
    #     should_consider_missing=True,
    #     seed=None)


    n_unique_comb1 = get_unicity_score(df1, shared_columns)
    n_unique_comb2 = get_unicity_score(df2, shared_columns)

    print("== Pre-linkage metrics ==")
    # print(f"Contribution score for source 1: {contribution_score_dict1}")
    # print(f"Contribution score for source 2: {contribution_score_dict2}")
    print(f"Unicity score for source 1: {n_unique_comb1}")
    print(f"Unicity score for source 2: {n_unique_comb2}")

    for linkage_algo in linkage_algos:
        for distance in distances:
            _df1 = df1.copy()
            _df2 = df2.copy()
            if distance != Distance.ROW_ORDER and should_shuffle_before_linkage:
                _df2 = _df2.sample(frac=1).reset_index(drop=True)
            
            # link the two sources
            print(f"\n\nRunning {ori_ava} with linkage algorithm: {linkage_algo.value}, distance: {distance.value} ...")
            linked_df = link_datasets(_df1, _df2, shared_columns, distance=distance, linking_algo=linkage_algo)
            linked_df.to_csv(f"data/pra_linked_data__{ori_ava}__{linkage_algo.value}__{distance.value}.csv", index=False)
