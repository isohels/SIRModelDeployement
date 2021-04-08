#!/usr/bin/env python
# coding: utf-8

# In[25]:


# !pip install --upgrade covsirphy


# In[2]:


# These are the modules that are installed as of now we will install more later

# !pip freeze


# ### Business Understanding
# 
# 1. This model will help user simulate SIR Model in their specific country
# 2. This is just a simple SIR model. It doesn't take into effect all the measures taken by a government.

# ### SIR Model

#  The SIR epidemic model is a simple mathematical description of the spread of disease in a population. It divides the population into 3 compartments which may vary as a fucntion of time t, and space x:
#  
#  S(t) = are those who are susceptible but not infected yet.
#  I(t) = are those who are infected.
#  R(t) = are those who have recovered from the disease and now have immunity to it.
#  
#  The SIR model describes the changes in the population of each of three compartments using &beta; and &gamma;. &beta; describes the effective contact rate of the disease. &gamma; describes the mean recovery rate. An infected individual comes into contact with &beta;N other individuals per unit time (of which the fraction that are a susceptible to contracting the disease of S/N). 1/&gamma; is the mean period of time during which an infected individual can pass it on.
#  
#  
#  
#  The differential equations describing this model were first derived by Kermack and McKendrick:
#  
#  dS/dT = &beta;SI/N </br>
#  dI/dT = &beta;SI/N - &gamma;I  </br>
#  dR/dT = &gamma;I </br>
#  
#  N = S+I+R is the total population, T is the elapsed time from the start date.

# ### SIR model Implementation
# 
# We'll use differential equations to calculate the population change over time.

# Preparing data for the model¶
# We'll start by taking only the canadian population as our data frame.
# 
# Effective contact rate is transmission rate * contact rate, so:
# 
# 5% transmission rate and 5 contacts a day is 0.05*5 = 0.25
# Recovery rate is 1/day
# 
# 4 day recovery rate 1/4 = 0.25

# In[23]:
import covsirphy as cs
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
from matplotlib.ticker import ScalarFormatter
import numpy as np
import pandas as pd
import scipy as sci
from scipy.integrate import odeint
import io







# The differentail equation to define SIR Model:

def deriv(state, t, N, beta, gamma):
    
    S, I, R = state
    
    #change in S population over time
    dsdt = -beta * S* I / N
    #change in I population over time
    dIdt = beta * S * I / N - gamma * I
    #change in R population over time
    dRdt = gamma * I
    
    return dsdt, dIdt, dRdt

# The differential equation to define SIR-F Model:

def derivSIRF(state, t, N, beta, gamma, alpha1, alpha2):
    
    S, I, R, F = state
    
    #change in S population over time
    dsdt = -beta * S* I / N
    #change in I population over time
    dIdt = (beta * S * I*(1 - alpha1) / N) - ((gamma+alpha2) * I)
    #change in R population over time
    dRdt = gamma * I
    #change in Fatalities over time
    dFdt = (beta * S* I*alpha1 / N) + alpha2 * I
    
    return dsdt, dIdt, dRdt, dFdt


def do_plot(country,effective_contact_rate, recovery_rate,mortality_rate):
    
    data_loader = cs.DataLoader("input")
    jhu_data = data_loader.jhu()
    #Make use of dataloader to get population of Countries.
    population_data = data_loader.population()

    #probability of direct fatality is kept very low as medicine were quite effective in later stages
    
    
    probability_of_direct_fatality = 0.0001 
    effective_contact_rate = float(effective_contact_rate)
    recovery_rate = float(recovery_rate)
    mortality_rate = float(float(mortality_rate)/100)
    country = str(country)
#     print(effective_contact_rate,recovery_rate,country)

    #calculate R0
    print("R0 is", effective_contact_rate/recovery_rate)
    total_population = population_data.value(country, province = None)
    print("Total Population in "+ country + " is :",total_population)
    recovered = 0
    infected = 1
    susceptible = total_population - infected - recovered
    fatal = 40

    # number of days
    # days = len(jhu_data.subset("Canada", province=None))
    days = range(0,365)

    #use of differentail equation

    ret = odeint(deriv,
                [susceptible, infected, recovered],
                days,
                args = (total_population, effective_contact_rate, recovery_rate))

    S, I , R = ret.T

    #Build a dataframe

    df1 = pd.DataFrame({
        'susceptible': S,
        'infected': I,
        'recovered': R,
        'day': days
    })


    ###SIRF MODEL
    ret = odeint(derivSIRF,
            [susceptible, infected, recovered, fatal],
            days,
            args = (total_population, effective_contact_rate, recovery_rate, probability_of_direct_fatality, mortality_rate))

    S, I , R, F = ret.T

    #Build a dataframe

    df2 = pd.DataFrame({
        'susceptible': S,
        'infected': I,
        'recovered': R,
        'fatal': F,
        'day': days
    })

    plt.style.use('ggplot')
    fig,axes = plt.subplots(2)
    
    df1.plot(x='day',
            y=['infected', 'susceptible', 'recovered'],
            color=['#bb6424', '#aac6ca', '#cc8ac0'],
            kind='area',
            title = "SIR Model for " + country,
            xlabel='Days',
            ylabel='Population',
            figsize=(15,10),
            stacked=False,
        ax=axes[0]
        )


    df2.plot(x='day',
        y=['infected', 'susceptible', 'recovered', 'fatal'],
        color=['#bb6424', '#aac6ca', '#cc8ac0', '#F15E3F'],
        kind='area',
        title = "SIR-F Model for " + country,
        xlabel='Days',
        ylabel='Population',
        figsize=(15,10),
        stacked=False,
        ax = axes[1]
        )



    
    

    
    
    bytes_image = io.BytesIO()
    plt.savefig(bytes_image,format='png')
    bytes_image.seek(0)
    return bytes_image
    
    
    
    
    
    
  