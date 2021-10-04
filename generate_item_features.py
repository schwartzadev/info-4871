# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd

columns = ['news_id', 'category', 'subcategory', 'title', 'abstract', 'url', 'title_entities', 'abstract_entities']

news = pd.read_csv(
    'news.tsv',
    delimiter="\t",
    names=columns)

news.shape


# %%
trimmed_news = news[['news_id', 'category', 'subcategory']]

trimmed_news.head()


# %%
categories = trimmed_news.category.unique()
category_dict = dict(zip(categories, range(len(categories))))


# %%
subcategories = trimmed_news.subcategory.unique()
subcategory_dict = dict(zip(subcategories, range(len(subcategories))))


# %%
trimmed_news = trimmed_news.replace({'category': category_dict, 'subcategory': subcategory_dict})

trimmed_news.head(4)


# %%
trimmed_news.to_csv('librec-auto-study/data/item-features.csv', header=False, index=False)
trimmed_news.head(50000).to_csv('librec-auto-study/data/item-features-sample.csv', header=False, index=False)


