# Entrusted Toolkit

These script enable admins to scan and modify institutional data in 'entrusted' folders. 

| Script        | Description |
| ------------- |-------------|
| [printUserFolders](#printUserFolders) | List all subfolders of a given folder |
| [ensureFolderName](#ensureFolderName) | Ensure that all subfolder names start with a specified prefix |
| [auditFolderName](#auditFolderName) | Print the path of any subfolder whose name does not start with a specified prefix |
| [printFolderCollaborators](#printFolderCollaborators) | Print the collaborations on a given folder and all subfolders  |
| [printPrimaryLogin](#printPrimaryLogin) | Print the primary login (email address) for a given list of usernames  |


## printUserFolders

Given a Box folder ID, log the ID and path of that folder and every subfolder.

### Usage

`printUserFolders -f FOLDER_ID -u USER_ID -a 'PATH_TO_AUTH_CONFIG_JSON'`

### Example

`printUserFolders -f 1234509876 -u 112233 -a '~/Documents/Box_Jwt_Config.json'`

Output:

```
12345 /My Files
12346 /My Files/Folder A
12347 /My Files/Folder B
```   

## ensureFolderName

Given a Box folder ID and some prefix, rename folders such that the folder and every subfolder begins with the specified prefix.

### Usage

`ensureFolderName -f FOLDER_ID -u USER_ID -p 'PREFIX' -a 'PATH_TO_AUTH_CONFIG_JSON'`

### Example

`ensureFolderName -f 1234509876 -u 112233 -p '[Sensitive]' -a '~/Documents/Box_Jwt_Config.json'`

Box Folder Tree Before:

```
/My Files
  /Folder A
  /Folder B
```   

Box Folder Tree After: 

```
/[Sensitive] My Files
  /[Sensitive] Folder A
  /[Sensitive] Folder B
```

## auditFolderName

Given a Box folder ID and some list of prefix, print the ID and path of any subfolder whose name does not start with one of the prefixes.

### Usage

`printUserFolders -f FOLDER_ID -u USER_ID -p PREFIX_1 PREFIX_2 -a 'PATH_TO_AUTH_CONFIG_JSON'`

### Example

`printUserFolders -f 1234509876 -u 112233 -p [Sensitive] {Sensitive} -a '~/Documents/Box_Jwt_Config.json'`

Output:

```
Violation 12345 /My Files
Violation 12346 /My Files/Folder A
Violation 12347 /My Files/Folder B
```   

## printCollaborations

Given a Box folder ID, print information about accepted collaborations originating in that folder and all subfolders.

### Usage

`printCollaborations -f FOLDER_ID -u USER_ID -a 'PATH_TO_AUTH_CONFIG_JSON'`

### Example

`printUserFolders -f 1234509876 -u 112233 -a '~/Documents/Box_Jwt_Config.json'`

Output:

```
FolderId, FolderPath, CollaborationId, CollaborationRole, CollaborationCreated, CollaboratorId, CollaboratorName, CollaboratorLogin, CreatorId, CreatorName, CreatorLogin
12345, "/All Files/My Files", 98765, editor, 2017-12-18T12:52:03-08:00, 112233, "User Foo", foo@iu.edu, 223344, "Collab Creator", creator@iu.edu
12346, "/All Files/My Files", 98765, editor, 2017-12-18T12:52:03-08:00, 112244, "User Bar", bar@iu.edu, 223344, "Collab Creator", creator@iu.edu
12347, "/All Files/My Files/data", 98766, editor, 2017-12-31T00:00:00-08:00, 12255, "User Baz", baz@iu.edu, 223344, "Collab Creator", creator@iu.edu
```   

## printPrimaryLogin

Given a list of Box usernames, print the primary login (email address).

### Usage

`printPrimaryLogin -f 'PATH_TO_USER_FILE' -a 'PATH_TO_AUTH_CONFIG_JSON'`

### Example

`printUserFolders -f ~/Documents/usernames.txt -a ~/Documents/Box_Jwt_Config.json`

Output:

```
Username, PrimaryLogin
foo, foo@iu.edu
bar, bar@iu.edu
baz, baz@iu.edu
zzz, (user not found)
```   