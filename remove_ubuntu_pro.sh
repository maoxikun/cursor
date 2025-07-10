#!/bin/bash

# Ubuntu Pro 组件完全删除脚本
# 适用于 Ubuntu 24.04 及更新版本

set -e

echo "=========================================="
echo "Ubuntu Pro 组件删除脚本"
echo "=========================================="

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查是否以root权限运行
check_root() {
    if [[ $EUID -eq 0 ]]; then
        log_error "请不要以root身份直接运行此脚本，脚本会在需要时使用sudo"
        exit 1
    fi
}

# 检查当前Ubuntu Pro状态
check_ua_status() {
    log_info "检查当前Ubuntu Pro状态..."
    
    if command -v ua &> /dev/null; then
        echo "UA工具状态："
        sudo ua status 2>/dev/null || true
    fi
    
    if command -v pro &> /dev/null; then
        echo "Pro工具状态："
        sudo pro status 2>/dev/null || true
    fi
}

# 1. 分离Ubuntu Pro订阅
detach_subscription() {
    log_info "正在分离Ubuntu Pro订阅..."
    
    # 尝试使用ua命令
    if command -v ua &> /dev/null; then
        sudo ua detach 2>/dev/null || log_warn "ua detach失败或未订阅"
    fi
    
    # 尝试使用pro命令
    if command -v pro &> /dev/null; then
        sudo pro detach 2>/dev/null || log_warn "pro detach失败或未订阅"
    fi
}

# 2. 禁用所有Ubuntu Pro服务
disable_services() {
    log_info "正在禁用Ubuntu Pro服务..."
    
    services=("esm-apps" "esm-infra" "livepatch" "fips" "fips-updates" "cc-eal" "cis" "ros" "ros-updates")
    
    for service in "${services[@]}"; do
        if command -v ua &> /dev/null; then
            sudo ua disable "$service" 2>/dev/null || true
        fi
        if command -v pro &> /dev/null; then
            sudo pro disable "$service" 2>/dev/null || true
        fi
    done
}

# 3. 停止systemd服务
stop_systemd_services() {
    log_info "正在停止systemd服务..."
    
    services=("ubuntu-advantage.service" "ua-messaging.service" "ua-reboot-cmds.service" "ubuntu-advantage-timer.timer")
    
    for service in "${services[@]}"; do
        if systemctl is-active --quiet "$service" 2>/dev/null; then
            log_info "停止服务: $service"
            sudo systemctl stop "$service" 2>/dev/null || true
        fi
        
        if systemctl is-enabled --quiet "$service" 2>/dev/null; then
            log_info "禁用服务: $service"
            sudo systemctl disable "$service" 2>/dev/null || true
        fi
    done
}

# 4. 删除Ubuntu Pro软件包
remove_packages() {
    log_info "正在删除Ubuntu Pro相关软件包..."
    
    # 查找已安装的包
    packages=$(dpkg -l 2>/dev/null | grep -E "ubuntu-advantage|ubuntu-pro|ua-" | awk '{print $2}' || true)
    
    if [ -n "$packages" ]; then
        log_info "找到以下包: $packages"
        echo "$packages" | xargs sudo apt remove --purge -y 2>/dev/null || true
    else
        log_info "未找到Ubuntu Pro相关软件包"
    fi
    
    # 删除常见的包（如果存在）
    common_packages=("ubuntu-advantage-tools" "ubuntu-pro-client" "ubuntu-advantage-desktop-daemon" "ubuntu-pro-client-l10n")
    
    for package in "${common_packages[@]}"; do
        if dpkg -l | grep -q "^ii.*$package" 2>/dev/null; then
            log_info "删除包: $package"
            sudo apt remove --purge -y "$package" 2>/dev/null || true
        fi
    done
}

# 5. 清理配置文件和数据
cleanup_files() {
    log_info "正在清理配置文件和数据..."
    
    # 删除配置目录
    directories_to_remove=(
        "/etc/ubuntu-advantage"
        "/var/lib/ubuntu-advantage"
        "/var/cache/ubuntu-advantage"
        "/run/ubuntu-advantage"
    )
    
    for dir in "${directories_to_remove[@]}"; do
        if [ -d "$dir" ]; then
            log_info "删除目录: $dir"
            sudo rm -rf "$dir"
        fi
    done
    
    # 删除日志文件
    sudo find /var/log -name "*ubuntu-advantage*" -type f -delete 2>/dev/null || true
    
    # 删除缓存文件
    sudo find /var/cache -name "*ubuntu-advantage*" -type f -delete 2>/dev/null || true
}

