"""chess_project_off

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1IhBgnr7kWJsKjIzSYmsnybaDBvefP8lG
"""

import os
import math
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import sklearn as skl
import statsmodels.api as sm
import streamlit as st

st.title('**:chess_pawn: Checkmated by Data :chess_pawn:**')

#INTRODUTCION
st.subheader('Introduction')
"""This project wants to explore the world of chess using this data set:

https://www.kaggle.com/datasets/datasnaek/chess

The goal of this study is to analyse how much starting first (having the white pieces) affects the game's victory probability and whether this effect, 
in games with more turns, is more or less impactful.
\nIn addition, it will also be investigated which opening moves are most frequently used and also those that most frequently lead to a win.  """

#SECTION A
st.subheader('A. Data-set presentation')

#GENERAL INFO SUBSECTION
with st.expander('**General informations**'):
    """
    This data-set groups data from more than 20,000 games collected from a selection of users on the site Lichess.org. This set contains:
    *  Game ID;
    *  Rated (Boolean value);
    *  Start Time;
    *  End Time;
    *  Number of Turns;
    *  Game Status;
    *  Winner;
    *  Time Increment;
    *  White Player ID;
    *  White Player Rating;
    *  Black Player ID;
    *  Black Player Rating;
    *  All Moves in Standard Chess Notation;
    *  Opening Eco (Standardised Code for any given opening, list here);
    *  Opening Name;
    *  Opening Ply (Number of moves in the opening phase);
    """
    chess_df = pd.read_csv(r"C:\Users\murar\Desktop\chess_project_off\chess.csv")

    #BUTTON FOR ORIGINAL DS
    if st.checkbox('SHOW DATASET'):
        chess_df    
    
    """Below can be seen a summary of statistical proprieties of the data-set"""
    #BUTTON FOR CHESS_DF.DESCRIBE()
    if st.checkbox('SHOW SUMMARY OF STATISTICAL PROPERTIES'):
        st.write(chess_df.describe())


#DATA HANDLING SUBSECTION
with st.expander('**Data handling**'):

    chess_df_backup = chess_df.copy() #BACKUP OF ORIGINAL DS

    """All the columns that will not be used are dropped and two new columns are added:"""
    """* **"white_win"** : equals 1 if winner it's white player, 0 otherwise;"""
    """* **"black_win"** : equals 1 if winner it's black player, 0 otherwise.
    """
    #DROOPING UNNECESSARY COLUMNS AND ADDED NEW ONES 
    chess_df.drop(['moves', 'white_id', 'black_id', 'id', 'created_at', 'last_move_at', 'rated'], axis=1, inplace = True )
    chess_df['white_win'] = ( chess_df['winner'] == 'white' ) * 1
    chess_df['black_win'] = ( chess_df['winner'] == 'black' ) * 1

    "Now the data-set looks like this: "

    #SHOWING UPDATED DS
    if st.checkbox('SHOW UPDATED DATASET'):
        chess_df


#GENERAL CORRELATION SUBSECTION
with st.expander('**General correlation**'):    

    """Here you can see the **correlation graphs** of the numerical variables in the data set:"""

    chess_corr_df = chess_df.drop(['victory_status', 'winner', 'increment_code', 'opening_eco', 'opening_name'], axis=1, inplace = False )
    chess_corr = chess_corr_df.corr()

    col_1, col_2, col_3 = st.columns([0.15, 0.7, 0.15])

    #PLOTTING CORRELATION GRAPH
    with col_2:
        fig_corr, ax = plt.subplots(figsize=(8, 6))  
        sb.heatmap(chess_corr, annot=True)  
        st.pyplot(fig_corr)

    """As a first impression, the only parameters that seems to have a little correlation are:"""

    """-    __white_rating and black_rating:__ positive correlation, this is because matchmaking software matches opponents with similar ratings."""
    """-   __white_win and black_win:__ negative correlation, obviously because if one player win, then the other loose. The correlation is not -1 because there can be some draws."""


#SECTION B
st.subheader("B. Which are the most common matches outcomes? What are the most played type of matches?")

