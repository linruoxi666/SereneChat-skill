# GitHub 推送指南

## 步骤 1: 在 GitHub 网页上创建仓库

1. 打开浏览器访问 https://github.com
2. 登录你的账户 (用户名: linruoxi666)
3. 点击右上角的 "+" 号，选择 "New repository"
4. 填写仓库信息:
   - Repository name: `xiaolongxia`
   - Description: `小龙虾 - 虚拟女友技能，一个可以进行人格演绎的聊天机器人`
   - 选择 Public 或 Private
   - **不要勾选** "Initialize this repository with a README"
5. 点击 "Create repository"

## 步骤 2: 复制仓库 URL

创建成功后，GitHub 会显示仓库页面。复制页面上显示的仓库 URL，格式类似:
- HTTPS: `https://github.com/linruoxi666/xiaolongxia.git`
- SSH: `git@github.com:linruoxi666/xiaolongxia.git`

## 步骤 3: 添加远程仓库并推送

在你的电脑上打开命令行 (PowerShell 或 CMD)，在 `H:\xiaolongxia` 目录下执行:

```bash
# 添加远程仓库 (将 URL 替换为你复制的仓库地址)
git remote add origin https://github.com/linruoxi666/xiaolongxia.git

# 提交代码 (如果还没有提交)
git commit -m "Initial commit: 小龙虾虚拟女友技能 v1.0.0"

# 推送到 GitHub
git push -u origin master
```

## 步骤 4: 验证推送成功

刷新 GitHub 仓库页面，你应该能看到所有文件已经上传成功。

---

## 完整命令序列

在 `H:\xiaolongxia` 目录下依次执行:

```powershell
# 1. 查看当前状态
git status

# 2. 添加所有文件到暂存区
git add .

# 3. 提交代码
git commit -m "Initial commit: 小龙虾虚拟女友技能 v1.0.0"

# 4. 添加远程仓库
git remote add origin https://github.com/linruoxi666/xiaolongxia.git

# 5. 推送到 GitHub
git push -u origin master
```

---

## 注意事项

1. 第一次推送可能需要输入 GitHub 用户名和密码
2. 如果启用了两步验证，需要使用 Personal Access Token 代替密码
3. 仓库 URL 可以是 HTTPS 或 SSH 格式

---

## 后续更新代码

以后更新代码时，只需执行:
```bash
git add .
git commit -m "你的更新说明"
git push
```
