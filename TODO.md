### 
1. 
delegate the job of writing database records to the kafka consumers.
Let the backend api servers pass the data as is to kafka.

WONTFIX in POC - needs db access code be split across multiple components, plus issues related to 
async response, poll back and wait till resource is ready.

2. 
Add redis cache and populate it with frequently accessed data
List of currently logged in users, JWT tokens, expiry, recent posts.

WONTFIX in POC - Time constraints.

3. 
Get the websocket chat working in a end to end manner.
DONE

4.
Admin token should be displayed on the admin profile page.

For PoC, picking it from backend logs.

5.
Implement authentication for kibana dashboard.
DONE


6.
Batch processing tasks, identify heavy analytics cases that could be suitable for batch processing.

7.
Clean up UI.

8.
Combine posts/image/video consumers into one process to reduce burden on the system.

9.
Submission of posts/images/videos from the UI.


10.
multi user chat on the UI.

11.
Logout for admin should do a server logout.
