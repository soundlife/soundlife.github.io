合并多层Docker Image
====================

:slug: flatten-docker-images
:date: 2015-09-04
:tags: docker
:authors: rex

用docker build生成出来的Docker Image会有很多层。Docker并不提供工具直接合并。而网上有很多人建议通过导出container来合并。可是这样，虽然所有文件都合并到一层了，Image的元信息都丢了。

根据\ `Docker Image Specification`_\ ，我们可以自己来补充这些信息

.. _Docker Image Specification: https://github.com/docker/docker/blob/master/image/spec/v1.md


首先导出 container

.. code::

    docker export --output="layer.tar" "${CONTAINER_ID}"

按照Spec，Image的ID是用随机数的，在这里用hash也不是什么问题。

.. code::

    FLATTENED_IMAGE_ID="$(sha256sum layer.tar | grep -Eo '^[a-f0-9]+')"

接着建立Spec所要求的文件，把元信息从原始Image里复制过来

.. code::

    cat > repositories << EOF
    {"${PROJECT_NAME}": {"${IMAGE_VERSION}": "${FLATTENED_IMAGE_ID}"}}
    EOF

    mkdir ${FLATTENED_IMAGE_ID}
    mv layer.tar ${FLATTENED_IMAGE_ID}/


    cat > ${FLATTENED_IMAGE_ID}/VERSION << EOF
    1.0
    EOF

    cat > ${FLATTENED_IMAGE_ID}/json << EOF
    {"Id": "${FLATTENED_IMAGE_ID}",
    "Created": $(docker inspect --format "{{json .Created}}" ${ORIGIN_IMAGE_ID}),
    "Config": $(docker inspect --format "{{json .Config}}" ${ORIGIN_IMAGE_ID}),
    "Architecture": $(docker inspect --format "{{json .Architecture}}" ${ORIGIN_IMAGE_ID}),
    "Os": $(docker inspect --format "{{json .Os}}" ${ORIGIN_IMAGE_ID}),
    "DockerVersion": $(docker inspect --format "{{json .DockerVersion}}" ${ORIGIN_IMAGE_ID}),
    "Size": $(stat --format '%s' ${FLATTENED_IMAGE_ID}/layer.tar)
    }
    EOF

把这些文件合并成tarball，并导入docker

.. code::

    tar cvf "../${TARBALL}" *
    cd ..

    docker load --input "${TARBALL}"

这样，Image就只剩下一层了。
