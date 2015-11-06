使用Docker Compose构建开发环境
==============================

:slug: build-development-environment-with-docker-compose
:date: 2015-08-21
:tags: docker
:authors: rex

一个网站可能会依赖Postgres，Memcache，Redis等等很多程序。依赖的东西多了，要把开发环境配置好，还是很花时间的。用\ `Docker Compose`_\ 就可以很方便的利用现成的Docker Image来启动这些程序。

你需要一个像下面这样的docker-compose.yml

.. code::

    web:
      build: .
      ports:
       - "8000:8000"
      volumes:
       - "${PWD}:/srv/my-project"
      environment:
        USER:
      command: bro start web server at 8000
      links:
       - postgres
       - memcache
       - redis

    postgres:
      image: postgres

    memcache:
      image: memcache

    redis:
      image: redis


volumes用来把当前目录mount到container里。即使是在Mac OS X上用boot2docker，这也是可以工作的，因为boot2docker会把/Users目录映射到虚拟机里。

environment假如value是空的，那么会把运行docker-compose命令所在的环境变量设置成container里的环境变量。

ports用来把container里面的端口映射到container外面。假如你用的是Mac OS X上的boot2docker，需要自行去VirtualBox里设置端口转发。

这些都设置好了之后，运行

.. code::

    docker-compose up -d

这一切就都运行起来了，你可以用

.. code::

    docker-compose logs

观察日志


假如你把container都搞砸了，也没有问题。运行下面这两行代码，再从头开始就好了

.. code::

    docker-compose kill
    docker-compose rm -f

.. _Docker Compose: http://docs.docker.com/compose/


为了加快Image下载速度，可以把registry-mirror设置成https://docker.mirrors.ustc.edu.cn
