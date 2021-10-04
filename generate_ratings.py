# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd

behaviors = pd.read_csv('behaviors.tsv', delimiter="\t", names=['impression_id', 'user_id', 'time', 'history', 'impressions'])


# %%
behaviors.shape


# %%
behaviors.head(4)


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

ratings.shape


# %%
def filter_by_freq(df: pd.DataFrame, column: str,
                   min_freq: int) -> pd.DataFrame:
    """Filters the DataFrame based on the value frequency in the specified column.

    :param df: DataFrame to be filtered.
    :param column: Column name that should be frequency filtered.
    :param min_freq: Minimal value frequency for the row to be accepted.
    :return: Frequency filtered DataFrame.
    """
    # Frequencies of each value in the column.
    freq = df[column].value_counts()
    # Select frequent values. Value is in the index.
    frequent_values = freq[freq >= min_freq].index
    # Return only rows with value frequency above threshold.
    return df[df[column].isin(frequent_values)]


filtered_ratings = ratings

items_or_users_have_lt_five = True

# We'll need to do this several times, so that users and items all have five items -- repeat until the number of items removed is zero
while items_or_users_have_lt_five:
    old_list_length = filtered_ratings.shape[0]
    print('filtering ratings, current size:', old_list_length)

    # Only include users with over 50 ratings
    filtered_ratings = filter_by_freq(filtered_ratings, 'user_id', 50)

    # Only include items with over 50 ratings
    filtered_ratings = filter_by_freq(filtered_ratings, 'item_id', 50)

    new_list_length = filtered_ratings.shape[0]

    items_or_users_have_lt_five = new_list_length < old_list_length


filtered_ratings.shape


# %%
print(len(filtered_ratings['user_id'].drop_duplicates()), 'users')
print(len(filtered_ratings['item_id'].drop_duplicates()), 'items')


# %%
freq = filtered_ratings['item_id'].value_counts()

# TODO: check for duplicate user/item pairs

freq.to_csv('frequency.csv')


# %%
filtered_ratings.count()


# %%
filtered_ratings.head(2)


# %%
filtered_ratings.to_csv('librec-auto-study/data/ratings.csv', header=False, index=False)
filtered_ratings.head(50000).to_csv('librec-auto-study/data/ratings-sample.csv', header=False, index=False)


