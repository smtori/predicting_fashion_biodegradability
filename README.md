# predicting_fashion_biodegradability
Analyzing fabric composition in fast fashion to understand material sustainability patterns using machine learning.
## About
This project examines garment data from a Zara product catalog to classify textiles by composition and explore sustainability trends. Using a from-scratch K-Nearest Neighbors classifier, we categorize garments into four material types based on their fabric makeup. Future work will incorporate linear regression modeling and external sustainability metrics to quantify the environmental impact of different fabric choices.
Data Source: Zenodo — Zara Dataset | DOI: 10.5281/zenodo.4261101
### Progress
![Progress](https://progress-bar.xyz/55)
## Material Categories
Each garment is assigned one of four labels based on its natural-to-synthetic fiber ratio:
CategoryDefinitionNatural100% natural fibers (cotton, linen, wool, camel hair)Synthetic100% synthetic fibers (polyester, nylon, acrylic, etc.)Blend — Mostly Natural≥ 50% natural fibersBlend — Mostly Synthetic< 50% natural fibers
## Project Structure
Raw_Data_Cleaning.py            # Data cleaning, merging, and feature engineering

Knn_fabric_clustering        # KNN classifier implementation and evaluation

README.md
## Raw_Data_Cleaning.py — Data Pipeline
Handles all preprocessing steps:

Loads and merges the Zara items and composition CSVs on item_code
Categorizes each raw material as natural, synthetic, or semi-synthetic
Computes per-garment natural vs. synthetic percentages
Builds a pivot table so each material becomes its own feature column
Assigns the four-category label and exports a model-ready CSV

Knn_fabric_clustering — KNN Classification
Implements K-Nearest Neighbors from scratch (no sklearn.neighbors):

Custom KNN class with Euclidean distance, neighbor selection, and majority-vote classification
Train / validation / test split (80/20 cascaded)
Hyperparameter tuning over odd values of k from 1–29, optimized on weighted F1 score
Evaluation via accuracy, weighted F1, and a full classification report
Example prediction — e.g., a 60% cotton / 40% polyester garment is classified in real time

## Planned Work

Linear Regression — Model the relationship between fabric composition and garment pricing to identify whether sustainable materials carry a cost premium.
Sustainability Metrics — Integrate external environmental impact data (water usage, CO₂ emissions, biodegradability) to score each garment's ecological footprint.
Visualizations — Expand charting (built on Altair) to visualize classification boundaries, pricing trends, and sustainability scores across categories.

## Tech Stack

Python 3
pandas · NumPy · scikit-learn (metrics and preprocessing only) ·
Altair (visualization)
