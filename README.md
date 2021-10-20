# chatbot_douban

Chatbot from scratch based on douban movie, support with chat and recommendation.

A website based functionality that support user to chat with our bot, also our bot will try to recommend users with unseen movies.

Full functionanlity:

1. A website user could login.
2. A chatbot form will be displayed for user to text.
3. Basic chat text will be made for users to start chat.
4. First check users have seen any hot movies with multiple selection, full data will be stored into database, will repeat until user don't want to select.
5. User could chat with bot that for movies', actors', or directors' information.
6. User could get more movies for actors or directors based on basic information
7. Try to reach user to see is a need to do recommendation, user could select to agree or don't agree with recommendation, if a good or not signal also will be stored for future adjustment.


There are 2 models will be made: one for chatbot and another for recommendation.


Technology used:
1. NLP for processing
2. MYSQL to persist structure data and mongoDB to store movie data
3. Flask for front end
4. Graph SQL used in case for movies information
5. HTML and JS for front end, both login and chat page
6. Chatbot model created for chat
7. Recommendation model for users' future interest.


Functionality split into parts:
1. Data extract from website with spider for movies, also try to with actors.
2. Create DB strcuture and dump data into DB.
3. Whether or not to use Graph DB? to be decided
4. Front end for user to login and store users' information
5. Chat form for website that user could text in the box.
6. Extract hot movies to be selected based on 5 movies each time for user to select, both with agree or stop, if there isn't movie selected, then couldn't do recommendation, try to let user to select again.
7. Chatbot model that support to do interaction with users.


Tools used:
MYSQL
MongoDB
BeautifulSoup

