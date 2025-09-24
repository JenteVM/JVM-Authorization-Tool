# JVM Authorization Tool

This project is to serve as a basic authorization tool
## Quick rundown

This project is made by JenteVM, it serves as a simple multi application authorization tool in which every application can have a different (or shared) database and store or authorize their users, it has built in database authorization (Not just CORS but also a db specific one to stop people from accesing other peoples databases) so people can be stopped from using the authorization API. I built this slow and steady in my own time so it may be hard to understand (I write spaghetti code) or have some (hopefully) minor flaws relating to security or QoL. If you find any problems, please do report them as I do want to have a good working software to present here.

## Why you should or shouldn't use it

You should use this application if you are looking for something small scale. This is because this application only has basic security features. I strongly suggest not to use this for any large scale production. There are many flaws I am working out of here but I am not in any way obliged to do so and thus will not be a reliable point when looking for something large scale. I do suggest it to people who just care about a small security layer though, as there (to my knowledge) aren't any things that do not work for the user. (except for some delayed stuff visible in the to_do_list.txt)