#OUTCOMES SUBSECTION
with st.expander("**Most common matches outcomes**"):

    endgame_reason_df = chess_df['victory_status'].value_counts()
    """The pie-chart of the end-game reasons looks like this:"""
    #CREATING ENDGAME REASON PIE CHART
    fig_outcomes, ax = plt.subplots(figsize=(4.5, 4.5))
    plt.pie(endgame_reason_df, labels = endgame_reason_df.index, autopct = '%i%%')
    plt.title('DISTRIBUTION OF ENDGAME REASON ', fontdict={'fontsize':'10'})
    
    col_4, col_5, col_6 = st.columns([0.15, 0.7, 0.15])
    
    #PLOTTING ENDGAME REASON PIE CHART
    with col_5:
        st.pyplot(fig_outcomes)

    """It's easy to see that the most endgame reason is "resign" followed by "checkmate" while "draw" and "out of time" are widely less frequent."""

#TYPE OF MATCHES SUBSECTION
with st.expander("**Most played type of matches**"):

    """It's generated a data frame of the most played type of matches. 
    The type of matches played less than 2% (of the total 20.000+ matches) are grouped with index 'other'. The plot of this df looks like this:"""

    most_played_mask = chess_df['increment_code'].value_counts() > chess_df['increment_code'].value_counts().sum() * 0.02
    most_played_df = chess_df['increment_code'].value_counts()[most_played_mask]
    other = chess_df['increment_code'].value_counts().sum()- most_played_df.sum()
    other_dict={'other':other}
    other_series = pd.Series(other_dict)
    all_type_df = most_played_df._append(other_series, ignore_index= False)

    #CREATING MOST PLAYED TYPE OF MATCHES
    fig_most_played, ax = plt.subplots(figsize = (6,6))
    explode = (0.04, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    plt.pie(all_type_df, labels = all_type_df.index, explode = explode, autopct = '%i%%')
    plt.title('Most played type of matches', fontdict={'fontsize':'10'})
    
    col_7, col_8, col_9 = st.columns([0.15, 0.7, 0.15])
    
    #PLOTTING ENDGAME REASON PIE CHART
    with col_8:
        st.pyplot(fig_most_played)
    
    """It's higlited that the most frequently played match type is the '10+0'. All other types are definitely less played."""


#SECTION C
st.subheader("C. Is there some correlation between starting with white pieces and the outcome of the match?")

with st.expander("**Which player wins more matches?**"):
    """As we can see in the following charts, white players have few more wins (10.001) than black ones (9.107) but the difference is very small: only 894 matches (4%)."""

    winner_df = chess_df['winner'].value_counts()

    #DISTRIBUTION CHART
    fig_oc, ax = plt.subplots(figsize=(3.7,4))
    plt.bar(winner_df.index, winner_df, color = ('skyblue', 'pink', 'red'), edgecolor = 'black')
    plt.title('Distribution of matches outcomes', fontdict={'fontsize':'10'})
    #PIE CHART
    fig_ocp, ax = plt.subplots(figsize=(6,4))
    plt.pie(winner_df, labels = winner_df.index, autopct = '%.1f%%', colors = ('skyblue', 'pink', 'red'))
    plt.title('Pie-chart of matches outcomes')

    col_10, col_11, col_12 = st.columns(3) 
    
    with col_10:
        #CHECKBOX FOR WINNER DISTRIBUTION CHART
        if st.checkbox('SHOW DISTRIBUTION OF WINNING PLAYER'):
            st.pyplot(fig_oc)
    
    with col_11:
    ##CHECKBOX FOR WINNER DISTRIBUTION PIE
        if st.checkbox('SHOW WINNING PLAYER PIE CHART'):
            st.pyplot(fig_ocp)
        
    with col_12:
        ##CHECKBOX FOR WINNER DISTRIBUTION DF
        if st.checkbox('SHOW WINNING PLAYER DF'):
            winner_df
    
    
            
    difference = chess_df['winner'].value_counts()['white']-chess_df['winner'].value_counts()['black']
    difference_pct = int((chess_df['winner'].value_counts('pct')['white']-chess_df['winner'].value_counts('pct')['black'])*100)
    

with st.expander('**How the situation changes when matches became longer in terms of number of turns?**'):
    """
    Here will be analyzed if the difference get bigger or smaller when matches have higher or lower number of turns. 
    Matches with 79 or more turns (75% of turns distribution) will be considered many-turns matches and matches with 37 
    or less turns (25% of turns distribution) will be considered few-turns matches.
    """

    many_turns_matches_mask = chess_df ['turns'] >= 79
    many_turns_matches_df = chess_df[many_turns_matches_mask]
    mtm_winner_df = many_turns_matches_df['winner'].value_counts()

    few_turns_matches_mask = chess_df ['turns'] <= 37
    few_turns_matches_df = chess_df[few_turns_matches_mask]
    ftm_winner_df = few_turns_matches_df['winner'].value_counts()

    """***MANY-TURNS MATCHES***"""
    
    """It can be noticed that the percentage of white winning in many-turns matches (1%) is decreased compared to the original data set matches (4%)."""
    
    #DISTRIBUTION CHART
    fig_ocmtd, ax = plt.subplots(figsize=(4.3,4))
    plt.bar(mtm_winner_df.index, mtm_winner_df, color = ('skyblue', 'pink', 'red'), edgecolor = 'black')
    plt.title('Distribution of many-turns matches outcomes', fontdict={'fontsize':'10'})
    
    #PIE CHART
    fig_ocmtp, ax = plt.subplots(figsize=(6,4))
    plt.pie(mtm_winner_df, labels = mtm_winner_df.index, autopct = '%.1f%%', colors = ('skyblue', 'pink', 'red'))
    plt.title('Pie-chart of many-turns matches outcomes')
    
    col_13, col_14, col_15 = st.columns(3) 
    
    with col_13:
        #CHECKBOX FOR WINNER DISTRIBUTION CHART
        if st.checkbox('SHOW CHART WITH MANY TURNS'):
            st.pyplot(fig_ocmtd)

    with col_14:
        #CHECKBOX FOR WINNER DISTRIBUTION CHART
        if st.checkbox('SHOW PIE CHART WITH MANY TURNS'):
            st.pyplot(fig_ocmtp)
                
    with col_15:
        #CHECKBOX FOR WINNER DISTRIBUTION DF
        if st.checkbox('SHOW DF WITH MANY TURNS'):
            mtm_winner_df
    

    difference =mtm_winner_df['white']-mtm_winner_df['black']
    difference_pct = round((many_turns_matches_df['winner'].value_counts('pct')['white']-many_turns_matches_df['winner'].value_counts('pct')['black'])*100)


    """***FEW-TURNS MATCHES***"""

    difference = ftm_winner_df['white']-ftm_winner_df['black']
    difference_pct = round((few_turns_matches_df['winner'].value_counts('pct')['white']-few_turns_matches_df['winner'].value_counts('pct')['black'])*100)

    #DISTRIBUTION CHART FEW
    fig_ocftd, ax = plt.subplots(figsize=(3,4))
    plt.bar(ftm_winner_df.index, ftm_winner_df, color = ('skyblue', 'pink', 'red'), edgecolor = 'black')
    plt.title('Distribution of few-turns matches outcomes')
    
    #PIE CHART FEW
    fig_ocftp, ax = plt.subplots(figsize=(6,4))
    plt.pie(ftm_winner_df, labels = ftm_winner_df.index, autopct = '%.1f%%', colors = ('skyblue', 'pink', 'red'))
    plt.title('Pie-chart of few-turns matches outcomes')
    
    """By contrast, the percentage of white winning in the few-turns matches DF is increased (13%) as you can see in the following charts: """

    col_16, col_17, col_18 = st.columns(3) 
    
    with col_16:
        #CHECKBOX FOR WINNER DISTRIBUTION CHART
        if st.checkbox('SHOW CHART WITH FEW TURNS'):
            st.pyplot(fig_ocftd)

    with col_17:
        #CHECKBOX FOR WINNER DISTRIBUTION CHART
        if st.checkbox('SHOW PIE CHART WITH FEW TURNS'):
            st.pyplot(fig_ocftp)
                
    with col_18:
        #CHECKBOX FOR WINNER DISTRIBUTION DF
        if st.checkbox('SHOW DF WITH FEW TURNS'):
            ftm_winner_df
    """From these pie-charts, can also be noticed that the percentage of draws increase in many-turns matches."""

with st.expander ('**Regression model**'):

    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn import metrics
    from sklearn.metrics import classification_report
    from sklearn.metrics import confusion_matrix

    """Two new DFs are generated: one collect the victory percentage of the black player and the other of the white depending on the value of variable "turns"."""

    white_win_mask = chess_df['winner'] == 'white'
    white_win_df = chess_df[white_win_mask]
    black_win_mask = chess_df['winner'] == 'black'
    black_win_df = chess_df[black_win_mask]

    ww_turns_pct = white_win_df['turns'].value_counts() / chess_df['turns'].value_counts()
    bw_turns_pct = black_win_df['turns'].value_counts() / chess_df['turns'].value_counts()

    """These two DFs are plotted:"""

    """*   Blue points reports white players win"""
    """*   Pink points reports black players win"""
    col_19, col_20 = st.columns(2)
    
    #WHITE WIN SCATTER
    fig_ws, ax = plt.subplots(figsize = (8,4))
    plt.scatter(ww_turns_pct.index, ww_turns_pct, c = 'skyblue')
    plt.title('Distribution of white winning percentage related to number of turns')

    #BLACK WIN SCATTER
    fig_bs, ax = plt.subplots(figsize = (8,4))
    plt.scatter(bw_turns_pct.index, bw_turns_pct, c = 'pink')
    plt.title('Distribution of black winning percentage related to number of turns')

    #COMBINED SCATTER
    fig_comb_scat, ax = plt.subplots(figsize = (12,5))
    plt.scatter(ww_turns_pct.index, ww_turns_pct, c = 'skyblue')
    plt.scatter(bw_turns_pct.index, bw_turns_pct, c = 'pink')
    plt.title('Combination of the two previous graphs ')

    with col_19:
        #CHECKBOX FOR WHITE WIN SCATTER
        if st.checkbox('SHOW WHITE WIN SCATTER'):
            fig_ws
    
    with col_20:
        #CHECKBOX FOR BLACK WIN SCATTER
        if st.checkbox('SHOW BLACK WIN SCATTER'):
            fig_bs
    
    #CHECKBOX FOR COMBINED WIN SCATTER
    if st.checkbox('SHOW COMBINED SCATTER'):
        fig_comb_scat


    """These graphs show that there is no definite pattern but, it can be noticed that there are many values at the extremes, this is because white usually win in an odd-numbered round, while black in an even-numbered round."""

    """For this reason is much interesting studying the ***distribution of draws***. 
    In order to do that two new columns are introduced in the data set:"""

    """*   "draws": boolean value that is worth 1 if the match is a tie and 0 if it is not;"""
    """*   "rating_diff" : indicates the rating difference between the two players in absolute value;"""  

    """It's also generated a new DF ("draw_turns_pct") that collects the percentage of draws per number of turns. 
    The scatter plot of this new DF looks as follows: """

    draw_mask = chess_df['winner'] == 'draw'
    draw_df = chess_df[draw_mask]

    chess_df ['draw'] = draw_mask * 1
    chess_df ['rating_diff'] = abs (chess_df['white_rating'] - chess_df ['black_rating'])

    draw_turns_pct = draw_df['turns'].value_counts() / chess_df['turns'].value_counts()

    #DRAWS SCATTER
    fig_dtpct, ax = plt.subplots(figsize = (10,4))
    plt.scatter(draw_turns_pct.index, draw_turns_pct, c = 'red')
    plt.title('Distribution of draws percentage related to number of turns ')

    #CHECKBOX FOR COMBINED WIN SCATTER
    if st.checkbox('SHOW DRAWS PCT PER TURNS SCATTER'):
        fig_dtpct


    """It seems to be an exponential distribution
    yp = f(xp) defined with the following code:
    """
    #REPORTING CODE FOR EXPONENTIAL CURVE
    st.code("""kp = np.log(2) / 250
    xp = np.linspace(0, 250, 10000)
    yp = 0.2 * np.exp(0.0075 * xp) - 0.2""")
    
    kp = np.log(2) / 250
    xp = np.linspace(0, 250, 10000)
    yp = 0.2 * np.exp(0.0075 * xp) - 0.2
    
    fig_dce, ax = plt.subplots(figsize = (10,4))
    plt.scatter(draw_turns_pct.index, draw_turns_pct, c = 'red')
    plt.plot(xp, yp)
    plt.xlim(0, 260)
    plt.ylim(-0.1, 1.1)
    plt.title('Distribution of draws percentage related to number of turns ')

    #CHECKBOX FOR COMBINED DRAW SCATTER AND EXPONEnTIAL
    if st.checkbox('SHOW COMBINED PLOT'):
        fig_dce

    """At this point, it's generated a logit model that studies the influence of number of turns and rating difference between the two players on the probability of a draw."""

    variables = ['turns', 'rating_diff']
    x = chess_df[variables]
    y = chess_df['draw']

    x_train_chess_df, x_test_chess_df, y_train_chess_df, y_test_chess_df = train_test_split(x, y, test_size = 0.5, random_state = 5)

    model = sm.MNLogit(y_train_chess_df, sm.add_constant(x_train_chess_df))
    result = model.fit()
    stats = result.summary()
    
    #CHECKBOX FOR LOGIT MODEL
    if st.checkbox('SHOW REGRESSION MODEL'):
        stats    
    """It can be noticed that 'turns', as expected has a positive coefficent, while 'rating_diff' has negative coefficent, as we could immagine."""

st.subheader("D. What are the best opening moves for white player? And for black one?")

with st.expander('**Data-set adaptation**'):

    """Two new DataFrames are generated: the first goups the most common openings when white player wins and the second is the same but 
    for matches in wich black player is the winner (only openings that have been used at least 2% of the considered matches are analyzed).
    """
    #GENERATING DF
    common_openings_white_win_mask = white_win_df['opening_eco'].value_counts('pct') > 0.02
    co_white_win_df = white_win_df['opening_eco'].value_counts()[common_openings_white_win_mask]
    co_white_win_pct_df = co_white_win_df / co_white_win_df.sum()
    common_openings_black_win_mask = black_win_df['opening_eco'].value_counts('pct') > 0.02
    co_black_win_df = black_win_df['opening_eco'].value_counts()[common_openings_black_win_mask]
    co_black_win_pct_df = co_black_win_df / co_black_win_df.sum()

    #PLOTTING DFs
    col_21, col_22, col_23, col_24 = st.columns(4)
    with col_22:
        if st.checkbox('SHOW WHITE DF'):   
            co_white_win_pct_df

    with col_23:
        if st.checkbox('SHOW BLACK DF'):
            co_black_win_pct_df

    """Now, in order to compare white and black best opening moves, it's generated a new DF as follows:"""

    #GENERATING DF
    delta = co_black_win_df - co_white_win_df
    delta.fillna(co_black_win_df, inplace = True)
    delta.fillna(co_white_win_df, inplace = True)
    delta_pct = delta / (co_black_win_df + co_white_win_df)
    delta_pct.fillna(delta / co_black_win_df, inplace = True)
    delta_pct.fillna(delta / co_white_win_df, inplace = True)
    
    #PLOTTING DF
    col_25, col_26, col_27 = st.columns(3)
    
    with col_26:
        if st.checkbox('SHOW DELTA DF'):
            delta_pct

with st.expander('**Plots and analysis**'):

    """Here you can see the plots of most common openings when white and black player win"""

    fig_cow, ax = plt.subplots(figsize = (10,4))
    plt.bar(co_white_win_pct_df.index, co_white_win_pct_df, color = ('skyblue'), edgecolor = 'black')
    plt.title('Most common openings when \nWHITE player wins', fontdict={'fontsize':'20'})

    if st.checkbox('SHOW WHITE PLAYER CHART'):
        st.pyplot(fig_cow)
    """This bar-chart shows that the distribution of opening moves is quite regular: the frequencies of C00, A00, C41, B00, B01, D00 and A40 are very close."""

    fig_cob, ax = plt.subplots(figsize = (10,4))
    plt.bar(co_black_win_pct_df.index, co_black_win_pct_df, color = ('pink'), edgecolor = 'black')
    plt.title('Most common openings when \nBLACK player wins', fontdict={'fontsize':'20'})

    if st.checkbox('SHOW BLACK PLAYER CHART'):
        st.pyplot(fig_cob)

    """In this case, howevere, the distribution has a peak in A00, but then it's quite regular."""

    """Below it's plotted the chart of delta percentage of winning related to each opening move-set between the two players.
    This bar-chart must be read as follows:"""


    """*   positive values refear to good openings for black player;"""
    """*   negtive values refear to good openings for white player."""

    """(Example: B00: -0,25 indicates that in a match that has B00 as opening, white has a 25% greater chance of winning than black.)"""
    fig_comb_delta, ax = plt.subplots(figsize = (10,4))
    plt.bar(delta_pct.index, delta_pct, color = ('lightgreen'), edgecolor = 'black')
    plt.title('Delta of best opening moves', fontdict={'fontsize':'20'})
    
    if st.checkbox('SHOW COMBINED DELTA CHART'):
        st.pyplot(fig_comb_delta)
    """**NOTE:** C40 can be considered the best opening move for black player with an efficency of almost 100%. This happens because C40 is rarely linked to 
    a victory by the white player, so it recived a FALSE boolean value in the "common_opening_white_win_mask"."""

    """From this DF will be removed all the values under 10%: these openeing moves are considered only because they are quite frequently used 
    but they are not linked to a significant difference of winning probability."""
    #REMOVING NOT SIGNIFICANT VALUES
    significant_mask = abs(delta_pct) > 0.1
    significant_delta = delta_pct[significant_mask]

    #CHECKBOX FOR SIGNIFICANT DELTA PCT
    if st.checkbox('SHOW SIGNIFICANT DELTA DF'):
        significant_delta


    #PLOTTING SIGNIFICANT DELTA PCT
    fig_sig_delta, ax = plt.subplots(figsize = (10,4))
    plt.bar(significant_delta.index, significant_delta, color = ('green'), edgecolor = 'black')
    plt.title('Delta of significant best opening moves', fontdict={'fontsize':'20'})

    if st.checkbox('SHOW SIGNIFICANT DELTA CHART'):
        st.pyplot(fig_sig_delta)

    """This graph highlites that:"""

    """*   **C40** is the best opening move for black player, but also **A00** and **B20** will probably lead to a win;"""
  
    col_28, col_29, col_30, col_31, col_32, = st.columns(5)
  
    #BUTTONS FOR OPENINGS LINK
    with col_28:
            st.link_button('LOOK AT A00', 'https://chessopenings.com/eco/A00/1/')
    
    with col_30:
            st.link_button('LOOK AT B20', 'https://chessopenings.com/eco/B20/1/')
    with col_32:
        st.link_button('LOOK AT C40', 'https://chessopenings.com/eco/C40/1/')
    
    """*   **A40**, **B00** and **C41** are the best opeing options for white player."""
   
    col_33, col_34, col_35, col_36, col_37, = st.columns(5)
   
    #BUTTONS FOR OPENINGS LINK
    with col_33:
        st.link_button('LOOK AT A40', 'https://chessopenings.com/eco/A40/1/')
    
    with col_35:
            st.link_button('LOOK AT B00', 'https://chessopenings.com/eco/B00/1/')
    
    with col_37:
            st.link_button('LOOK AT C41', 'https://chessopenings.com/eco/C41/1/')

    
st.subheader('E. Data-set download and conclusions ')

#DATA SET DOWNLOAD

with st.expander('**Download final DS**'):
    
    """Here can be downloaded the final dataset (with all the added columns and without the dropped ones) clicking on the dounload button below."""
    def dl_ds (ds):
        return ds.to_csv().encode('utf-8') 

    st.download_button('DOWNLOAD FINAL DATA-SET', dl_ds(chess_df), file_name = 'chess_ds.csv')

with st.expander('**Final statements**'):
    """In conclusion, according to the results of this study, it can be stated that: """
    """* moving first slightly favours the white player but this effect is less pronounced as the number of turns increases (the number of draws increases exponentially). 
    This happens because chess is a game which tends to be fair to both players;"""
    """* the increase rating difference between the two players implies a slight decrease on the probability of a draw;"""
    """* **C40**, **A00** and **B20** can lead more probably to a black player win;"""
    """* **A40**, **B00** and **C41** can lead more probably to a white player win."""