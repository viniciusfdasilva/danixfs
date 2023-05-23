<html>
<center><img src="https://silvavinicius.com.br/danixfs/logo.png" width="600" height="600"></center>
</html>

* Author: Vinicius F. da Silva
* Version 0.1.4
* Released: 2023

A very simple subsystem builder!

The Danixfs is a root filesystem management! Build a Alpine subsystem and pre install
essentials packages and compilers from languages choice by user: 
# Image:

#### Building a clike environment

![](./img/img_i.png)
![](./img/img_ii.png)
![](./img/img_iii.png)
### System Environments

![](./img/img_iv.png)
### Environments Snapthots

![](./img/img_v.png)


# Required packages

    * curl 7.81.0 or higher 
    * tar 1.34 or higher 
    * python3 or higher
    * pip3 or higher
# Install Danix

```shell 
$ sudo make install
```

To clean configuration run:

```shell
$ sudo make clean
```

```shell 
$ danix -h
```

![](./img/img_vi.png)

# Remove Danix

To remove danix run:
```shell
$ sudo danixclean
```
# Common erros

![](./img/img_vii.png)

To fix this erro open file *registry.py* located in /usr/local/lib/python3.10/dist-packages/django/apps/

Search for 

```python
raise RuntimeError("populate() isn't reentrant")" 
```

line. And replace for following code:

```python
self.app_configs = {}
```

Save file and try again
