- length() function: returns the number of characters in a string
```
select tweet_id
from Tweets
where length(content) > 15;
```
- substr(col, start_index, len) : 1 based indexing
- concat(str1, str2)
- upper(), lower()
```
select user_id, concat(upper(substr(name, 1, 1)), lower(substr(name, 2))) as name
from Users
order by user_id;
```
