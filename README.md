# architecture-requirements
Time-induced python program to retrieve and input data in a database for requirements in architecture. Input is done after assessing the biometrics.


The Architecture Requirements Specification provides a quantitative view of the solution, stating measurable criteria that must be met during the implementation of the architecture.

Often workers find it difficult to express their requirements and get information about time taken in the process to the architect.

2-3 kiosks can be established at relevant places in the architectural premises which can enable workers to input their requirements and retrieve information about its status. Similarly, the architect can input information about its status. For his authenticity, a fingerprint scanner can be incorporated in the kiosk.

This project intents to address the technological statement of architecture work.

# 1.

We will assume fingerprint scanner inputs a test fingerprint file in the python program. Function fingerprint() will match the test files to fingerprints stored in a directory. The directory only contains fingerprints of architects. After matching, the function will retrieve data from the database containing fields SNo, Name, fingerprint filename and provide access to further information in the kiosk if user is authorised. 

# 2.
PYTHON PROGRAM:


OBJECTIVE:

The program intents to perform following functions:
1.	Allows worker to input his requirements.
2.	Allows architect to retrieve the requirements.
3.	Allows architect to update status of requirements.
4.	Allows worker to retrieve status of requirements.
5.	Allows architect to retrieve complete log of requirements.
6.	Allows worker to check his Wid. 
7.	Allows architect to add and remove workers in the database.
8.	Allows architect to retrieve workers in the database.

NOTE: 
1.	Worker input is automatically cleared from the database once updated by architect. It can then be retrieved from worker status.
2.	Assuming requirements are fulfilled by the expected arrival time, worker status is automatically cleared from the database.


NOTE: 
1. To switch between worker and architect, exit prompt.
2. 2. Architect must exit prompt after each use to maintain his authenticity.
3. 3. Names of workers are unique. 


Tables worker_input, worker_status, architect_input, wid have been employed for this purpose.
