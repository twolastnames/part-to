# Part To

### An interactive cookbook.

A user picks what recipes they want to cook in a meal. It then displays the individual recipes into a recipe for a meal. The program then estimates a completion time of the interwoven recipes and commands the cook operation by operation to complete the meal. Execution times of tasks are used to better forcast future meal execution times. It can make two recipes that take 15 minutes with 10 minutes of work each become a meal with 20 minutes of work completed in 20 minutes.

## Makefile Targets

| Command   | Description |
|-----------|-------------|
| up        | With docker, it runs the application an port 22222 while requiring the use of port 20222. The quickest way to see the application with docker is the command: `sudo echo sudoized && git clone https://github.com/twolastnames/part-to.git && cd part-to && make up`. Note: nginx will 502 backend calls for a few minutes while waiting for the part-to backend to seed and launch.
| updateapi | From reading the openapi file, generates the front end API and backend templates for handling requests in an unmarshalled manner. |
| release   | From githook enforced commit message sematics, cut a release branch of proper version and prepend the release notes. | 
| runback   | Run a development backend. The front end can be accessed on port 8000, but the front end doesn't hot rebuild. |
| runfront  | Run a development frontend with hot rebuild. It's accessable on port 3000. |
| clean     | Delete anything this file generates. |
| test      | Run unit tests. |



## Contributions

Obviously, writing some code for features/fixes would be appreciated and discussions could start by adding an issue to this project. I'd also like to hear in the issues about problems with running make commands.

A please contribution, would be to add your favorite recipes. Examples can be seen in the `examplerecipes` directory. The easiest way to add/test a recipe to a running instance is to create a virtual environment and execute `FILE=myrecipe.toml ORIGIN=http://myhost:20222 make forcerecipe`. With this target, a recipe of the same name/title will be overwritten. Once the recipe works correctly, adding it to the `examplerecipes` directory and making a PR sets it up to be in future releases.

Note: an "engagement" in a recipe is a percent of time spent managing that duty. 100% is the default and is called a task.
