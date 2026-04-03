"""
Step 1: Create proper train/dev/test split
- 70% train, 15% dev, 15% test
- Stratified by label (keeps void proportion equal)
- Fixed random seed for reproducibility
"""

from datasets import load_from_disk, concatenate_datasets, DatasetDict
from sklearn.model_selection import train_test_split

# Load original dataset
ds = load_from_disk("../../loc_datasets/agb-de")
full_data = concatenate_datasets([ds["train"], ds["test"]])

print(f"Total clauses: {len(full_data)}")
print(f"Total void:    {sum(full_data['label'])}")

# Get indices and labels
indices = list(range(len(full_data)))
labels = full_data["label"]

# First split: 70% train, 30% temp
train_idx, temp_idx = train_test_split(
    indices, test_size=0.30, random_state=42, stratify=labels
)

# Second split: 15% dev, 15% test
temp_labels = [labels[i] for i in temp_idx]
dev_idx, test_idx = train_test_split(
    temp_idx, test_size=0.50, random_state=42, stratify=temp_labels
)

# Create dataset splits
train_ds = full_data.select(train_idx)
dev_ds = full_data.select(dev_idx)
test_ds = full_data.select(test_idx)

# Verify proportions
print(f"\nFinal splits:")
print(
    f"Train: {len(train_ds)} clauses, {sum(train_ds['label'])} void ({100*sum(train_ds['label'])/len(train_ds):.1f}%)"
)
print(
    f"Dev:   {len(dev_ds)} clauses, {sum(dev_ds['label'])} void ({100*sum(dev_ds['label'])/len(dev_ds):.1f}%)"
)
print(
    f"Test:  {len(test_ds)} clauses, {sum(test_ds['label'])} void ({100*sum(test_ds['label'])/len(test_ds):.1f}%)"
)

# Save split
new_ds = DatasetDict({"train": train_ds, "dev": dev_ds, "test": test_ds})

new_ds.save_to_disk("../../loc_datasets/agb-de-proper-split")
print("\nSplit saved! ✅")
