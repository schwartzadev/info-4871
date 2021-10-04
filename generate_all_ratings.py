"""
Generates an all-ratings.csv file with every rating -- no k-core algorithm is applied.
"""
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd

behaviors = pd.read_csv('behaviors.tsv', delimiter="\t", names=['impression_id', 'user_id', 'time', 'history', 'impressions'])


# %%
# I used the following algorithm to generate the `ratings.csv` file:

# * For each behavior in the `behaviors.tsv` file:
#   * For each impression in the behavior's impressions
#     * If the impression is a click (ends with `-1`)
#       * Create a record with `userId,articleId,1`
#     * If the impression is not a click (ends with `-0`)
#       * Create a record with `userId,articleId,-0.5`
#     * Ignore items that a user hasn't seen, `librec-auto` assumes zeroes

ratings_data = []

for index, row in behaviors.iterrows():
    impressions = row['impressions'].split(' ')
    clicks = list(filter(lambda impression: impression[-2:] == '-1', impressions))
    ignores = list(filter(lambda impression: impression[-2:] == '-0', impressions))
    [ratings_data.append([row['user_id'], click[:-2], 1]) for click in clicks]
    [ratings_data.append([row['user_id'], ignore[:-2], -0.5]) for ignore in ignores]

ratings = pd.DataFrame(ratings_data, columns=['user_id', 'item_id', 'numeric_rating'])

ratings.to_csv('librec-auto-study/data/all-ratings.csv', header=False, index=False)
ratings.head(50000).to_csv('librec-auto-study/data/all-ratings-sample.csv', header=False, index=False)
