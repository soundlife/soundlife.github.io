前端工具配置
============

:slug: frontend-tools-configuration
:date: 2015-09-11
:tags: docker, npm, gulp, bower, webpack, sass
:authors: rex


NPM在国内下载速度比较慢，可以使用淘宝的NPM镜像。配置npmrc。registry那行是为NPM设置的镜像，disturl是为node-gyp设置的镜像。

.. code::

    registry=https://registry.npm.taobao.org
    disturl=http://npm.taobao.org/mirrors/node    

因为npm, bower分别依赖当前目录下的node_modules, bower_components。而有一些包里会一些原生程序，而原生程序不能同时在Mac OS X和boot2docker里运行。在运行CI时，前后端所有步骤都会一次在Docker里运行。为了让所有人都能在自己机器上重现CI上的结果，在boot2docker里运行时，我们把这两个目录设置到了 /usr/local/lib/node 下。不幸的是，这些工具很多都假设这两个目录是在当前目录下，并没有直接配置的方法。

把package.json复制到/usr/local/lib/node/package.json，运行npm时，加上prefix参数

.. code::

    npm install --prefix=/usr/local/lib/node

设置PATH, NODE_PATH环境变量

.. code::

    export PATH=/usr/local/lib/node/node_modules/.bin:$PATH
    export NODE_PATH=/usr/local/lib/node/node_modules

这样一配置，webpack就不工作了。

webpack的配置里有这么一行

.. code::

    module: {loaders: [{ loader: 'babel-loader' }]}

在配置好 node_modules 目录后需要改成

.. code::

    module: {loaders: [{ loader: require.resolve('babel-loader') }]}

接下来修改 bower_components 的路径。先把.bowerrc修改成下面这样

.. code::

    {
      "analytics": false,
      "interactive": false,
      "cwd": "/usr/local/lib/node"
    }


把bower.json复制到/usr/local/lib/node/bower.json

在gulpfile.js里，先增加一行

.. code::

    var bower = require('bower');

接着把所有

.. code::

    gulp.src(mainBowerFiles({}))

改成

.. code::

    gulp.src(mainBowerFiles({paths: bower.config.cwd}))


最后来配置SASS。在Docker里，SASS安装不起来，需要加一个环境变量


.. code::

    export SKIP_SASS_BINARY_DOWNLOAD_FOR_CI=true

SASS找不到bower_components里的文件，需要在gulpfile.js作类似如下配置


.. code::

    .pipe(sass({includePaths: [path.resolve(bower.config.cwd, bower.config.directory)]}))
