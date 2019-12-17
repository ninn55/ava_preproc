# Jupyter Notebook 后台运行

* `nohup jupyter notebook --allow-root > error.log &`
* `ps -ef | grep jupyter`
* `kill -9 <pid>`
* 密码等设置可见`<working_dir>/error.log`