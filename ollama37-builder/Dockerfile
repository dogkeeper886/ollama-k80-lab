FROM rockylinux/rockylinux:8

# Update OS and install cuda toolkit 11.4 and nvdia driver 470
RUN dnf -y update\
    && dnf -y install epel-release\
    && dnf -y config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel8/x86_64/cuda-rhel8.repo\
    && dnf -y module install nvidia-driver:470-dkms\
    && dnf -y install cuda-11-4

# Post install, setup path    
COPY cuda-11.4.sh /etc/profile.d/cuda-11.4.sh

# Install gcc 10
RUN dnf -y install wget unzip lbzip2\
    && dnf -y groupinstall "Development Tools"\
    && cd /usr/local/src\
    && wget https://github.com/gcc-mirror/gcc/archive/refs/heads/releases/gcc-10.zip\
    && unzip gcc-10.zip\
    && cd gcc-releases-gcc-10\
    && contrib/download_prerequisites\
    && mkdir /usr/local/gcc-10\
    && cd /usr/local/gcc-10\
    && /usr/local/src/gcc-releases-gcc-10/configure --disable-multilib\
    && make -j ${nproc}\
    && make install

# Post install, setup path
COPY gcc-10.sh /etc/profile.d/gcc-10.sh
COPY gcc-10.sh /etc/ld.so.conf.d/gcc-10.sh

# Install cmake
RUN dnf -y install openssl-devel\
    && cd /usr/local/src\
    && wget https://github.com/Kitware/CMake/releases/download/v4.0.0/cmake-4.0.0.tar.gz\
    && tar xvf cmake-4.0.0.tar.gz\
    && mkdir /usr/local/cmake-4\
    && cd /usr/local/cmake-4\
    && /usr/local/src/cmake-4.0.0/configure\
    && make -j ${nproc}\
    && make install

# Install go
RUN cd /usr/local\
    && wget https://go.dev/dl/go1.24.2.linux-amd64.tar.gz\
    && tar xvf go1.24.2.linux-amd64.tar.gz

