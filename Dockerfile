FROM centos:centos7
WORKDIR /project/
# 安装基础开发包
RUN yum -y install zlib zlib-devel && \
yum -y install bzip2 bzip2-devel && \
yum -y install gcc mariadb-devel && \
yum -y install ncurses ncurses-devel && \
yum -y install readline readline-devel && \
yum -y install openssl openssl-devel && \
yum -y install openssl-static && \
yum -y install xz lzma xz-devel && \
yum -y install sqlite sqlite-devel && \
yum -y install gdbm gdbm-devel && \
yum -y install tk tk-devel && \
yum -y install libffi libffi-devel && \
yum -y install gcc && \
yum -y update glib2
# 安装python3
RUN mkdir /tmp/source_file && \
cd /tmp/source_file && \
curl -O https://mirrors.huaweicloud.com/python/3.9.0/Python-3.9.0.tar.xz && \
tar -xvf Python-3.9.0.tar.xz && \
cd Python-3.9.0 && \
./configure --prefix=/usr/python --enable-shared CFLAGS=-fPIC && \
make && make install && \
touch /etc/ld.so.conf.d/python3.conf && \
echo '/usr/python/lib' > /etc/ld.so.conf.d/python3.conf && \
ldconfig && \
ln -s /usr/python/bin/python3 /usr/bin/python3 && \
ln -s /usr/python/bin/pip3 /usr/bin/pip3
COPY requirements.txt /project/
RUN pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com && \
ln -s /usr/python/bin/gunicorn /usr/bin/gunicorn
# 设置时区
ENV TIME_ZONE=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TIME_ZONE /etc/localtime && echo $TIME_ZONE > /etc/timezone
# 清除安装包
RUN rm -rf /tmp/source_file
