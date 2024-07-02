- length() function: returns the number of characters in a string
```
select tweet_id
from Tweets
where length(content) > 15;
```
