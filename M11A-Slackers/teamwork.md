# Teamwork Reflection

## Iteration 2:
### Meetings
Though our meetings were scarce during Iteration 2, they were by no means unproductive.
Our most important meeting had to be done via a group call in Week 5 due to conflicting schedules
not allowing for an on campus meeting, and was used as a means to orient all of the team members
in the right direction for Iteration 2.

During this meeting we discussed how work was going to be divided amongst the group members, and
an initial deadline for individual work to be completed before merging our branches together to work
on the front end.

A skeleton of the plan is as follows.

    - Alasdair would handle the authentication and standup functions.
    - Avi would handle the message functions.
    - Sam would handle the channel functions.
    - Wincent would handle the user, admin, and search functions.
    - An intial deadline was set for the 14th of October.

Note that, unlike in Iteration 1, the group chose to divide functions based on
their typing within the Slackr project. As a result however, some had less functions
to implement than others, so to overcome this, we decided that those with more functions
could pass several of theirs off to the less burdened group members later on in the week,
once all group members had gotten a feel for how each others' functions worked.

Apart from our major meeting in Week 5, there was only one other formal meetings due to
members being very busy Week 6 as a result of deadlines from other courses. To ensure
that Iteration 2 still went smoothly despite these deadlines, the group kept in close
communication via our group chat, where we discussed our progress and any questions we may
have had for each other on a daily basis.

The other formal meeting took part the day before the official deadline of Iteration 2,
and consisted of team members all coming together to merge and work out kinks in our
code before the due date. The group members chose to once again utilise a group call
for the meeting.

The meeting consisted of the following items.

    - Merging our individual branches to the master branch.
    - Testing the program as a whole with the front end.
    - Updating and/or re-writing tests from Iteration 1.

The meeting all in all spanned five hours, with the group coding away to ensure
that they met the deadline.

### Methods for successful meetings
In order to ensure that the meetings were successful, we chose to make sure that all the
points discussed were readily available for members to look back on throughout Iteration 2.
For our formal meeting of Week 5, a team member chose to keep a minute that kept track of
which team member was assigned which set of functions, as well as any other concerns or issues
raised during the meeting (conflicting schedules, looming deadlines, etc.).
Note that this was not a major concern for our informal meetings, as the messages in the group chat
were recorded by the software itself, and thus did not require any external effort.
For the formal meeting in Week 6, there was no formal minute, as we felt
as that extraneous effort would result in less time put towards the actual deliverables,
and as such they were ignored.

### How we overcame any hurdles
The major hurdles were meeting our initial deadline, and getting our code to work with each other's code
as well as the frontend. Though some members missed the initial deadline of the 21st, as a result of
impending deadlines from other courses, they were able to complete all their code by the 22nd, and as a result,
the hurdle was not too large.
However, perhaps as a result, when initially merging the code to master, many bugs, naming conflicts, and merge
conflicts were encountered. To combat this, we chose to approach each one individually, and as a group. Our collective
strengths and knowledge of our own code, allowed for this process to go relatively smoothly, with little trouble.
A relatviely major issue did arise with a branch being too far behind master where resolving the merge conflicts would be too much work,
so to combat this, members manually copied the files into master, and closed the merge request.
Another hurdle was connecting our code to the frontend for Iteration 2. Though this was not a formal requirement, we felt
as that should have been our end goal. While we tried to mesh the backend and the frontend together as a team, in the end we
were largely unsuccessful, and chose to instead test our code solely through pytests and coverage.

### How multiple people worked on the same code
With multiple people working on the same code, there were bound to be some conflicts
and thus a meeting was allocated to spend time together unifying code accross the board
and dealing with any merge conflicts, naming conflicts, and any other errors that resulted on the
same code.

When individual members needed help with their branch, the helper would checkout onto the relevent
branch to assist the other member, and thus all the code was shared amongst the two.
Furthermore, when creating our merge requests into master, we made sure to do them one at a time,
so we could iron out any kinks as they popped up, rather than having been left with a mess of bugs and
conflicts from merging all at once. Though this a fair amount of time to do, it saved us much more time
in the long run.

## Iteration 3:
### Meetings
During Iteration 3, the team held formal meetings sparsely due to the relatively simple tasks that needed 
to be done before the major task of connecting the backend to the frontend. We held only one verbal meeting, early on 
during the iteration, where each group member's tasks were delegated, and a preliminary deadline was set for 
the 14th of November to have code refactored. However, unfortunately this deadline was not met by all members, 
and so it was extended to the 15th. The tasks that were delegated during this meeting included the implementation 
of changes to the specification, as well as general refactoring of the code we had written in Iteration 2. 
Furthermore, during this meeting we populated the issues board with these task so they could be easily tracked.

During the coding process, we also had two "informal" text meetings in the group chat (on top of regular messages),
where we discussed issues in our code between all members over an extended period, and attempted to work out errors. 
The final one of these was on Sunday afternoon, to attempt to get any final errors in pytests and make sure all of our
code worked ahead of the demonstration.

By planning out these meetings in advance through the group chat, and summarising them in text during the meetings, we ensured
that every meeting was productive, and that what we had discussed in the meetings was implemented in our work.

### How we overcame any hurdles
A few hurdles did occur during this iteration. Due to conflicting schedules, our
first voice meeting was pushed back to the night of the 11th of November, and even then
one of the members could not join in. Otherwise, this meeting did not have any hurdles.
Another hurdle included this missing of the initial deadline for the tasks discussed in
this meeting, as it was not all completed by the 14th of November. In order to overcome this,
we simply had to extend the deadline a bit further.

### How multiple people worked on the same code
We handled this issue in much the same way as we did in iteration 2. Tis iteration a meeting for the
purpose of unifying code was not necessary, as the style of the code was already dictated in
iteration 2. 

Again, we attempted to keep our coding as seperate as possible, working on the same files as we did
in iteration 2. If anyone needed help, help would be given on the relevent branch to avoid merge conflicts.
