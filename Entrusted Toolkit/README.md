# Entrusted Toolkit

These script enable admins to scan and modify institutional data in 'entrusted' folders. 

## ensureFolderName

Given a Box folder ID and some prefix, this script will ensure that the folder and every subfolder begins with the specified prefix.

### Usage

`ensureFolderName -f FOLDER_ID -u USER_ID -p 'PREFIX' -a 'PATH_TO_AUTH_CONFIG_JSON'`

### Example

`ensureFolderName -f 1234509876 -u 112233 -p '[Sensitive]' -a '~/Documents/Box_Jwt_Config.json'`

Before:

```
/My Files
  /Folder A
  /Folder B
```   

After: 

```
/[Sensitive] My Files
  /[Sensitive] Folder A
  /[Sensitive] Folder B
```
