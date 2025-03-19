import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Denis_Ivakhov",  # Замените на уникальное имя!
    version="0.0.1",
    author="Denis Ivakhov",
    author_email="d.ivahov2008@gmail.com",  # Замените на ваш email
    description="My simple Python module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/Denis_Ivakhov/my_module_package",  # Если есть репозиторий
    packages=setuptools.find_packages(),  # Находит пакет 'my_package'
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)