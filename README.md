# HP 菌数据库平台

这是一个用于管理和搜索 HP 菌株数据的平台，具有用户认证、数据搜索和下载功能。

## 功能特点

- 用户注册与登录
- HP 菌株数据搜索与筛选
- 支持按国家、地区、疾病和耐药性筛选
- 分页显示搜索结果
- 基因序列下载
- 响应式设计，支持移动设备

## 技术栈

- 前端: HTML5, CSS3, JavaScript, Bootstrap 5
- 后端: Node.js, Express.js
- 数据库: PostgreSQL
- 认证: JWT (JSON Web Tokens)

## 安装与设置

### 前提条件

- Node.js (v16 或更高版本)
- PostgreSQL (v12 或更高版本)
- npm 或 yarn

### 1. 克隆仓库

```bash
git clone <repository-url>
cd wechat3
```

### 2. 安装依赖

```bash
npm install
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env` 并填写必要的配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置数据库连接和其他配置：

```env
# 数据库配置
DB_NAME=hpdata
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# JWT 配置
JWT_SECRET=your_jwt_secret
JWT_EXPIRES_IN=30d

# 邮件配置 (可选，用于用户注册验证)
EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_SECURE=false
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_email_password
```

### 4. 初始化数据库

1. 创建 PostgreSQL 数据库：

```sql
CREATE DATABASE hpdata;
```

2. 运行数据库迁移：

```bash
psql -U postgres -d hpdata -f database/schema.sql
```

### 5. 导入数据

将您的 CSV 文件放入项目目录，然后运行：

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 导入数据
python database/import_data.py path/to/your/merged_final_results123_top101.csv
```

或者使用 npm 脚本：

```bash
npm run import-data -- path/to/your/merged_final_results123_top101.csv
```

### 6. 启动应用

开发环境：

```bash
npm run dev
```

生产环境：

```bash
npm start
```

应用将在 http://localhost:3000 上运行。

## 使用指南

### 搜索功能

1. 访问网站并登录
2. 使用顶部的搜索栏或导航到搜索页面
3. 使用筛选器缩小搜索范围：
   - 选择国家
   - 选择地区（选择国家后可用）
   - 选择疾病类型
   - 选择耐药性
4. 点击"搜索"按钮查看结果
5. 点击"下载序列"按钮下载基因序列

### 筛选器说明

- **国家**: 选择菌株来源国家
- **地区**: 选择国家后，可选择特定地区
- **疾病**: 选择与菌株相关的疾病
- **耐药性**: 选择菌株的耐药性特征

## API 文档

### 获取筛选条件

```
GET /api/search/filters
```

### 获取地区（根据国家）

```
GET /api/search/regions?countryId=1
```

### 搜索菌株

```
GET /api/search/strains?page=1&limit=20&countryId=1&regionId=2&diseaseId=3&drugResistanceId=4
```

### 下载基因序列

```
GET /api/strains/:id/download
```

## 部署

### Railway 部署

1. Fork 此仓库到您的 GitHub 账户
2. 登录 [Railway](https://railway.app/)
3. 点击 "New Project" -> "Deploy from GitHub repo"
4. 选择您 fork 的仓库
5. 在 Railway 仪表板中，添加以下环境变量：
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`
   - `DB_HOST`
   - `DB_PORT`
   - `JWT_SECRET`
6. 部署应用

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT
