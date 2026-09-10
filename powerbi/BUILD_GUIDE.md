# Power BI dashboard build guide

## Files to import

Open Power BI Desktop and choose **Get data > Text/CSV**, then import `../data/expense_data.csv`. Rename the imported table to `Expenses`. Ensure these data types before building visuals:

| Column | Type |
| --- | --- |
| `expense_date` | Date |
| `amount` | Fixed decimal number |
| All other columns | Text |

Import `theme.json` through **View > Themes > Browse for themes**. Create the measures in `measures.dax` one at a time from **Modeling > New measure**.

## Page design: Executive Spend Summary

Use a 16:9 canvas. Set the page background to `#F6F8FC` and use white visual containers with 12px rounded corners, soft shadows, and 16px internal padding. Use Segoe UI throughout. Do not use heavy borders, crowded legends, or more than six colors.

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│ PERSONAL EXPENSE ANALYTICS                  Date | Category | Mode | Day type │
├──────────────┬──────────────┬──────────────┬─────────────────────────────────┤
│ Total Spend  │ Avg / Day    │ Top Category │ Highest Spend Day               │
│ ₹14,533      │ ₹484         │ Food         │ 24 Dec 2025 · ₹2,090            │
├───────────────────────────────────────┬─────────────────────────────────────┤
│ Daily spending trend                  │ Spend by category                   │
│ Line chart                             │ Sorted horizontal bar chart          │
├───────────────────────────────────────┼─────────────────────────────────────┤
│ Weekday vs weekend                     │ Payment mix                          │
│ Clustered columns + average tooltip    │ Donut chart                          │
├───────────────────────────────────────┴─────────────────────────────────────┤
│ Top 5 spend days table                 │ Key insight callout                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Visual configuration

1. **Header**: text box, `PERSONAL EXPENSE ANALYTICS`, 22pt Segoe UI Semibold. Add a smaller subtitle: `December 2025 spending behavior`.
2. **Slicers**: horizontal dropdown slicers for `expense_date`, `category`, `payment_mode`, and `day_type`. Keep them in a single row on the right of the header.
3. **KPI cards**: four New Card visuals using `[Total Spend]`, `[Average Daily Spend]`, `[Top Category]`, and `[Highest Spend Date]`. For the last card, show `[Highest Daily Spend]` as the reference label.
4. **Daily spending trend**: line chart. X-axis: `expense_date`; Y-axis: `[Total Spend]`. Turn on markers. Use `#4F6DF5`; hide the legend; set the Y-axis title to `Spend (INR)`.
5. **Spend by category**: clustered bar chart. Y-axis: `category`; X-axis: `[Total Spend]`; sort descending. Use `#8B5CF6`. Turn on data labels, display units `None`, and remove the legend.
6. **Weekday vs weekend**: clustered column chart. X-axis: `day_type`; Y-axis: `[Total Spend]`. Add `[Average Daily Spend]` to the tooltip so the total is interpreted alongside active-day differences.
7. **Payment mix**: donut chart. Legend: `payment_mode`; Values: `[Total Spend]`. Put the legend at bottom and show percentage labels.
8. **Top 5 spend days**: table with `expense_date`, `[Total Spend]`, and `category`; apply a Top N visual filter of 5 by `[Total Spend]`. Sort descending. Use alternating row shading.
9. **Insight callout**: a text box linked to the current dataset: `Food is the largest spending category. Use category and date filters to investigate daily spikes and discretionary spend.`

## Finishing touches

- Format currency measures as `₹#,0; (₹#,0); -` and percentages as `0.0%`.
- Align all visual edges and use 20px spacing between containers.
- Disable unnecessary visual headers and interactions that do not help filtering.
- Add alt text to every chart and use the same category color when it appears in multiple places.
- Save the completed file as `Personal_Expense_Analytics.pbix`.
