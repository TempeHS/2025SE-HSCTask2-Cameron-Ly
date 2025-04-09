# Final Data Preview

## Engineered Features

| Feature Name         | Description                                           | Data Type | Example Value |
| -------------------- | ----------------------------------------------------- | --------- | ------------- |
| `hand_strength`      | Numerical score representing the strength of the hand | Float     | 0.85          |
| `unique_ranks`       | Number of distinct card ranks in the hand             | Integer   | 4             |
| `unique_suits`       | Number of distinct card suits in the hand             | Integer   | 3             |
| `max_rank_frequency` | Maximum frequency of any single rank in the hand      | Integer   | 2             |

## Outputs

| Output Name | Description                     | Data Type | Example Value |
| ----------- | ------------------------------- | --------- | ------------- |
| `fold`      | Probability of folding the hand | Float     | 0.22          |
| `check`     | Probability of checking         | Float     | 0.53          |
| `call`      | Probability of calling          | Float     | 0.07          |
| `raise`     | Probability of raising          | Float     | 0.16          |
| `all_in`    | Probability of going all-in     | Float     | 0.02          |

## Summary Statistics

| Metric         | Value  |
| -------------- | ------ |
| Total Records  | 10,000 |
| Missing Values | 0      |
| Feature Count  | 4      |
| Output Count   | 5      |

## Notes

- Features are derived from poker hand details using domain-specific logic.
- Outputs are generated using a trained machine learning model.
- Ensure the input data is validated before making predictions.
