import scipy.stats as stats
import math
import numpy as np
import seaborn as sns
import statsmodels.api as sm

from matplotlib import pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF


def analyse_residuals(target, prediction):
    e = target-prediction
    mu = 0
    sigma = np.sqrt(np.var(e)) 
    ecdf = ECDF(e.ravel())

    plt.figure(figsize=(24, 10))

    plt.subplot(2, 2, 1)
    plt.title('Porównanie dystrybuant', size=20)
    plt.ylabel('Prawdopodobieństwo')
    plt.xlabel('Wartości resztowe')
    plt.plot(ecdf.x,ecdf.y)

    s = np.random.normal(mu, sigma, len(e))
    ecdf_2 = ECDF(s.ravel())
    plt.plot(ecdf_2.x,ecdf_2.y)

    plt.subplot(2, 2, 2)
    sns.distplot(e, hist=False)
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, len(e)*10)
    plt.title('Porównanie gęstości', size=20)
    plt.xlabel('Wartości resztowe')
    plt.plot(x, stats.norm.pdf(x, mu, sigma))

    plt.subplot(2, 2, 3)
    plt.title('Histogram wartości resztowych', size=20)
    plt.xlabel('Wartości resztowe')
    plt.hist(e, density=True, bins=30)

    plt.subplot(2, 2, 4)
    plt.title('QQPlot wartości resztowych', size=20)
    plt.xlabel('Kwantyle wartości resztowych')
    plt.ylabel('Kwantyle rozkładu N(0, 329.88)')

    plt.scatter(sorted(e), sorted(s))
    plt.plot([min(e), max(e)], [min(e), max(e)], c='r')
    plt.tight_layout()
    
def my_boxplot(e):
    plt.figure(figsize=(30, 10))
    plt.title("Wykres pudełkowy wartości resztowych", size=32)
    sns.boxplot(x=e)
