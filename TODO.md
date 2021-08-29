### 
1. WONTFIX in POC - too many issues to handle here.
delegate the job of writing database records to the kafka consumers.
Let the backend api servers pass the data as is to kafka.

2. WONTFIX in POC - complicated access model, time constraints
Add redis cache and populate it with frequently accessed data
List of currently logged in users, JWT tokens, expiry, recent posts.

3. 
Get the websocket chat working in a end to end manner.

4.
Admin token should be displayed on the admin profile page.

5.
Implement authentication for kibana dashboard.

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
