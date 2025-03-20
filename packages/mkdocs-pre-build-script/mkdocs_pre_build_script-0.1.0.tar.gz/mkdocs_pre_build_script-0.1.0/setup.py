from setuptools import setup, find_packages

# 读取 README 文件内容
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='mkdocs-pre-build-script',
    version='0.1.0',
    description='A MkDocs plugin to run a Python script before build',
long_description=long_description,  # 添加 long_description 字段
    long_description_content_type='text/markdown',  # 指定内容类型为 Markdown
    author='StudyPavilion',
    author_email='studypavilion@163.com',
    url='https://github.com/StudyPavilion/mkdocs_pre_build_script',
    packages=find_packages(),
    install_requires=[
        'mkdocs',
    ],
    entry_points={
        'mkdocs.plugins': [
            'mkdocs-pre-build-script = pre_build_script.pre_build_script:MkdocsPreBuildScript',
        ]
    },
)
