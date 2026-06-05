# Troubleshooting

## nnU-Net cannot find paths

Check that these environment variables are set:

```bash
echo "$nnUNet_raw"
echo "$nnUNet_preprocessed"
echo "$nnUNet_results"
```

## Dataset integrity check fails

Common causes:

- File names do not follow nnU-Net format.
- Images use `_0000.nii.gz` but labels do not.
- Label values do not match `dataset.json`.
- Training image and label shapes differ.

## CUDA out of memory

Try:

- Use `CONFIG=2d` first.
- Reduce patch size through nnU-Net planner customization later.
- Use fewer background processes.
- Train on a smaller fold or subset for debugging.

## Predictions look empty

Check:

- Input modality and intensity range.
- Whether labels were correctly mapped.
- Whether the model trained long enough.
- Whether prediction used the same dataset ID and configuration.

