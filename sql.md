# SQL — From Basics to Expert

## String Functions & Pattern Matching
- **`length(str)`**: Returns the number of characters in a string.
  ```sql
  select tweet_id
  from Tweets
  where length(content) > 15;
  ```
- **`substr(col, start_index, len)`**: Extracts a substring (1-based indexing in SQL).
- **`concat(str1, str2, ...)`**: Concatenates multiple strings into one.
- **`upper(str)` & `lower(str)`**: Converts strings to upper or lower case.
  ```sql
  -- Capitalize first letter and lowercase the rest:
  select user_id, concat(upper(substr(name, 1, 1)), lower(substr(name, 2))) as name
  from Users
  order by user_id;
  ```
- **Pattern Matching (`LIKE`)**:
  - `%` represents zero, one, or multiple characters.
  - `_` represents exactly one single character.
  ```sql
  select *
  from Patients
  where conditions like '% DIAB1%' or conditions like 'DIAB1%';
  ```

---

## SQL Joins & Set Operations
- **`INNER JOIN`**: Returns records that have matching values in both tables.
- **`LEFT (OUTER) JOIN`**: Returns all records from the left table, and the matched records from the right table (unmatched columns are `NULL`).
- **`RIGHT (OUTER) JOIN`**: Returns all records from the right table, and the matched records from the left table.
- **`FULL (OUTER) JOIN`**: Returns all records when there is a match in either left or right table.
- **`CROSS JOIN`**: Cartesian product of two tables (every row in table A paired with every row in table B).
- **`SELF JOIN`**: A table joined with itself, essential for hierarchical data (e.g., employee to manager):
  ```sql
  select e.name as Employee, m.name as Manager
  from Employee e
  left join Employee m on e.manager_id = m.id;
  ```
- **`UNION` vs `UNION ALL`**:
  - `UNION`: Combines result sets of multiple queries and **removes duplicates** (requires expensive sort operation).
  - `UNION ALL`: Combines result sets **retaining all duplicates** (significantly faster; use unless deduplication is required).

---

## Window Functions
Window functions calculate aggregate values across a set of table rows that are related to the current row, without collapsing rows into a single output row (unlike `GROUP BY`).

### Ranking Functions
- **`ROW_NUMBER()`**: Unique sequential integer ($1, 2, 3, 4\dots$) assigned to each row within a partition.
- **`RANK()`**: Assigns identical ranks to ties, skipping subsequent ranks ($1, 2, 2, 4\dots$).
- **`DENSE_RANK()`**: Assigns identical ranks to ties without skipping subsequent ranks ($1, 2, 2, 3\dots$).
- **`NTILE(n)`**: Divides ordered rows into $n$ roughly equal buckets (e.g., percentiles, quartiles).

### Value / Navigation Functions
- **`LAG(col, offset, default)`**: Accesses data from a preceding row without a self-join (great for year-over-year growth).
- **`LEAD(col, offset, default)`**: Accesses data from a succeeding row.

### Example: Top K Salaries in Each Department
```sql
with RankedSalaries as (
    select
        d.name as Department,
        e.name as Employee,
        e.salary as Salary,
        dense_rank() over (partition by e.departmentId order by e.salary desc) as rnk
    from Employee e
    join Department d on e.departmentId = d.id
)
select Department, Employee, Salary
from RankedSalaries
where rnk <= 3;
```

### Cumulative Sums & Moving Averages
```sql
select
    transaction_date,
    amount,
    sum(amount) over (order by transaction_date rows between unbounded preceding and current row) as running_total,
    avg(amount) over (order by transaction_date rows between 6 preceding and current row) as rolling_7day_avg
from DailySales;
```

---

## Common Table Expressions (CTEs)
- **Standard CTE**: Improves readability and modularity over nested subqueries.
  ```sql
  with HighValueOrders as (
      select customer_id, sum(total_amount) as total_spent
      from Orders
      group by customer_id
      having sum(total_amount) > 10000
  )
  select c.name, hvo.total_spent
  from HighValueOrders hvo
  join Customers c on c.id = hvo.customer_id;
  ```
- **Recursive CTE**: Traverses hierarchical trees or graph relationships (e.g., organizational charts):
  ```sql
  with recursive OrgHierarchy as (
      -- Anchor member
      select id, name, manager_id, 1 as level
      from Employees
      where manager_id is null
      union all
      -- Recursive member
      select e.id, e.name, e.manager_id, o.level + 1
      from Employees e
      inner join OrgHierarchy o on e.manager_id = o.id
  )
  select * from OrgHierarchy order by level, manager_id;
  ```

---

## Indexing & Query Performance Optimization
- **B-Tree Indexes**: Standard index structure. Efficient for equality (`=`), range queries (`<`, `<=`, `>`, `>=`, `BETWEEN`), and prefix searches (`LIKE 'abc%'`).
- **Composite Indexes & The Leftmost Prefix Rule**:
  - An index on `(A, B, C)` can satisfy queries filtering on `(A)`, `(A, B)`, or `(A, B, C)`.
  - It **cannot** be used efficiently for queries filtering only on `(B)` or `(C)` without leading column `A`.
- **Covering Index**: An index that contains all columns requested by a query. Allows the database engine to satisfy the entire query from the index tree directly, bypassing expensive table/heap lookups.
- **Query Diagnostics (`EXPLAIN ANALYZE`)**:
  - Check for **Seq Scan** (Full Table Scan) vs **Index Scan** vs **Index Only Scan**.
  - High variance between estimated rows and actual rows indicates outdated table statistics; run `ANALYZE table_name;`.
- **Anti-Patterns that Invalidate Indexes**:
  - Applying functions to indexed columns: `WHERE YEAR(created_at) = 2026` $\to$ Fix: `WHERE created_at >= '2026-01-01' AND created_at < '2027-01-01'`.
  - Implicit type coercion: Comparing a `VARCHAR` column to an integer literal forces a full table scan.
  - Leading wildcard searches: `WHERE name LIKE '%john'` cannot use a standard B-Tree index.

---

## Transactions & ACID Isolation Levels
- **ACID Guarantees**:
  - **Atomicity**: All changes succeed or entire transaction rolls back.
  - **Consistency**: Database transitions only from one valid state to another valid state adhering to constraints.
  - **Isolation**: Concurrent transactions execute without interfering with one another.
  - **Durability**: Committed data survives system crashes and power failures (persisted via WAL - Write-Ahead Logging).
- **Transaction Isolation Levels**:
  | Isolation Level | Dirty Read | Non-Repeatable Read | Phantom Read |
  | :--- | :---: | :---: | :---: |
  | **Read Uncommitted** | Possible | Possible | Possible |
  | **Read Committed** (Default in PG) | Prevented | Possible | Possible |
  | **Repeatable Read** (Default in MySQL) | Prevented | Prevented | Possible (PG prevents via MVCC) |
  | **Serializable** | Prevented | Prevented | Prevented |

- **Concurrency Anomalies Explained**:
  - **Dirty Read**: Transaction A reads uncommitted changes made by Transaction B (which may roll back).
  - **Non-Repeatable Read**: Transaction A reads a row, Transaction B modifies/deletes that row and commits, Transaction A re-reads and sees different values.
  - **Phantom Read**: Transaction A reads rows matching a range condition, Transaction B inserts new rows matching that condition and commits, Transaction A re-executes query and sees new "phantom" rows.
- **MVCC (Multi-Version Concurrency Control)**: Modern databases (PostgreSQL, MySQL InnoDB) use MVCC so readers do not lock writers, and writers do not lock readers. Each row holds transaction visibility timestamps (`xmin`/`xmax`).
