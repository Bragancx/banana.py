# banana.py 🍌
Banana turns more easily yet to connect to your database.

- Follow the idea of ruby on rails methods.
- Each table is a function.
- Easily understing and clean code.

## Full example of how to use.

### How to setup the connection?

It's easy to setup, just pass a dictionary with the connection parameters.
Like below:

```
conn = {
    "host": "xxx",
    "database": "xxx",
    "username": "xxx",
    "password": "xxx"
}

banana = Banana(conn)
```

### Doing a SELECT
To do a select is quite simple too.

All the tables are called like functions so, imagine you have a 
table called "bananas_list", so, the select will look like this:
```
select = banana.BananasList().execute()
print(select)
```

The "execute()" is the signal to execute the query and return it.

This will print the result following this structure:
```
[
    {}, # Row
    {}, # Row
    {}, # Row
]
```
Each dictionary means one row.

### Doing a INSERT

```
data = {
    "name": "Banana",
    "quantity": 35
}

insert = banana.BananasList().insert(data).execute()
print(insert) # Prints the id of the row we inserted as array.
```

But this doesn't commit automatically!
WHY? Performance!
It's much more performatic you set all your inserts and do a commit.

Command to do the commit:
```
banana.commit()
```

### Doing a UPDATE

It's very similar to the insert:
```
data = {
    "name": "Not banana",
    "quantity": 1
}

update = banana.BananasList().update(data).execute()
print(update) # Prints the id of the row we updated as array.
```

This doesn't do the commit automatically too.
This will updated every single row in your table, so, we need a "WHERE", and there he's:
```
update = banana.BananasList().update(data).where("ID > 0","ID < 2").execute()
```
You can pass mutliples conditions as string, if you want to use "OR" condition do it in a single condition:
```
update = banana.BananasList().update(data).where("ID > 0 or ID < 2").execute()
```

### Doing a DELETE

To delete a value you will need to just pass the ids of the row:
```
delete = banana.BananaList().delete(1,2,3).execute()
print(delete) # Print an empty array.
```

Quite simple, huh?!

### Other methods

#### Ordering

Like ".where()" you can pass order following the same idea:
```
select = Banana.BananasList().order("id DESC", "name ASC").execute()
print(select) # Prints the select correctly ordered.
```

#### Find

You can use the method "find" to search to one row by her id, like:
```
find = Banana.BananasList().find(1).execute()
print(find) # Prints an array with one row.

# OUTPUT
# [ {} ]
```


