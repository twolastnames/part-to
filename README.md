# Part To

### An interactive cookbook.

A user picks what recipes they want to cook in a meal. It then displays the individual recipes into a recipe for a meal. The program then estimates a completion time of the interwoven recipes and commands the cook operation by operation to complete the meal. Execution times of tasks are used to better forcast future meal execution times. It can make two recipes that take 15 minutes with 10 minutes of work each become a meal with 20 minutes of work completed in 20 minutes.

## Makefile Targets

| Command   | Description |
|-----------|-------------|
| full      | creates a full environment on [http://localhost:8000](http://localhost:8000) from scratch. `git clone https://github.com/twolastnames/part-to.git && cd part-to && make full is expected to work with most UNIX distributions from an empty directory. Subsequent launches should be `make runback` as the backend will serve the front end if asked to. |
| updateapi | From reading the openapi file, generates the front end API and backend templates for handling requests in an unmarshalled manner. |
| release   | From githook enforced commit message sematics, cut a release branch of proper version and prepend the release notes. | 
| runback   | Run a development backend. The front end can be accessed on port 8000, but the front end doesn't hot rebuild. |
| runfront  | Run a development frontend with hot rebuild. It's accessable on port 3000. |
| clean     | Delete anything this file generates. |
| test      | Run unit tests. |
| runproduct | WIP: production server command |
