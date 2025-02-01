http://Social-backend-env-2.eba-sghwfqpq.us-east-2.elasticbeanstalk.com

/create-user/

{ "username": "chipsloyalty2", "email": "test4@example.com", "password": "notagoodpassword", "first_name": "chips", "last_name": "loyalty" }

/get-user/{id}

(get all users) /get-users/

/create-post/

{ "user": 5, "title": "Not a Great Title", "content": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum." }

/get-post/{id}

/create-comment/

{ "post": 1, "user": 5, "content": "nice ipsum" }

get-posts-by-user/{user-id}