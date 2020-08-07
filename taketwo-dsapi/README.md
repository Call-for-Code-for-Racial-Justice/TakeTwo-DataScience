# Data Science API (DS-MVP-0)

This is a simple API as part of the Data Science Stream defined in DS-MVP-0. The API uses FastAPI and there is a backend cloudant database. 

The base terms in the database come from [Wikipedia](https://en.wikipedia.org/wiki/List_of_ethnic_slurs). However, over time the dataset is subject to changes/amendments.

In the future this api will serve the model result rather than a database lookup term. 

DS-MVP-0 (this module does not involve "data science/machine learning" models, and may be placed in a different repo - e.g. taketwo-webapi). A module that can detect racially biased terms based on a dictionary look-up, where the look up may be done via calls to a database table containing pre-identified set of racially biased terms.