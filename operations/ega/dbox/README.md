### List files accessible on EGA Aspera server

EGA Aspera servers has one file that we know of that is listing all the files accessible for download on their server. This
file is called dbox_content. The purpose of this operation is to display the dbox_content file.

In order to run this command, asperca command-line client is required: ascp:
https://downloads.asperasoft.com/en/downloads/50

To have more help running this operation:
```bash
./main.py ega dbox -h
```

The operation command
```bash
./main.py ega dbox {ASPERA_SERVER} {ASPERA_USER}
```

{ASPERA_SERVER}: The url of EGA Aspera server
{ASPERA_USER}: The user name to access the server
