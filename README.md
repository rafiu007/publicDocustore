# docuStore
document storage django service
the api server has 3 main apis which encompass all business logic.They are explained below.
Code with unittest is in the test branch  as main branch contains credentials to hosted db.


# uploadfile

`Request`
```
curl --location --request POST 'https://docu-store-rafiu.herokuapp.com/file/uploadfile' \
--form 'folder="e"' \
--form 'topic="war,love"' \
--form 'file=@"/Users/rafiu/code.cpp"'
```
`Sample Response`
```
{
    "Msg": "The file has been inserted"
}
```

# searchfile

`Request`
```
curl --location --request POST 'https://docu-store-rafiu.herokuapp.com/file/searchfile' \
--header 'Content-Type: application/json' \
--data-raw '{
    "folder_name":"e",
    "file_name":[],
    "topic":[]
}'
```
`Sample Response`
```
[
    [
        {
            "id": 3,
            "file_name": "code",
            "file": "/media/upload/2022/02/27/code.cpp",
            "file_type": "text/x-c",
            "file_size": 779.0,
            "created_at": "2022-02-27T06:56:05.120044Z",
            "updated_at": "2022-02-27T06:56:05.120071Z",
            "file_topic": [
                1,
                2
            ]
        }
    ]
]
```

# delete

`Request`
```
curl --location --request DELETE 'https://docu-store-rafiu.herokuapp.com/file/delete' \
--header 'Content-Type: application/json' \
--data-raw '{
    "folder_name":"e",
    "file_name":["sss"]
}'
```
`Sample Response`

```
{
    "msg": "folder removed successfully"
}
```
