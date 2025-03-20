# chromy 

Chromy is a tool that allows you to make chrome extensions with ease. It manages the manifest.json and 
project creation completely for you. You can use it to create a completely new project or use it on an 
existent creation.


## Installing chromy

You can easily install chromy using pip:

```bash
pip install chromy-cli
```
<br>

## Using chromy
### Creating a new project

You can create a new project using the following command:

```bash
chromy init
```

This will create a new project in the current directory, you can `cd` in to any directory and run the command there.

### Using an existing project

You can use chromy on existing projects as well. It will automatically use the current directory you're running the command in. If you want to use 
another directory, run the command `set <directory>`.



### Adding locales to your extensions

You can add locales to your extensions using the following command:

```bash
chromy add locales
```

This will create a locales folder in the current directory and add the locales to the manifest.json file. You can then add your locales to the folder.
You can speed up the process by using:

```bash
chromy add lang <language>
```

Make sure <language> is a valid language code (e.g. en). You can find a list of valid language codes [here](https://developer.chrome.com/docs/extensions/reference/api/i18n#type-LanguageCode).


### Adding permissions
Adding permissions to your manifest.json is fairly straight forward.

```bash
chromy add permission <permission>
```
