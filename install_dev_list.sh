sudo apt-get update
sudo apt-get install cmake git
git clone https://github.com/tensorflow/tensorflow.git

#for caffe
sudo apt-get install  libleveldb-dev libsnappy-dev libopencv-dev libhdf5-serial-dev libatlas-base-dev libopenblas-dev libgflags-dev libgoogle-glog-dev liblmdb-dev
sudo apt-get install --no-install-recommends libboost-all-dev 
wget https://github.com/google/protobuf/releases/download/v2.6.1/protobuf-2.6.1.tar.bz2
tar xjf protobuf-2.6.1.tar.bz2
cd protobuf-*
./configure;make;sudo make install

wget https://dl.bintray.com/boostorg/release/1.67.0/source/boost_1_67_0.tar.bz2;tar xjf boost_1_67_*;cd boost_*;
./bootstrap.sh;./b2;./b2 install

cd ..
git clone  https://github.com/BVLC/caffe.git

#for opencv
wget https://www.nasm.us/pub/nasm/releasebuilds/2.14rc0/nasm-2.14rc0.tar.gz
tar xzf nasm-2.14rc0-xdoc.tar.bz2
cd nasm*
./configure;make;sudo make install

wget ftp://ftp.videolan.org/pub/x264/snapshots/last_x264.tar.bz2

tar xfj last_x264.tar.bz2;
cd x264-*
./configure --enable-shared

sudo apt-get install  libfaac-dev libmp3lame-dev libtheora-dev libvorbis-dev libxvidcore-dev libxext-dev libxfixes-dev

wget https://ffmpeg.org/releases/ffmpeg-4.0.tar.bz2
tar xjf ffmpeg-4.0.tar.bz2 
cd ffmpeg-4.0/
./configure --prefix=/usr/local/ffmpeg  --enable-pic --enable-shared  --enable-gpl --enable-nonfree --enable-postproc --enable-pthreads  --enable-libmp3lame --enable-libx264 --enable-libxvid 

git clone https://github.com/opencv/opencv.git

