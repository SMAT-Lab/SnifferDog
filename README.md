### Dependencies

This project is developed  using Python 3.7  and all the dependencies are  listed in requirements.txt

###  How to use our tool

To generate dependency for given notebooks or Python script, please run the following command.  Please note that currently our API bank includes a limited number of Python libraries, If you hope to add more libraries, please do let us know via Issues report or any means. You can also use the API mapping tool in this project to build API bank for your own, when you try to do this in your publishable work, it would be great to let us known! In addition, this project can also be engineered for entire poject as what we did in the paper.
```
python lib_ver_producer.py filename
```
 
Right now, we have collected a large amount of Python OSS projects and working on expand the volumn of the API blank, we will release it once we've done ! 

### API bank  👋

You can use this [link](https://drive.google.com/file/d/1-UL6xfWG1P0NYpYmv6tlK2GAg933-jgw/view?usp=share_link) to download this dataset.
Unzip API bank data

```console
unzip API-bank-data.zip 
```
How to get the summary of API bank data (e.g the total number of APIs,  the number of added APIs, ...)

```
python API_stat.py
```

### Dataset 

The folder dataset contains three files. 

1. dataset/all.selected.notebooks  6004 notebook project considered in this project. This is a csv file where each of lines has the detailed information such as its GitHub link, Python version, selected notebook and environment file.
2. dataset/snifferdog.executable.notebooks  507 notebook project are executed by  SnifferDog. This is a csv file where each of lines has the detailed information such as its GitHub link, Python version, selected notebook and environment file.
3. dataset/all.github.urls  all 100k notebook projects  


### How to execute a notebook automatically ?

To replicate our results that 507 notebooks are executed by SnifferDog. You need first import the enviornment and then activate the environment.  All the 507 envrionment configrations are in the folder ./ yml/.  The following two script will help you to do this. Please note that the environment name for a project is the same as the project ID in the dataset file (the first column is the project ID)

1. import an environment.  
```
conda env create --name project_ID --file=project_ID.yml
```

2. To execute a notebook
```
conda activate project_ID
python run_jupyter.py   notebookfile
conda deactivate
```

### How to  do API mapping for a Python library ?

1. Download the releases of the library.
```
python download_lib_versions.py  libraryname
```
2. Run the lib_API_mapping.py file
```
python lib_API_mapping.py release_data_dir  libraryname
```
Please note that the program will output a json file for the given library to store its API information
