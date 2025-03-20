# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clscurves', 'clscurves.plotter', 'clscurves.tests']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.8.2,<4.0.0',
 'mpl-scatter-density>=0.7,<0.8',
 'numpy>=1.20.3,<2.0.0',
 'pandas>=1.2.4,<3.0.0',
 'psutil>=5.9.5,<6.0.0',
 'scipy>=1.6.3,<2.0.0',
 'tqdm>=4.65.0,<5.0.0']

setup_kwargs = {
    'name': 'clscurves',
    'version': '0.4.0',
    'description': 'Compute and plot bootstrapped performance curves for classification problems.',
    'long_description': '# classification-curves\n\nA library for computing and plotting bootstrapped metrics (ROC curves,\nPrecision-Recall curves, etc.) to evaluate the performance of a classification\nmodel.\n\n## Example\n```python\nmg = MetricsGenerator(\n    predictions_df,\n    label_column="label",\n    score_column="score",\n    weight_column="weight",\n    score_is_probability=False,\n    reverse_thresh=False,\n    num_bootstrap_samples=20,\n)\n\nmg.plot_pr(\n    op_value=0.1,\n    bootstrapped=True,\n    bootstrap_alpha=0.05,\n)\nmg.plot_roc()\n```\n\n![Example PR curve](docs/img/pr_curve_bootstrapped.png)\n![Example ROC curve](docs/img/roc_curve.png)\n',
    'author': 'Christopher Bryant',
    'author_email': 'cbryant@berkeley.edu',
    'maintainer': 'Christopher Bryant',
    'maintainer_email': 'cbryant@berkeley.edu',
    'url': 'https://github.com/chrismbryant/classification-curves',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10.0,<3.13',
}


setup(**setup_kwargs)
