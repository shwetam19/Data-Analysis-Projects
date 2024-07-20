import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv('medical_examination.csv')

# 2
BMI = df['weight']/((df['height']/100)**2)
df['overweight'] = (BMI > 25).astype(int)

# 3
df['cholesterol'] = df['cholesterol'].replace([1, 2, 3], [0, 1, 1])
df['gluc'] = df['gluc'].replace([1, 2, 3], [0, 1, 1])

# 4
def draw_cat_plot():
    # 5
    df_cat = df[(df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))]

    # 6
    df_cat = pd.melt(df, id_vars = ['cardio'], value_vars = ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])

    #7
    df_cat = pd.DataFrame(df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total'))

    # 8
    fig = sns.catplot(x='variable', y='total', hue='value', col='cardio', data=df_cat, kind='bar').fig

    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
  # Clean the data
  df_heat = df[(df['ap_lo'] <= df['ap_hi'])
    & (df['height'] >= df['height'].quantile(0.025))
    & (df['height'] <= df['height'].quantile(0.975))
    & (df['weight'] >= df['weight'].quantile(0.025))
    & (df['weight'] <= df['weight'].quantile(0.975))]

  # Calculate the correlation matrix
  corr = df_heat.corr()

  # Generate a mask for the upper triangle
  mask = np.zeros_like(corr)
  mask[np.triu_indices_from(mask)] = True

  # Set up the matplotlib figure
  fig, ax = plt.subplots(figsize=(12, 12))

    # Draw the heatmap with 'sns.heatmap()'
  ax = sns.heatmap(corr, annot=True, fmt='.1f', mask=mask, square=True)

  # Do not modify the next two lines
  fig.savefig('heatmap.png')
  return fig