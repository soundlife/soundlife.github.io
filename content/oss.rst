AWS S3和阿里云 OSS API的区别
============================

:slug: difference-between-aws-s3-and-aliyun-oss-api
:date: 2015-09-18
:tags: s3, oss
:authors: rex

阿里云OSS除了功能比AWS S3少不少以外，API大致上和AWS S3是一样的，只是有一些微小的差别。

AWS S3上Authorization Header是以AWS开头的，阿里云OSS是用OSS开头的。一些特殊的header，AWS S3是以x-amz开头的，阿里云OSS是用x-oss开头的。

计算canonical string时，Resource，AWS S3是直接取原始字符串的，阿里云OSS是取解析后的，比如

.. code::

    PUT /%E5%A5%BD

AWS S3里最后一行要用

.. code::

    /bucket-name/%E5%A5%BD

阿里云OSS里最后一行要用


.. code::

    /bucket-name/好

在Copy Object时，x-oss-copy-source必须以/开头，比如

.. code::

    x-oss-copy-source: /bucket-name/object-name

不知道为啥AWS S3可以不用，至少boto没有以/开头。

另外一个特殊的地方是，假如你发的Header里x-oss-date不为空，而Date为空，计算canonical string时，两者都应该取x-oss-date的值。这个在用浏览器上传文件时比较重要，因为XMLHttpRequest不能设置Date Header。