# 6. 清理APT源
cleanup_apt_sources() {
    log_info "正在清理APT源配置..."
    
    # 删除ESM相关源
    sudo find /etc/apt/sources.list.d -name "*ubuntu-esm*" -delete 2>/dev/null || true
    sudo find /etc/apt/sources.list.d -name "*ubuntu-fips*" -delete 2>/dev/null || true
    sudo find /etc/apt/sources.list.d -name "*ubuntu-cis*" -delete 2>/dev/null || true
    
    # 删除ubuntu-advantage相关源
    sudo find /etc/apt -name "*ubuntu-advantage*" -delete 2>/dev/null || true
    sudo find /etc/apt -name "*ubuntu-pro*" -delete 2>/dev/null || true
    
    # 清理apt认证文件
    sudo find /etc/apt/auth.conf.d -name "*ubuntu-advantage*" -delete 2>/dev/null || true
    sudo find /etc/apt/auth.conf.d -name "*ubuntu-pro*" -delete 2>/dev/null || true
}

# 7. 删除systemd服务文件
cleanup_systemd() {
    log_info "正在清理systemd服务文件..."
    
    # 删除服务文件
    sudo find /lib/systemd/system -name "*ubuntu-advantage*" -delete 2>/dev/null || true
    sudo find /lib/systemd/system -name "*ua-*" -delete 2>/dev/null || true
    sudo find /etc/systemd/system -name "*ubuntu-advantage*" -delete 2>/dev/null || true
    sudo find /etc/systemd/system -name "*ua-*" -delete 2>/dev/null || true
    
    # 重新加载systemd
    sudo systemctl daemon-reload
}

# 8. 清理定时任务
cleanup_cron() {
    log_info "正在清理定时任务..."
    
    # 删除cron任务
    sudo find /etc/cron* -name "*ubuntu-advantage*" -delete 2>/dev/null || true
    sudo find /etc/cron* -name "*ubuntu-pro*" -delete 2>/dev/null || true
    sudo find /etc/cron* -name "*ua-*" -delete 2>/dev/null || true
}

# 9. 清理用户配置
cleanup_user_config() {
    log_info "正在清理用户配置..."
    
    # 清理当前用户的配置
    rm -rf ~/.cache/ubuntu-advantage/ 2>/dev/null || true
    rm -rf ~/.config/ubuntu-advantage/ 2>/dev/null || true
    
    # 清理所有用户的配置（需要root权限）
    sudo find /home -name ".cache" -type d -exec find {} -name "*ubuntu-advantage*" -delete \; 2>/dev/null || true
    sudo find /home -name ".config" -type d -exec find {} -name "*ubuntu-advantage*" -delete \; 2>/dev/null || true
}

# 10. 更新系统
update_system() {
    log_info "正在更新系统..."
    
    sudo apt update
    sudo apt autoremove -y
    sudo apt autoclean
}

# 11. 验证删除结果
verify_removal() {
    log_info "正在验证删除结果..."
    
    echo ""
    echo "=== 验证结果 ==="
    
    # 检查剩余的包
    remaining_packages=$(dpkg -l 2>/dev/null | grep -E "ubuntu-advantage|ubuntu-pro|ua-" || true)
    if [ -n "$remaining_packages" ]; then
        log_warn "发现剩余包:"
        echo "$remaining_packages"
    else
        log_info "✅ 所有Ubuntu Pro包已删除"
    fi
    
    # 检查剩余的服务
    remaining_services=$(systemctl list-units --all 2>/dev/null | grep -i "ubuntu-advantage\|ua-" || true)
    if [ -n "$remaining_services" ]; then
        log_warn "发现剩余服务:"
        echo "$remaining_services"
    else
        log_info "✅ 所有Ubuntu Pro服务已删除"
    fi
    
    # 检查剩余的配置文件
    remaining_configs=$(find /etc -name "*ubuntu-advantage*" -o -name "*ubuntu-pro*" 2>/dev/null || true)
    if [ -n "$remaining_configs" ]; then
        log_warn "发现剩余配置文件:"
        echo "$remaining_configs"
    else
        log_info "✅ 所有配置文件已删除"
    fi
    
    # 检查APT源
    remaining_sources=$(find /etc/apt/sources.list.d -name "*ubuntu-esm*" -o -name "*ubuntu-fips*" -o -name "*ubuntu-cis*" 2>/dev/null || true)
    if [ -n "$remaining_sources" ]; then
        log_warn "发现剩余APT源:"
        echo "$remaining_sources"
    else
        log_info "✅ 所有相关APT源已删除"
    fi
}

# 主函数
main() {
    echo ""
    log_info "开始执行Ubuntu Pro组件删除流程..."
    echo ""
    
    # 检查权限
    check_root
    
    # 显示当前状态
    check_ua_status
    
    echo ""
    read -p "确认要继续删除Ubuntu Pro组件吗？(y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "操作已取消"
        exit 0
    fi
    
    echo ""
    log_info "开始删除流程..."
    
    # 执行删除步骤
    detach_subscription
    disable_services
    stop_systemd_services
    remove_packages
    cleanup_files
    cleanup_apt_sources
    cleanup_systemd
    cleanup_cron
    cleanup_user_config
    update_system
    
    echo ""
    log_info "删除流程完成，正在验证结果..."
    verify_removal
    
    echo ""
    log_info "🎉 Ubuntu Pro组件删除完成！"
    log_info "建议重启系统以确保所有更改生效：sudo reboot"
}

# 执行主函数
main "$@"