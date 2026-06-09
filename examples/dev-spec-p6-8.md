# 第一章 代码架构规范

## 1.1 DDD 四层代码结构与依赖规范

### 【1.1.1】DDD 代码四层必须按照 Interface（接口层）、Application（应用服务层）、Domain（领域层）、Infrastructure（基础设施层）分层，其中 Application 和 Domain 为业务核心层，每一层分别对应一个 maven 子模块

**【级别】** 严重

**【描述】**

如下图所示：

> **架构分层示意**（原书为插图，OCR 识别文字如下）
>
> - 用户界面层
> - 应用层
> - 领域层
> - 基础设施层

DDD 之父 Eric Evans 在 2003 年出版的《领域驱动设计：软件核心复杂性应对之道》一书中阐述了他推荐的 DDD 分层架构。在他的架构中，定义了以下层级：

- **表示层（Presentation Layer）**：负责与用户进行交互。
- **应用层（Application Layer）**：定义软件要完成的任务，并且指挥表达领域概念的对象来解决问题。
- **领域层（Domain Layer）**：负责表达业务概念、业务状态信息以及业务规则，是业务软件的核心。
- **基础设施层（Infrastructure Layer）**：为上面各层提供通用的技术能力，为应用层传递消息，为领域层提供持久化机制，为用户界面层绘制屏幕组件等。

前后端分离之后，表示层演化为接口层，不过边界和依赖关系并没有变化。

每一层按照独立 maven 子模块划分，是为了明确各层之间的依赖关系。maven 子模块强制了与其他子模块的依赖关系，是无法打破的，无法 import 不依赖的 maven 子模块内的 package 和类。如果使用 package 简单区分，就缺少了这层强制关系，必须使用其他工具来确保依赖关系，发现成本很高。同时在应用主 jar 包内部，每个独立 maven 子模块都是个独立的 jar 包，具备进一步进行替换的灵活性。

**【反例】**

下图中代码结构是按照聚合划分 maven 模块，模块内 4 层结构再按照 package 进行了划分。主要带来的问题有：

1. 无法通过 maven 子模块依赖来强制约束各层之间的依赖关系。代码内 domain 层可以 import 接口层，或者 application 的类，造成依赖关系混乱。
2. 构建时无法制作为独立的 jar 包，无法进行各层的替代。
3. 领域之间的界限相对模糊，很难做到正交。需要有跨聚合的协调和编排，这些需要有个地方存放。

```text
com.mycompany.blog
├── .article          // 按照聚合分 maven 模块
│   ├── .interfaces
│   ├── .application
│   ├── .domain
│   ├── .infrastructure
│   └── pom.xml
├── .comment          // 按照聚合分 maven 模块
│   ├── .interfaces
│   ├── .application
│   ├── .domain
│   ├── .infrastructure
│   └── pom.xml
└── .starter          // 启动子模块
    ├── BlogApplication.java
    └── pom.xml
```

**【正例】**

DDD 各层作为独立子模块，强制建立子模块之间的依赖关系。各层内部聚合作为 package 进行细分：

```text
com.mycompany.blog
├── .interfaces       // 按照四层结构划分 maven 子模块
│   ├── .article
│   ├── .comment
│   └── pom.xml
├── .application      // 按照四层结构划分 maven 子模块
│   ├── .article
│   ├── .comment
│   └── pom.xml
├── .domain           // 按照四层结构划分 maven 子模块
│   ├── .article
│   ├── .comment
│   └── pom.xml
├── .infrastructure   // 按照四层结构划分 maven 子模块
│   ├── .article
│   ├── .comment
│   └── pom.xml
└── .starter          // 启动子模块
    ├── BlogApplication.java
    └── pom.xml
```

application 层子模块的 pom 文件明确只依赖了 domain 层，这样禁止了 application 层 import 接口层和基础设施层的类：

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <parent>
        <groupId>com.huawei.demo</groupId>
        <artifactId>enrollment</artifactId>
        <version>0.0.1-SNAPSHOT</version>
        <relativePath>../pom.xml</relativePath>
    </parent>
</project>
```

<!--
ocr-quality:
  prose: high
  code: review-required
  source: 开发规范1.pdf pages 6-8
  golden-example: true
-->
