#File Transfer Portal for the company "Altshare"


##API
REST API Endpoints for tranfering files 
GET /files # List all uploaded files 
POST /upload # Uploads a new file from current folder
GET /files/name #Opens the uploaded file in browser

*Make sure the files are in local folder, for practice there are 2 examples files named:
example-1.pdf
test.txt command- curl -X POST http://localhost:(chosen port number)/upload -F "file=@./test.txt"
