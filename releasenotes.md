## 1.5.0.0-beta
*released: Oct 08, 2025 07:05 PM UTC*
- do not discard overdue tasks *(fix)*
- fix empty/broken test *(test)*
- do not allow zero durations in recipe definitions *(feat)*
- have latest tag target *(chore)*

## 1.4.0.1-beta
*released: Sep 28, 2025 03:09 PM UTC*
- fix image versioning *(chore)*

## 1.4.0.0-beta
*released: Sep 28, 2025 02:58 PM UTC*
- have fix/build versioning *(feat)*

## 1.3.2.2-beta
*released: Sep 28, 2025 03:51 AM UTC*
- have version number an start page *(feat)*

## 1.2.2.2-beta
*released: Sep 28, 2025 02:07 AM UTC*
- remove unused imports *(refactor)*
- increment next left on up timer adjustment *(fix)*
- have imminent logic on back *(fix)*
- have test humper work with multiple dependents *(chore)*
- fix image versioning *(chore)*

## 1.2.1.2-beta
*released: Aug 31, 2025 11:31 PM UTC*
- stop button flickers *(fix)*

## 1.2.0.2-beta
*released: Aug 31, 2025 09:04 PM UTC*
- have beta releases *(chore)*
- have versioned builds *(chore)*
- have version string logic *(chore)*
- have quicker new version deployment *(chore)*

## 1.2.0.1-alpha
*released: Aug 24, 2025 06:34 PM UTC*
- have multi dependent support *(feat)*
- better describe recipe contribution *(docs)*

