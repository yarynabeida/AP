TO INSTALL:

Open command prompt and input these commands:

> cd folder/to/clone-into/
> git clone https://github.com/yarynabeida/AP_variant_2.git
> pyenv install 3.8.6
> cd AP_variant_2
> pip install virtualenv
> virtualenv space
> .\space\Scripts\activate
> pip install -r requirements.txt

Then open and run myapp.py, input in command prompt:

> curl -v -XGET http://localhost:5000/api/v1/hello-world-2
