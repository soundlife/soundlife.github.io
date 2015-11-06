把多个flv合并成一个streaming MP4
================================

:slug: concat-flv-into-one-streaming-mp4
:date: 2015-09-25
:tags: ffmpeg, youtube-dl, mp4, flv
:authors: rex

要测试视频播放的功能，需要很多mp4文件。我们可以用youtube-dl从流行的视频网站比如优酷下载到很多视频。

可是优酷的视频却是以分段的flv为主的。因此还需要用ffmpeg把这些flv合并成一个MP4。合并的方法鄂可以参考ffmpeg Wiki里的\ `Concatenate`_\ 条目。

而一个streaming MP4，是以一个duration为0的moov box开头，后面就是一个moof，一个mdat，不断重复直到结束。可以用以下参数来转换。

.. code::

   -movflags frag_keyframe+empty_moov+default_base_moof

.. _Concatenate: https://trac.ffmpeg.org/wiki/Concatenate

把以上代码合并成一个脚本

.. code::

    #!/usr/bin/env bash

    URL="$1"
    FILELIST=$(youtube-dl -F "${URL}" | grep formats | grep -Po '[^ ]+(?=:)')
    FILENAME=$(youtube-dl -e "${URL}" | head -n 1)
    youtube-dl -f flv -o '%(id)s.%(ext)s' "${URL}"
    ffmpeg -f concat -i <(for f in ${FILELIST}; do echo "file '${PWD}/$f.flv'"; done) -c copy -movflags frag_keyframe+empty_moov+default_base_moof "${FILENAME}.mp4"