## 1.1.0.1-alpha
*released: Aug 02, 2025 06:24 PM UTC*
- give contribution advice *(docs)*
- fix bad English in the up make target *(docs)*
- fix single shot launch command *(chore)*
- fix production build *(chore)*
- saturated time window situation *(fix)*
- have no overwrite feature for recipe inserts *(chore)*
- have "unlimited" local caching *(feat)*
- have up target *(chore)*
- get docker build running post merge *(chore)*
- fix dual node_module target from previous merge conflict *(chore)*
- do not assume virtual env is installed on build machine *(chore)*
- fix bad assertion name *(test)*
- let dockerfile manage dockered data location *(chore)*
- have crude production build *(chore)*
- staging rerender flickering *(fix)*
- advertise timers are adjustable *(feat)*
- left spacing with imminent timers *(fix)*
- show active parttos in the overview *(feat)*
- cache overuse with unrealistic amount of part tos *(fix)*
- have more sequential patterned timeline *(refactor)*
- piggy back on already defined active_tasks *(refactor)*
- remove dead code *(refactor)*
- get more descriptive fail messages *(test)*
- cache only volatile endpoint call for time of a page load *(feat)*
- add testing mock *(test)*
- add example recipes *(docs)*
- have definition list for whole test instead of each partto *(test)*
- have replicatable set iteration order *(test)*
- force string ids in timeline calculation because differing types created extra testing *(fix)*
- rename makefile target *(chore)*
- remove unnecessary log statement *(fix)*
- have selection page paused by default *(feat)*
- can have default pause state on panes *(feat)*
- remove unused import *(refactor)*
- have durations in displayed timelines *(feat)*
- have middleware not api validate front end calls *(fix)*
- have less naive timeline calculation *(feat)*
- have test input dumper from recipe file *(refactor)*
- remove unused function *(refactor)*
- have task duration calculation by run state *(feat)*
- have a duty not be a task *(fix)*
- link work to task instead of duty *(fix)*
- have depend* naming match *(refactor)*
- have timeline definition accessible *(refactor)*
- have timeline repr dump tool *(test)*
- have timeline algorithm *(feat)*
- have common repr function format *(style)*
- update description *(docs)*
- better describe what the project does *(docs)*
- remove unused file *(refactor)*
- do not have spinner flicker in at beginning *(feat)*
- keep selected item through deletion *(fix)*
- correct spacing of icon before texts *(fix)*
- have iconed task page descriptions *(feat)*
- have pretty task/duty/imminent body *(feat)*
- have shared body component *(refactor)*
- have duty instead of a task *(fix)*
- have overview page *(feat)*
- have formatted times *(feat)*
- have task/duty knowlegde for non started tasks *(feat)*
- have picnic table icon *(feat)*
- have accordion effects on already open render also *(feat)*
- have iconed title component *(feat)*
- have complete dinner message *(feat)*
- have something other than empty string to display a 0 duration *(feat)*
- catch cyclic dependencies in part to creation *(fix)*
- have understyled overview when cooking *(feat)*
- have understyled overview when staging a meal *(feat)*
- have overview component *(feat)*
- have overview icon *(feat)*
- have accordion for items/tools for groups of tasks *(feat)*
- have parttos layout for others to use *(feat)*
- have mandatory upcoming tasks in run state *(feat)*
- move api validation to middleware *(refactor)*
- have structured endpoint variants *(refactor)*
- remove duplicate function under another name *(refactor)*
- show argument types are anchored to import pass *(refactor)*
- remove unused method *(refactor)*
- remove structuring to allow serializing non 200 repsonses *(refactor)*
- do some refactoring in the serializers *(refactor)*
- have a fish n chips dinner *(feat)*
- have better spacing on parttos *(feat)*
- have upcoming task data in run state *(feat)*
- have better styled definition lists *(feat)*
- have beta styled recipe selection *(feat)*
- have carousel scrolling *(fix)*
- have list accordions start open *(feat)*
- do not have empty message flicker before list arrives *(fix)*
- have support for listing part to descriptions *(feat)*
- have accordions default open *(feat)*
- have pretty selectable part to lists *(feat)*
- have prettier shared list item *(feat)*
- have sharable animations *(refactor)*
- have more recipes *(feat)*
- do not do averaging ourselves in aggregation *(fix)*
- have pizza recipe *(feat)*
- have intelligent part to disclosure *(feat)*
- have sharable list item *(refactor)*
- use formatted definitions for item set lists *(feat)*
- have formatted list items for definitions (unused) *(feat)*
- have dynamic sized list items *(feat)*
- fix quote types *(style)*
- have better spacing on empty accordion *(fix)*
- have some application entity icons *(feat)*
- have application wide styled scrollbars *(feat)*
- have styled ingredients and tools *(feat)*
- remove rogue comment *(style)*
- have run state duration be calculated from past *(feat)*
- have timers based off previous runs *(feat)*
- ensure imminent timers are disclosed at cook start *(test)*
- hold theme through reload *(feat)*
- have german breakfast *(feat)*
- make front end block timers if not cooking *(fix)*
- have zero magnitude timers move *(fix)*
- have correct empty pane spacing *(fix)*
- have done cooking message *(feat)*
- have layouts for task details *(feat)*
- put menu on a feature flag *(feat)*
- do not have unused console log statement *(style)*
- better describe an empty initial pane *(feat)*
- reintroduce logo click *(feat)*
- use shared taskdefinition component *(refactor)*
- position task page so stage can also use it *(refactor)*
- do not lose offsets on rerender *(fix)*
- have navigation to imminent duties *(feat)*
- have calmer flashing for alarm toasts *(feat)*
- have sharable flashing elements *(refactor)*
- go to alarming duty when clicking corresponding toast *(feat)*
- have message admit UI recipe entry is not supported *(feat)*
- obey black spacing rules *(style)*
- go to first item in list when last is deleted *(fix)*
- have better named marshaling *(refactor)*
- make demo location clickable *(docs)*
- remove commented out dead code from early on *(style)*
- have only one DB instert for batch run state changes *(refactor)*
- have 2 DB hit batch state changes *(refactor)*
- have media assets in demo environment *(fix)*
- have black enforced space *(style)*
- ensure demo environment build *(chore)*
- fix demo environment sound *(fix)*
- have demo *(chore)*
- obey black with a double space *(style)*
- deflake timer test *(test)*
- remove unnecessary verboseness *(style)*
- remove unfulfilled custom django commands *(chore)*
- remove older naive run state management system *(refactor)*
- do not have old tests for single file *(test)*
- do not have timers before cooking starts *(fix)*
- remove dead code *(refactor)*
- use timer provider *(feat)*
- use custom message dispatcher that allows function passing *(fix)*
- have run state broadcasted *(refactor)*
- put partto insert freeze guard in *(fix)*
- have chicken salad *(feat)*
- have backend supported timer availability *(feat)*
- have global run state availability *(refactor)*
- add some duration mathematics *(refactor)*
- set up heavier featured routing for storybook *(test)*
- clean node_modules directory too *(chore)*
- give backend knowledge of timers *(feat)*
- remove erronously checked in file *(chore)*
- fix ci not happening *(chore)*
- limit imminent duties to 1 *(feat)*
- have ingredients in tasks *(feat)*
- standardize ARGUMENTS *(chore)*
- have first meal used in Part To (went well) *(feat)*
- have alarm notifications *(feat)*
- have css working with front end code templater *(chore)*
- revamp timers *(feat)*
- fix landscape view not always filling width with definitions *(fix)*
- remove some unused comments in css *(style)*
- have version endpoint *(feat)*
- have finish time in run states *(feat)*
- fix time calculations *(fix)*
- have storybook target *(chore)*
- have full imminent workflow *(feat)*
- do not directly access "Cooker" tabler icon *(refactor)*
- remove unused stories *(chore)*
- have non-carousel list view *(feat)*
- verify front end builds with every commit *(chore)*
- have implemented imminent run state field *(feat)*
- make navigation logo clickable to home *(feat)*
- fix cache control being bypassed *(fix)*
- have tasks added field part to *(feat)*
- save fix for timer rerender until an overall styling overhaul *(fix)*
- remove unused file *(refactor)*
- have imminent in run state *(feat)*
- have required ingredients and tools *(feat)*
- do not have disabled debouncing on buttons *(fix)*
- fix duty as task in Bavarian Roast *(fix)*
- have shared test argument option environment variable *(chore)*
- have working run starts *(fix)*
- expose time used in definition order calculation *(refactor)*
- have correct partto post duration parsing *(fix)*
- fix situation where double task occurs with final duty *(fix)*
- generalize recipe insert user feedback *(chore)*
- insert any number of recipes in one console command *(chore)*
- have working bavarian pot roast recipe *(fix)*
- have required ingredients and tools fields in task definitions *(feat)*
- have inventory helpers (ingredients & tools) *(feat)*
- fix updateapi test generation *(chore)*
- fix release version mismatch *(chore)*
- have API updater in Makefile *(chore)*
- enforce unit tests passing on commit *(chore)*

## 1.0.0.1-alpha
*released: Dec 04, 2024 03:47 PM UTC*
- remove automatic git push from release creation *(chore)*
- have versioning *(chore)*

