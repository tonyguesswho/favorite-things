## Deliverables Timeline

1.  How long did you spend on the coding test below?
    
    I spent 22hours on the coding test. Here is breakdown of the time management from Thursday.
    - Thursday - 4hours
    - Friday - 6hours
    - Saturday - 4hours
    - Sunday - 4hours
    - Monday - 4hours

2.  What would you add to your solution if you had more time?
    
    - Authentication: 
        The authentication workflow would work as follows:

        1. Client provides email and password, which is sent to the server
        2. Server then verifies that email and password are correct and responds with an auth token
        3. Client stores the token and sends it along with all subsequent requests to the API
        4. Server decodes the token and validates it
        5. This cycle will repeats until the token expires or is revoked. In the latter case, the server issues a new token.

    - User Administration & Account Management

        Seeing that different users will have their accounts provisioned and manage their Favorites differently. I will also design the application to manage the Signing up of Users.

    - Manage Attributes under each category

        Currently, the user specifies the extra attributes when creating a favorite thing. But managing it under each category will create room for consistency across favorite things.

## Most Useful feature in Python3.6/Flask latest version

1.  Python

    - String interpolation: This is another option to format strings called Formatted String Literals. This feature lets you use embedded Python expressions inside string constants. This was used in all the model_string_representation methods for all the model/ORM classes, i.e. `models.py`
        ```
        class Category(BaseModel):
            ....
            
            def __repr__(self):
                return f'<Category: {self.name}>'
        ```

        ```
        class Audit(BaseModel):
            ....
            
            def __repr__(self):
                return f'<Audit on {self.resource_type}>'
        ```

        ```
        class Favorite(BaseModel):
            ....

            def __repr__(self):
                return f'<Favorite: {self.title}>'
        ```


## Tracking Performance issue on Production

-   Experience with Seegad
    I worked with the team that built Seegad, where like every growing application, we run into interesting performance problems. The application and its dependent services was deployed to DigitalOcean, where you have a static allocation of server resources unless you make a request for more. That causes most issues when you application ought to auto-scale and this has its own natural problems. We have ran into some interesting issues in production which I will highlight two most challenging ones and how we solved them.

    1. Requests taking too long:
    The first challenge with this was that we were in a situation of `If You Can’t Measure It, You Can’t Manage It`. We had no way to profile our application and so I had to work with the team to setup an application monitoring and profiling system. We had different options but we went for ELK (Elastic Search, Logstash and Kibana) stack for the APM and cProfile for the application profiling. Once these were provisioned we were able to see the performance data of the application against the defined metrics.
    This gave us insight into how the frontend and backend APIs were performing and bottlenecks that were making requests take longer to process. At the end of this, we had a per-request log which helped us to identify and fix the following issues:

    -   Reducing the number of times some endpoints were being called as this had a negative impact on our limited server       resources
    -   Too many joins table in our queries and other inefficient queries
    -   Employed the use of Python Generators when dealing with running a logic through a large set of database records.        This helped us reduce both the average time complexity as well as the memory footprint of the logic.
    -   Converted some huge tasks that does not require a user feedback to scheduled tasks using Redis as the Message           Broker and Celery as the task runner.
    -   Replacing some forloops with list comprehension

