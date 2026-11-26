
# Welcome to your CDK Python project

This is a blank project for CDK development with Python.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv (venv) within this project, stored under the `.venv`
directory.  To create the venv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the venv fails,
you can create the venv manually.

## Python Environment Setup

1) To manually create a venv on MacOS and Linux

```bash
python3 -m venv .venv
```

2) Activate the venv

```bash
source .venv/bin/activate

# On Windows use:
#   .venv\Scripts\activate.bat
```

3) Install project dependencies

```bash
pip install -r requirements.txt
```

## Using CDK

At this point you can now synthesize the CloudFormation template for this code.

```bash
cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `requirements.txt` file and rerun the `python -m pip install -r requirements.txt`
command.

## Useful commands

* `cdk ls`          list all stacks in the app
* `cdk synth`       emits the synthesized CloudFormation template
* `cdk deploy`      deploy this stack to your default AWS account/region
* `cdk diff`        compare deployed stack with current state
* `cdk docs`        open CDK documentation

Enjoy!
