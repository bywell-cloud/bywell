Distinctiveness and Complexity

In this project task manager , people can register to login either as manager or as worker so it has different user levels.
There is a time tracker in managers login to see the number of days to expiry date to see if work is progressing as scheduled.
I have placed modal for popup view to view the problems or progress.i have used javascript for searching tasks according to project name for the worker , also for 
view tasks asigned by the manager . I also included progress bar to view progress status.

What is in the system and how it works.

Including what is above the following :
1) for manager
   a)manager can add and delete project
   b)He can assign task to a worker for a project
   c)He can view  a task and can see the progress done 
   d)He can only edit  a task which he has assigned
   e)He can delete a task which he has assigned.
   f)Can view all tasks in project and can click to view only ones he has assigned
   g)Only manager and Admin can change status from 100% to a lower status.
   f)popup view to view the problems or progress(using modal source below is the link source)

2) Worker
   a) Can only view all tasks assigned to him
   b) Can search for tasks for specific project
   c) Can update progress status
   d) Can add problem and progress report for each task
   e) can not edit task name, description and (start and end) dates

3) The index.html would check if the role is for worker or for manager  If  user rolelevel is 1 then it is for manager else for worker and if for worker it displays the information for 
   a worker to view, if it is for manger then it will display the information for a manager to view - the index.html get information from index in views.py
   
   
   For manager :
   The addproject.html - create new project by manager using addproject in views.py
   The assign.html - to assign a task by manager using assign in views.py
   The view.html and js22.js - view tasks by manager using view in views.py  and to view tasks assigned by me(logged in manager) 
   delete in views.py to delete task
   deletepr in views.py to delete project
   The edit.html - edit tasks by manager using edit in views.py

  ( source for modal popups:
   <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.0.0/jquery.min.js"></script>

   <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-modal/0.9.1/jquery.modal.min.js"></script>
   <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/jquery-modal/0.9.1/jquery.modal.min.css" />)
   
   
   For worker
   The action.html - to update progress(update progress bar and update problem /progress) for task by worker using action in views.py
   The js2222121.js to view tasks for specific project
   popup view to view the problems or progress(using modal source above is the link source)

4) When you register user you choose either register as worker or as manager.

  When you login the system checks the rolelevel if it is for manager or for worker .
   
   
   



