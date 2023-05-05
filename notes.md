# Notes I take while doing this project.

### I followed the [DigitalOcean SQLAlchemy Tutorial](https://www.digitalocean.com/community/tutorials/how-to-use-flask-sqlalchemy-to-interact-with-databases-in-a-flask-application) when working on this project.

## Table of contents
- [Content Notes](#content-notes)
  - [General notes](#general-notes)
  - [How to use SQLAlchemy](#how-to-use-sqlalchemy)
- [Future Development](#future-development)


## Content notes:

### General notes

Note: To open flask shell type `flask --app main shell`.

Note:
The db.create_all() function does not recreate or 
update a table if it already exists. For example, 
if you modify your model by adding a new column, 
and run the db.create_all() function, the change 
you make to the model will not be applied to the 
table if the table already exists in the database. 
The solution is to delete all existing database tables
with the db.drop_all() function and then recreate them 
with the db.create_all() function like so:

```python
>>> db.drop_all()
>>> db.create_all()
```

The only problem is that this will delete all the data.
To upgrade with saving data we have to use <i>schema migration</i>.
We can use `Flask-Migrate` extension.


### How to use SQLAlchemy:
1. Configure a database
2. Make a table model Class
3. Make an object of the above Class
4. Add the object to the database session 
`db.session.add(obj)`
5. Commit the session `db.session.commit()`
6. To view the database we query the model class
`Class.query.all()`


### How to get items form the database:
- To get specific records
     `Class.query.filter_by(attribute=value).all()`
- Get by primary key
      `Class.query.get(1)` (id is the key in this case)

## Future development
I can make a form that takes in a movie name.
Then I would pass the POST request and search for the 
movie in the database. Return the list of movies that have
matching words with the request.    

Can add a feature that allows a user to `add` a movie
from the external database to their list. This would
utilize some movie database API.

List movies in the order ranked.

List movies by the release date.


Get movies from the database. Store user's saved movies by the 
id refereces from the API database. Store id:user_rating:user_description.
Display the list of user movies. Display the movis in order ranked.
