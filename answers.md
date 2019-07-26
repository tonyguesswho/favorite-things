## Deliverables Timeline

1.  How long did you spend on the coding test below?

    I didnt work on the test in one go but in total I spent approximately 80 hours

2.  What would you add to your solution if you had more time?

    - I would enable image uploads so users can document their favorite things with pictures
    - Add social sharing
    - Improve performance by integrating Redis
    - Also add social authentication to enable users login quickly


## Most Useful feature in Python3.7/Flask latest version

1.  Python

    - The most useful feature of python 3.7 is  the built in breakpoint
        <img width="990" alt="Screen Shot 2019-07-26 at 12 42 42 AM" src="https://user-images.githubusercontent.com/19865565/61915978-a5712680-af3e-11e9-9bd8-e5524ba0048b.png">

     Also the speed of python has improved alot in version 3.7

## Tracking Performance issue on Production

-   Experience with Seegad
    I worked with team on aproject that required us to build an asset mannagement system and also migrate the present system(google sheets) being used to the new platform. The dockerized project had many dependencies and at a point we had issues with our celery and redis, migrating data was taking too long and automated emails stopped functioning.

    The approach I took in the above case is similar to the way track down issues on production, first of all I try to make sure it is not an  enviroment issue.I will normally replicate the bug on dev enviromet, run the application with Docker and also on local my local machine to confirm its not an issue with the differnt setup and after I will isolate the different aspect of the codebase  associated with the bug. In this case i will isolate redis and run the code without redis.Also making use of APM tools has really helped me in debugging production isssues.The above case it turned out it was an issue with our GCP setup.

