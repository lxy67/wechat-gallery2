# Zeabur 部署指南

## 准备工作

1. 确保所有文件已提交到 GitHub 仓库
2. 注册 [Zeabur](https://zeabur.com/) 账号并登录

## 部署步骤

### 1. 生成数据库文件

在本地运行以下命令生成 `database.sql` 文件：

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 生成 SQL 文件
python import_data.py
```

这将创建一个包含数据库结构和数据的 `database.sql` 文件。

### 2. 部署到 Zeabur

1. 登录 [Zeabur 控制台](https://dash.zeabur.com/)
2. 点击 "New Project" 按钮
3. 选择 "Import from GitHub" 并授权访问你的仓库
4. 选择你的仓库
5. 等待构建完成

### 3. 设置环境变量

在 Zeabur 控制台中：

1. 进入你的项目
2. 点击 "Environment Variables" 标签页
3. 添加以下环境变量：

```
NODE_ENV=production
PORT=3000
JWT_SECRET=your_secure_jwt_secret
DATABASE_URL=postgresql://username:password@host:port/dbname
```

### 4. 设置数据库

1. 在 Zeabur 控制台中，点击 "Add Service"
2. 选择 "PostgreSQL"
3. 等待数据库服务启动
4. 复制数据库连接字符串
5. 更新环境变量中的 `DATABASE_URL`

### 5. 导入数据库

1. 在 Zeabur 控制台中，进入你的 Node.js 服务
2. 点击 "Console" 标签页
3. 运行以下命令导入数据库：

```bash
# 连接到数据库
psql $DATABASE_URL -f database.sql
```

### 6. 启动应用

1. 在 Zeabur 控制台中，进入你的 Node.js 服务
2. 确保 "Start Command" 设置为：

```
npm start
```

3. 点击 "Restart" 按钮重启服务

## 访问应用

1. 在 Zeabur 控制台中，找到你的服务
2. 点击生成的域名访问应用
3. 或者绑定自定义域名

## 故障排除

1. **数据库连接问题**：
   - 检查 `DATABASE_URL` 格式是否正确
   - 确保数据库服务已启动

2. **构建失败**：
   - 检查 `package.json` 中的依赖
   - 查看构建日志中的错误信息

3. **应用无法启动**：
   - 检查端口配置
   - 查看应用日志

## 更新应用

1. 推送代码到 GitHub
2. Zeabur 会自动重新部署
3. 如果需要重新导入数据，重复步骤 5

## 联系我们

如有问题，请通过以下方式联系我们：
- 邮箱：support@example.com
- GitHub Issues: [Issues](https://github.com/yourusername/your-repo/issues)
