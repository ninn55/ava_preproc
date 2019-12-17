# Dataturks标注

Dataturks是可以完全自主托管，商用免费的数据集标注解决方案（Apache）。可用于自然语言处理与视觉项目。支持多边形bbox、文档标注、POS\NER标签。输出格式包括Pascal VOC、tensorflow、keras等。

## 部署

准备docker
```
sudo yum update -y
sudo yum install docker -y

sudo service docker start
```

部署docker镜像

```
curl -o dataturks_docker.tar.gz https://s3-us-west-2.amazonaws.com/images.onprem.com.dataturks/dataturks_docker_3_3_0.tar.gz
#pre downloaded instance on root@10.0.14.49/home/wniu/dataTurks/

tar -xvzf dataTurks_docker.tar.gz
sudo docker load --input dataturks_docker.tar
sudo docker run -d -p 80:80 dataturks/dataturks:3.3.0
```
注：端口号为<server_port>:<container_port>


配置docker常用命令

* `docker container ls`
* `docker ps -a`
* `docker stop <container id>`
* CAUTION `docker kill <container id>`
* Remove images, `docker rm <container id>`
* Backup `docker save -o <tar file> <Image>`
* Restore\add `docker load -i <tar file>`
* `docker <command> --help`

## 使用方法

* 注：详细的使用方法`https://dataturks.com/help/help.php`

* `url: 10.0.14.49:<port_number>`

* 标注： 在主页面点击 start tagging

* Evaluate：在右上角option，点击HIt's done

* 导出：在右上角option，点击download

* 新建数据集时List of Entities/Categories是逗号分隔的类别名称

* 在添加数据时有两种方法

    * 文件: 直接上传图片文件至docker容器（！猜测）。
    * url：url文件为一行为一个图片url的格式。在标注时加载至客户端浏览器中，图片不直接储存于服务器端docker容器。


TODO : Pre-annotated data!