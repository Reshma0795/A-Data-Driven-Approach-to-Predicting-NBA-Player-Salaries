# Introduction
The National Basketball Association (NBA) is one of the most famous sports franchises in the world. As of today, this professional basketball league is composed of 30 teams in North America, with more than 500 players playing each year. As of 2020, NBA players are the world’s best paid athletes by average annual salary per player. This project presents a data-driven approach to predicting the salaries of NBA players based on various factors, such as their performance statistics, team dynamics, and market trends. 

I collected a comprehensive dataset of NBA players and their salaries from the past several seasons, along with their corresponding performance metrics and other relevant features. I then used machine learning techniques to train and evaluate several models to predict player salaries.

This project can be useful for NBA teams, agents, and fans who are interested in understanding and predicting the salaries of players, as well as for data scientists and machine learning enthusiasts who are interested in applying their skills to a real-world problem.

# Objective
This project will explore how to use each NBA player’s performance to determine the player’s annual salary.

# Methodology
The method I have used in this project is divided in 3 parts:

## Part A : Web Scraping
In part A, I have scraped data from www.basketballreference.com where I grab information of all NBA players who were active during the 2009/2010 season to the 2020/21 season. Assuming the "most current season" as the 2020/2021 season as the data may not be complete for recent seasons. 

## Part B : Data Preparation and Description
In this second part, I load the data in Python and describe and explore the data.

## Part C : Data Analytics
In this section, I perform data analytics techniques on the prepared data set, and justify and interpret the model.

## Results
From the analysis conducted, I have identified the factors that are important to the player salary. 

These are 
1) Mins_Played_per_game
2) TRPG = Total_Rebounds_per_game
3) APG = Assists_per_game
4) SPG=Steals_per_game
5) BPG = Blocks_per_game
6) TPG = Turnovers_per_game
7) PFPG = Personal_Fouls_per_game
8) PPG = Points_per_game
9) EXP=Experience
10) PER=Player Efficiency Rating

Higher salary is an indication of better performance. Hence, we get a consolidated wisdom about the performance of the players which helps to decide on the acquisition or retention of the players in the team and thus contributing to the overall revenue of the team.
