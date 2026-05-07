@echo off
echo ========================================
echo  小龙虾 - GitHub 推送脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [1/4] 检查 Git 状态...
git status
echo.

echo [2/4] 添加文件到暂存区...
git add .
echo.

echo [3/4] 提交代码 (如果没有提交过)...
git commit -m "Initial commit: 小龙虾虚拟女友技能 v1.0.0" 2>nul
if %errorlevel% equ 0 (
    echo 代码提交成功！
) else (
    echo 代码已经提交过了。
)
echo.

echo [4/4] 推送前设置...
echo.
echo ========================================
echo 重要提示：
echo ========================================
echo.
echo 在推送之前，你需要在 GitHub 网页上创建仓库：
echo.
echo 1. 打开浏览器访问: https://github.com/new
echo 2. Repository name 输入: xiaolongxia
echo 3. Description 输入: 小龙虾 - 虚拟女友技能
echo 4. 选择 Public 或 Private
echo 5. 不要勾选 "Initialize this repository with a README"
echo 6. 点击 "Create repository"
echo.
echo 创建仓库后，返回这里继续。
echo.
echo 或者，你可以在下方提供 GitHub Personal Access Token
echo 来自动创建仓库。
echo.
echo 如果选择手动创建，请访问：
echo https://github.com/new
echo.
echo ========================================
echo.

pause
