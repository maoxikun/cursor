# Ubuntu 24.04 删除Ubuntu Pro相关组件完整指南

## 概述

Ubuntu Pro是Canonical提供的企业级支持服务，包含扩展安全维护(ESM)、合规性工具等功能。本指南将帮助您在Ubuntu 24.04系统中完全删除Ubuntu Pro相关组件。

## 1. 检查当前Ubuntu Pro状态

### 检查Ubuntu Pro服务状态
```bash
# 检查Ubuntu Advantage工具状态
sudo ua status

# 或者使用新的命令
sudo pro status
```

### 检查已安装的相关包
```bash
# 查找ubuntu-pro相关包
dpkg -l | grep -E "ubuntu-pro|ubuntu-advantage|ua-"

# 使用apt搜索
apt list --installed | grep -i -E "ubuntu-pro|ubuntu-advantage|ua-"
```

## 2. 停用Ubuntu Pro服务

### 分离/注销Ubuntu Pro订阅
```bash
# 如果已经订阅了Ubuntu Pro服务，先注销
sudo ua detach

# 或者使用新命令
sudo pro detach
```

### 禁用所有Ubuntu Pro服务
```bash
# 禁用ESM-Apps
sudo ua disable esm-apps

# 禁用ESM-Infra  
sudo ua disable esm-infra

# 禁用其他可能的服务
sudo ua disable livepatch
sudo ua disable fips
sudo ua disable fips-updates
sudo ua disable cc-eal
sudo ua disable cis
```

## 3. 删除Ubuntu Pro软件包

### 删除主要包
```bash
# 删除ubuntu-advantage-tools包
sudo apt remove --purge ubuntu-advantage-tools

# 删除ubuntu-pro-client（如果存在）
sudo apt remove --purge ubuntu-pro-client

# 删除其他相关包
sudo apt remove --purge ubuntu-advantage-desktop-daemon
sudo apt remove --purge ubuntu-pro-client-l10n
```

### 删除所有相关包（一次性）
```bash
# 查找并删除所有ubuntu-advantage相关包
sudo apt remove --purge $(dpkg -l | grep -E "ubuntu-advantage|ubuntu-pro|ua-" | awk '{print $2}')
```

## 4. 清理配置文件和数据

### 删除配置目录
```bash
# 删除Ubuntu Advantage配置目录
sudo rm -rf /etc/ubuntu-advantage/

# 删除缓存和状态文件
sudo rm -rf /var/lib/ubuntu-advantage/
sudo rm -rf /var/cache/ubuntu-advantage/

# 删除日志文件
sudo rm -rf /var/log/ubuntu-advantage*
```

### 删除APT源配置
```bash
# 删除ESM相关的APT源
sudo rm -f /etc/apt/sources.list.d/ubuntu-esm*
sudo rm -f /etc/apt/sources.list.d/ubuntu-fips*
sudo rm -f /etc/apt/sources.list.d/ubuntu-cis*

# 删除ubuntu-advantage相关的APT配置
sudo find /etc/apt -name "*ubuntu-advantage*" -delete
sudo find /etc/apt -name "*ubuntu-pro*" -delete
```

## 5. 停止和删除相关服务

### 停止systemd服务
```bash
# 停止ubuntu-advantage相关服务
sudo systemctl stop ubuntu-advantage.service
sudo systemctl disable ubuntu-advantage.service

# 停止其他可能的服务
sudo systemctl stop ua-messaging.service
sudo systemctl disable ua-messaging.service

sudo systemctl stop ua-reboot-cmds.service
sudo systemctl disable ua-reboot-cmds.service
```

### 删除服务文件
```bash
# 删除systemd服务文件
sudo rm -f /lib/systemd/system/ubuntu-advantage*
sudo rm -f /lib/systemd/system/ua-*

# 重新加载systemd
sudo systemctl daemon-reload
```

## 6. 清理定时任务

### 删除cron任务
```bash
# 删除ubuntu-advantage相关的cron任务
sudo rm -f /etc/cron.d/ubuntu-advantage*
sudo rm -f /etc/cron.daily/ubuntu-advantage*

# 检查并删除其他定时任务
sudo find /etc/cron* -name "*ubuntu-advantage*" -delete
sudo find /etc/cron* -name "*ubuntu-pro*" -delete
```

