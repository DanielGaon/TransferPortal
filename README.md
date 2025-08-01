#File Transfer Portal for the company "Altshare"


##API
REST API Endpoints for tranfering files 
GET /files # List all uploaded files 
POST /upload # Uploads a new file from current folder
GET /files/name #Opens the uploaded file in browser

*Make sure the files are in local folder, for practice there are 2 examples files named:
example-1.pdf
test.txt 
command- upload-curl -X POST http://localhost:(chosen port number)/upload -F "file=@./test.txt"
delete- curl -X DELETE http://localhost:(chosen port number)/files/test.txt







#Next steps
Add size restrictions
Add Anti-virus scan
Configure what happens with duplicate names and upload copys
Add login option and audit of who uploads
Add option for folders