# Entrusted Toolkit

These script enable admins to scan and modify institutional data in 'entrusted' folders. 

| Script        | Description |
| ------------- |-------------|
| [printUserFolders](#printUserFolders) | Given a Box folder ID, log the ID and path of that folder and every subfolder. |
| [ensureFolderName](#ensureFolderName) | Given a Box folder ID and some prefix, rename folders such that the folder and every subfolder begins with the specified prefix. |


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
