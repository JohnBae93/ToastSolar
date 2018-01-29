# Toast Solar
Toast solar is Toast AI engine for recommendation system

* Pre-Processing
    * Korean Tokenizing ([KoNLPy](http://konlpy.org/en/v0.4.4/))
    * Word Embedding ([fastText](https://fasttext.cc/))
* Recommendation system
    * Label-Based Filter
        * Semi-Supervised Learning (Content Labelling)
        * Reinforcement Learning (User Labelling)
        * Calculate Similarity (Cosine, Pearson`s)
    * Collaboration Filter
        * User-Based Filter
        * Content-Based Filter