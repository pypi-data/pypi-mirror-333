# mkdocs-pre-build-script

## 安装

```bash
pip intall mkdocs-pre-build-script
```

## 使用

### mkdoc.yal 配置

```yaml
site_name: 我的文档

plugins:
- pre_build_script:
    script:
      - print1.py #可以替换为其他python文件
      - ./src/print2.py
```

> [!tip]
>
> python文件的位置时相对于项目根目录的。

### 示例

示例项目地址：[StudyPavilion/mkdocs_pre_build_script_example: mkdocs_pre_build_script 示例项目](https://github.com/StudyPavilion/mkdocs_pre_build_script_example)

项目结构：

```
mkdocs_pre_build_script_example
├── docs
│   └── index.md
├── src
│   └── print2.py
├── README.md
├── mkdocs.yml
└── print1.py
```

## 编译项目

### windows

安装依赖

```bash
pip install -r requirements.txt
```

打包项目

```bash
python setup.py sdist bdist_wheel
```

