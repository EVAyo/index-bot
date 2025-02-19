Name:       index-bot
Version:    1.0.11.0
Release:    1%{?dist}
Summary:    telegram index bot
License:    LGPL

%description
telegram index bot,meda by tg-se.

# 构建前
%prep

# 编译
%build

# 安装
%install
mkdir -p $RPM_BUILD_ROOT/opt/index-bot/
mkdir -p $RPM_BUILD_ROOT/usr/lib/systemd/system

mv ReadMe.md $RPM_BUILD_ROOT/opt/index-bot/

mkdir $RPM_BUILD_ROOT/opt/index-bot/elasticsearch
cp elasticsearch-7.15.2-linux-x86_64.tar.gz $RPM_BUILD_ROOT/opt/index-bot/elasticsearch/
cp elasticsearch-analysis-ik-7.15.2.zip $RPM_BUILD_ROOT/opt/index-bot/elasticsearch/
cp index-bot-elasticsearch.service $RPM_BUILD_ROOT/usr/lib/systemd/system/

mkdir $RPM_BUILD_ROOT/opt/index-bot/java 
cp jdk-11.0.12_linux-x64_bin.tar.gz $RPM_BUILD_ROOT/opt/index-bot/java/

mv bot/ $RPM_BUILD_ROOT/opt/index-bot/bot
cp index-bot.service $RPM_BUILD_ROOT/usr/lib/systemd/system/

# 安装后
%post

# elasticsearch
adduser elasticsearch
tar -zxf /opt/index-bot/elasticsearch/elasticsearch-7.15.2-linux-x86_64.tar.gz -C /opt/index-bot/elasticsearch/
mkdir -p /opt/index-bot/elasticsearch/plugins/ik
unzip /opt/index-bot/elasticsearch/elasticsearch-analysis-ik-7.15.2.zip -d /opt/index-bot/elasticsearch/plugins/ik/
rm /opt/index-bot/elasticsearch/elasticsearch-7.15.2-linux-x86_64.tar.gz
rm /opt/index-bot/elasticsearch/elasticsearch-analysis-ik-7.15.2.zip
chown -R elasticsearch /opt/index-bot/elasticsearch

# java
tar -zxf /opt/index-bot/java/jdk-11.0.12_linux-x64_bin.tar.gz  -C /opt/index-bot/java/
rm /opt/index-bot/java/jdk-11.0.12_linux-x64_bin.tar.gz

systemctl enable index-bot.service
systemctl enable index-bot-elasticsearch.service
systemctl start index-bot.service
systemctl start index-bot-elasticsearch.service

cat /opt/index-bot/ReadMe.md
echo 'Installed successfully'

# 卸载前
%preun
systemctl stop index-bot.service
systemctl stop index-bot-elasticsearch.service
systemctl disable index-bot.service
systemctl disable index-bot-elasticsearch.service
userdel elasticsearch -f
rm -rf /opt/index-bot
echo 'Successfully uninstalled'

# 卸载后
%postun
echo 'Successfully uninstalled'

%files
/opt/dbchk/*
/usr/lib/systemd/system/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
# let's skip this for now
