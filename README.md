## Taste Profile Derivation (Methodology)

This project derives a structured **user preference profile** directly from an annotated watch-history dataset.  
The resulting profile is not based on subjective intuition, but on consistent patterns extracted from the user’s highest-rated titles and their associated genre attributes.  
This profile serves as the foundation for retrieval and explanation in an RAG-based recommendation pipeline.

---

### 1. Preference Signal from Rating Scores

Each title in the dataset is assigned an explicit preference score ranging from **1–10**, allowing clear separation of positive and negative signals:

- **8–10** → Strong positive preference (core taste)  
- **6–7** → Moderate preference (supporting interests)  
- **4–5** → Neutral exposure (weak signal)  
- **1–2** → Strong negative preference (avoidance signal)  

By prioritizing high-scoring items, the system focuses on the most informative content when constructing the user’s taste representation.

---

### 2. Genre Tag Aggregation

For titles rated in the upper range, the system aggregates their associated `genre_tags`.  
Recurring tag patterns reveal dominant thematic interests, such as:

- Psychological suspense and crime investigation  
- Dark social commentary and moral tension  
- Emotionally grounded human realism  
- Immersive science-fiction world-building  
- Warm, character-centered animated storytelling  

These repeated genre signals form the primary dimensions of the user’s preference space.

---

### 3. Cluster-Based Interpretation of User Taste

Rather than modeling preferences at the level of individual titles, the system groups highly rated content into broader narrative clusters.  
For example:

- **Psychological crime thrillers with twists**  
  (*Mouse*, *Signal*, *Parasite*)

- **Deep human and socially grounded realism dramas**  
  (*My Mister*, *Misaeng*, *Reply 1988*)

- **Immersive sci-fi universes with emotional depth**  
  (*Dune*, *Interstellar*, *Stranger Things*, *Arcane*)

- **Warm Pixar/Disney-style storytelling**  
  (*Coco*, *Toy Story*, *Zootopia*)

This clustering allows the preference profile to generalize beyond specific franchises and supports transferable recommendation logic.

---

### 4. Negative Preference Filtering

Low-rated titles provide equally valuable signals.  
Disliked content frequently aligns with lighter romantic tones, ambiguous pacing, or superhero-family narrative structures.

These negative signals are incorporated as exclusion constraints to reduce mismatched recommendations and improve relevance.

---

### Result: Core Preference Summary

Based on rating-weighted signals, genre frequency, thematic clustering, and negative filtering, the user’s dominant preference categories are:

- Psychological crime thrillers with strong twists  
- Deep human and socially grounded realism dramas  
- High-quality cinematic films with intensity and meaning  
- Immersive sci-fi universes with emotional depth  
- Warm Pixar/Disney-style storytelling focused on character and emotion  

---

## End-to-End Recommendation Pipeline (RAG Framework)

This project applies a Retrieval-Augmented Generation (RAG) workflow to produce both accurate and explainable recommendations.

---

### Step 1. Dataset Construction

The system begins with a structured user preference dataset containing:

- Title metadata (`title`, `type`, `notes`)  
- Explicit preference scores (1–10)  
- Genre-level semantic descriptors (`genre_tags`)  
- Preference buckets (`very_liked`, `liked`, `neutral`, `disliked`)  

This dataset functions as the grounding source for personalization.

---

### Step 2. Retrieval: Candidate Generation

Given a user profile, the system retrieves candidate titles from a content corpus using semantic similarity search.

- Titles are embedded into a shared vector space using metadata and plot-level descriptions  
- User preference embeddings are computed from high-scoring clusters  
- Top-*k* candidates are retrieved via nearest-neighbor vector search  

This stage ensures recommendations are grounded in semantically relevant content rather than popularity alone.

---

### Step 3. Reranking: Preference-Aware Scoring

Retrieved candidates are reranked using a preference-sensitive scoring function that accounts for:

- Similarity to the user’s dominant genre clusters  
- Strength of positive preference alignment  
- Penalization of overlap with disliked genre dimensions  
- Diversity constraints to avoid redundant suggestions  

This hybrid ranking step improves stability beyond retrieval-only approaches.

---

### Step 4. Generation: Explainable Recommendation Output

After ranking, the system uses a generative model to produce natural-language recommendation explanations.

Each recommendation is paired with:

- Supporting evidence from retrieved content documents  
- Explicit alignment with known user preferences  
- Transparent justification rather than ungrounded generation  

---

## Profile-to-Query Transformation

A key contribution of this framework is converting structured user taste into retrieval-ready semantic queries.

The user profile is transformed into a composite query representation by:

- Selecting high-score preference clusters  
- Aggregating frequent genre tag dimensions  
- Removing disliked narrative features  
- Producing a dense embedding that represents the user’s dominant thematic interests  

This embedding acts as the retrieval backbone for candidate generation, ensuring recommendations remain personalized, interpretable, and grounded.

---

## Explainable Recommendation Emphasis

Traditional recommendation systems often provide high-performing rankings but limited interpretability.  
This project explicitly targets **explainable personalization** by integrating retrieval and generation:

- Retrieval provides traceable evidence from content metadata and descriptions  
- Preference clustering provides human-interpretable taste dimensions  
- Generation produces concise explanations grounded in retrieved context  

As a result, the system not only recommends *what* the user may enjoy, but also communicates *why* each recommendation matches the user’s established preferences.


<img width="657" height="437" alt="data_example_1" src="https://github.com/user-attachments/assets/41ab961d-cc21-4a80-ae97-87d8d42e4ed9" />

<img width="656" height="554" alt="data_example_2" src="https://github.com/user-attachments/assets/21804f20-67bc-4a53-822b-16b42883e949" />

check the visualization: https://minjilee-purdue.github.io/llm-rec/