## 7. 更新APT缓存

### 清理和更新
```bash
# 更新包列表
sudo apt update

# 清理无用的包
sudo apt autoremove

# 清理包缓存
sudo apt autoclean
```

## 8. 验证删除结果

### 检查是否完全删除
```bash
# 验证包已删除
dpkg -l | grep -E "ubuntu-pro|ubuntu-advantage|ua-"

# 验证服务已删除
systemctl list-units --all | grep -i "ubuntu-advantage\|ua-"

# 验证配置文件已删除
ls -la /etc/ | grep ubuntu-advantage
ls -la /var/lib/ | grep ubuntu-advantage

# 检查APT源
ls -la /etc/apt/sources.list.d/ | grep -E "ubuntu-esm|ubuntu-fips|ubuntu-cis"
```

## 9. 高级清理（可选）

### 清理用户配置
```bash
# 删除用户目录下的相关配置（如果存在）
rm -rf ~/.cache/ubuntu-advantage/
rm -rf ~/.config/ubuntu-advantage/
```

### 清理环境变量
```bash
# 检查环境变量
env | grep -i ubuntu

# 编辑配置文件删除相关环境变量（如果有）
sudo nano /etc/environment
```

## 10. 一键删除脚本

创建一个脚本来自动化整个删除过程：

```bash
#!/bin/bash
# Ubuntu Pro 完全删除脚本

echo "开始删除Ubuntu Pro组件..."

# 1. 分离服务
sudo ua detach 2>/dev/null || sudo pro detach 2>/dev/null || true

# 2. 禁用所有服务
for service in esm-apps esm-infra livepatch fips fips-updates cc-eal cis; do
    sudo ua disable $service 2>/dev/null || true
done

# 3. 停止服务
sudo systemctl stop ubuntu-advantage.service 2>/dev/null || true
sudo systemctl stop ua-messaging.service 2>/dev/null || true
sudo systemctl stop ua-reboot-cmds.service 2>/dev/null || true

# 4. 删除包
sudo apt remove --purge -y $(dpkg -l | grep -E "ubuntu-advantage|ubuntu-pro|ua-" | awk '{print $2}') 2>/dev/null || true

# 5. 删除配置和数据
sudo rm -rf /etc/ubuntu-advantage/
sudo rm -rf /var/lib/ubuntu-advantage/
sudo rm -rf /var/cache/ubuntu-advantage/
sudo rm -rf /var/log/ubuntu-advantage*

# 6. 删除APT源
sudo rm -f /etc/apt/sources.list.d/ubuntu-esm*
sudo rm -f /etc/apt/sources.list.d/ubuntu-fips*
sudo rm -f /etc/apt/sources.list.d/ubuntu-cis*

# 7. 删除服务文件
sudo rm -f /lib/systemd/system/ubuntu-advantage*
sudo rm -f /lib/systemd/system/ua-*

# 8. 删除定时任务
sudo find /etc/cron* -name "*ubuntu-advantage*" -delete 2>/dev/null || true
sudo find /etc/cron* -name "*ubuntu-pro*" -delete 2>/dev/null || true

# 9. 重新加载和清理
sudo systemctl daemon-reload
sudo apt update
sudo apt autoremove -y

echo "Ubuntu Pro组件删除完成！"
```

## 注意事项

1. **备份重要数据**: 删除前请确保备份重要的系统配置
2. **生产环境谨慎操作**: 在生产环境中操作前请先在测试环境验证
3. **检查依赖关系**: 某些系统可能依赖Ubuntu Pro服务，删除前请确认
4. **安全更新**: 删除Ubuntu Pro后，您将失去扩展安全维护支持
5. **重启系统**: 完成删除后建议重启系统以确保所有更改生效

## 恢复方法

如果需要重新安装Ubuntu Pro：

```bash
# 重新安装ubuntu-advantage-tools
sudo apt update
sudo apt install ubuntu-advantage-tools

# 重新订阅（需要有效的token）
sudo ua attach YOUR_TOKEN
```

通过以上步骤，您可以完全删除Ubuntu 24.04系统中的Ubuntu Pro相关组件。