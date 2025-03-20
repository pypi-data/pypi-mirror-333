### Go inside of the parent folder 
( Here it is C:\My_Python_Libraries)

### Install using pip

``` pip install . ```

### Check installation

```
    from mallickboy.runtime  import runtime
    from mallickboy.rle  import compress

    # use runtime before defination
    @runtime
    def main():
```

### Setup 

`py -3.11 -m venv .venv`

`pip install -r .\requirements.txt`

`.\.venv\Scripts\activate`

Create setup wheel for `pip` installation

`python .\setup.py sdist bdist_wheel`

Install Current version

`pip install .\mallickboy-0.0.7-py3-none-any.whl`

`pip install .` (without craeting setup tools, setup.py is required)
