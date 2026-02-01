### Taste Profile Derivation (Methodology)

To summarize the user's content preferences, we derived a structured taste profile directly from the annotated watch-history dataset. This process was not based on subjective guessing, but on consistent patterns observed in the user's highest-rated titles and their associated genre attributes.

1. Preference Signal from Ratings

Each title in the dataset is assigned an explicit preference score (1–10). Titles rated in the upper range (typically 8–10) are treated as strong positive signals representing the user's core interests, while low-rated titles (1–2) represent strong negative preferences.

This separation allows the system to focus on the most informative content when building the user profile.

2. Genre Tag Aggregation

For all strongly preferred titles, we aggregate the associated `genre_tags`. By analyzing which tags appear most frequently among high-scoring items, the system identifies recurring thematic patterns such as:

* psychological thriller
* dark crime and mystery
* emotionally driven human drama
* immersive science fiction universes
* warm, character-centered animation

These repeated tag structures form the foundation of the user's dominant preference dimensions.

3. Cluster-Based Interpretation

Rather than relying on individual titles, preferences are grouped into broader clusters of related narrative types. For example:

* Mouse, Signal, and Parasite consistently align with psychological crime and suspense-driven storytelling
* My Mister, Misaeng, and Reply 1988 represent human-centered social realism
* Dune and Interstellar reflect emotionally grounded science fiction with large-scale world-building
* Pixar titles such as Coco and Toy Story indicate strong affinity for warm, emotionally meaningful animation

This clustering provides a more generalizable representation of user taste beyond specific franchises.

4. Negative Preference Filtering

Disliked content is equally informative. Titles labeled with low scores frequently include lighter romantic tones, ambiguous pacing, or superhero-family style narratives. These signals are incorporated as exclusion constraints, improving recommendation relevance by reducing mismatched suggestions.

### Result: Core Preference Summary

Based on the combination of rating-weighted signals, genre tag frequency, thematic clustering, and negative filtering, the user profile can be summarized into the following dominant preference categories:

* Psychological crime thrillers with strong twists
* Deep human and socially grounded realism dramas
* High-quality cinematic films with intensity and meaning
* Immersive science fiction universes with emotional depth
* Warm Pixar/Disney-style storytelling focused on character and emotion

This structured profile serves as the retrieval query backbone for an explainable RAG-based recommendation pipeline.
