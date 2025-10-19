"""
Generate realistic embeddings for apps with historical performance data.
This connects the sample apps, embeddings, and performance data properly.
"""
import pickle
import pandas as pd
import numpy as np
from pathlib import Path

# Load data
apps_df = pd.read_csv('data/sample_apps.csv')
perf_df = pd.read_csv('data/historical_performance.csv')

# Get apps that have performance data
apps_with_perf = list(perf_df['app_id'].unique())
print(f"Found {len(apps_with_perf)} apps with performance data")

# Get app metadata for these apps
apps_metadata = apps_df[apps_df['app_id'].isin(apps_with_perf)][
    ['app_id', 'app_name', 'super_category', 'app_platform']
].drop_duplicates(subset=['app_id'])

print(f"Matched {len(apps_metadata)} apps with metadata")

# Generate embeddings for v1 and v2
# v1: Simpler model (64 dimensions)
# v2: More sophisticated model (128 dimensions, better separation)

def generate_embeddings_v1(app_id, category, platform):
    """Generate v1 embeddings - simpler model"""
    np.random.seed(hash(app_id) % 2**32)

    # Base vector
    base = np.random.randn(64)

    # Add category signal (weaker in v1)
    if pd.notna(category):
        cat_hash = hash(str(category)) % 2**32
        np.random.seed(cat_hash)
        cat_signal = np.random.randn(64) * 0.3
        base += cat_signal

    # Normalize
    norm = np.linalg.norm(base)
    return base / (norm + 1e-9)


def generate_embeddings_v2(app_id, category, platform):
    """Generate v2 embeddings - more sophisticated"""
    np.random.seed(hash(app_id) % 2**32)

    # Base vector (higher dimension)
    base = np.random.randn(128)

    # Add stronger category signal (better in v2)
    if pd.notna(category):
        cat_hash = hash(str(category)) % 2**32
        np.random.seed(cat_hash)
        cat_signal = np.random.randn(128) * 0.6  # Stronger signal
        base += cat_signal

    # Add platform signal (v2 considers platform)
    if pd.notna(platform):
        platform_hash = hash(str(platform)) % 2**32
        np.random.seed(platform_hash)
        platform_signal = np.random.randn(128) * 0.2
        base += platform_signal

    # Normalize
    norm = np.linalg.norm(base)
    return base / (norm + 1e-9)


# Build embeddings dictionaries
embeddings_v1 = {}
embeddings_v2 = {}

for _, row in apps_metadata.iterrows():
    app_id = row['app_id']
    category = row['super_category']
    platform = row['app_platform']

    embeddings_v1[app_id] = generate_embeddings_v1(app_id, category, platform)
    embeddings_v2[app_id] = generate_embeddings_v2(app_id, category, platform)

print(f"\nGenerated embeddings for {len(embeddings_v1)} apps")
print(f"v1 shape: {embeddings_v1[apps_with_perf[0]].shape}")
print(f"v2 shape: {embeddings_v2[apps_with_perf[0]].shape}")

# Save pickle files
with open('data/mock_embeddings_v1.pkl', 'wb') as f:
    pickle.dump(embeddings_v1, f)
print("\n[OK] Saved v1 embeddings to data/mock_embeddings_v1.pkl")

with open('data/mock_embeddings_v2.pkl', 'wb') as f:
    pickle.dump(embeddings_v2, f)
print("[OK] Saved v2 embeddings to data/mock_embeddings_v2.pkl")

# Also save app metadata mapping for quick lookup
metadata_map = {}
for _, row in apps_metadata.iterrows():
    metadata_map[row['app_id']] = {
        'name': row['app_name'],
        'category': row['super_category'],
        'platform': row['app_platform']
    }

with open('data/app_metadata.pkl', 'wb') as f:
    pickle.dump(metadata_map, f)
print("[OK] Saved app metadata to data/app_metadata.pkl")

print("\n" + "="*60)
print("SUCCESS! Embeddings generated for all apps with performance data")
print(f"Apps: {len(embeddings_v1)}")
print(f"Sample app IDs: {apps_with_perf[:5]}")
print("="*60)
