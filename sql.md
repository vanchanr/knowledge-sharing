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
- col `like` pattern
- % represents zero, one, or multiple characters
- _ represents one, single character
```
select *
from Patients
where conditions like '% DIAB1%' or conditions like 'DIAB1%';
```
- [find employees with top k salaries in each department](https://leetcode.com/problems/department-top-three-salaries)
```
select Department.name as Department, e1.name as Employee, e1.salary as Salary
from Employee e1
join Department
on e1.departmentId = Department.id
where (
    select count(distinct(e2.salary))
    from Employee e2
    where e2.departmentId = e1.departmentId and e2.salary > e1.salary
) <= 2;
```

- other topics: self join
