# File Transfer Portal 


## API
REST API Endpoints for tranfering files 

GET /files # List all uploaded files 

POST /upload # Uploads a new file from current folder

GET /files/name #Opens the uploaded file in browser

DELETE /files/name #Deletes the uploaded file in browser

*Make sure the files are in local folder, for practice there are 2 examples files named:
example-1.pdf
test.txt 

> 📌 **Curl Example:**
```bash
*Make sure the files are in local folder, for practice there are 2 examples files named:
example-1.pdf
test.txt 
curl -X POST http://localhost:<port>/upload -F "file=@./test.txt"
curl -X DELETE http://localhost:<port>/files/test.txt
```

