PYTHONPATH=/usr/lib/pymodules/python2.6:`pwd`
for python in \
	~/Projects/python/branches/release2{4,5,6}-maint/python \
	~/Projects/python/trunk/python \
	~/Projects/python/branches/release31-maint/python \
	~/Projects/python/branches/py3k/python; do

    echo $python
    rm -rf build signalfd/_signalfd.so
    $python setup.py build_ext -i && $python signalfd/test/test_signalfd.py

done
