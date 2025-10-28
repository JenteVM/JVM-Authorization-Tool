# JVM Authorization Tool

This project is to serve as a basic authorization tool
## Quick rundown

This project is made by JenteVM, it serves as a simple multi application authorization tool in which every application can have a different (or shared) database and store or authorize their users, it has built in database authorization (Not just CORS but also a db specific one to stop people from accesing other peoples databases) so people can be stopped from using the authorization API. I built this slow and steady in my own time so it may be hard to understand (I write spaghetti code) or have some (hopefully) minor flaws relating to security or QoL. If you find any problems, please do report them as I do want to have a good working software to present here.

## Why you should or shouldn't use it

You should use this application if you are looking for something small scale. This is because this application only has basic security features. I strongly suggest not to use this for any large scale production. There are many flaws I am working out of here but I am not in any way obliged to do so and thus will not be a reliable point when looking for something large scale. I do suggest it to people who just care about a small security layer though, as there (to my knowledge) aren't any things that do not work for the user. (except for some delayed stuff visible in the to_do_list.txt)

## How to set it up (frontend)

*Read the wiki for detailed documentation.* <br><br>
Currently the frontend is only set up for my example, please do not use this but use your own.
My frontend is visible at https://jvm-authorization-tool.vercel.app/ and the back end at https://auth.jvm.hackclub.app/ (it does not have an index)

* __base_url/api/registry/__ 
  * allows you to get all registries or post a new one (if authorized in the .env)
* __base_url/api/registry/__*db_id*__/__ 
  * allows you to get a specific registry by id
* __base_url/api/registry/authenticate/__*db_id*__/__*token*__/__ 
  * allows you to authenticate a new origin for a registry via a generated token (use get request)
* __base_url/api/registry/authenticate/__*db_id*__/create/__ 
  * allows you to create a new token for use with the previous point (use get request; need to be authorized to do so; have post level auth for that database)
* __base_url/api/__*db_id*__/users/__ 
  * allows you to get all users (if authorized in the .env or database) or post a new one (if authorized in the database)
* __base_url/api/__*db_id*__/users/__*id_method*__/__*identifier*__/__ 
  * allows you to get a specific user by either id (id_method=id), username (id_method=username) or email (id_method=email)
* __base_url/api/__*db_id*__/users/authenticate/__*int:time_extension*__/__*token*__/__ 
  * allows you to authenticate a user with a token (token gets refreshed upon doing so), this needs to be done with a post request
* __base_url/api/__*db_id*__/users/authenticate/__*int:time_extension*__/0/__ 
  * allows you to authenticate a user with username and password (token is generated upon succesfull log in), this needs to be done with a post request
 
## Notice:
I have made use of AI to go to the module base I have now. It is AI assisted coding. It is all tested and should not cause issues but I did want to bring this to your attention for if you find it important. The frontend used for the Public Test however was fully made by AI as its only purpose was and still is for testing. 

## Public Test
The frontend is available for testing at https://jvm-authorization-tool.vercel.app/, it ofcourse has some flaws, please do not mind those. The backend (for as far as is allowed) is visible at https://auth.jvm.hackclub.app/api/registry/ (it does not have an index). <br> The base user login info can be found on the testing page
I ask of you to not try and use this user for anything else than to create your own database or to test. I do not want any changes made to this user, other users are fine, but changing this user would make the experience non-existent for others wanting to test it out which I would not want to happen.
