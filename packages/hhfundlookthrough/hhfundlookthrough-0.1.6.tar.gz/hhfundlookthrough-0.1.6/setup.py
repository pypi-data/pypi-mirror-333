from setuptools import setup, find_packages

setup(name="hhfundlookthrough",
	  version="0.1.6",
	  packages=find_packages(),
	  install_requires=[
		'cvxpy==1.6.0',
		'hhfactor',
		'scipy==1.13.1'
	  ],
	  author="hh",
	  author_email="hehuang0717@outlook.com",
	  description="fundlookthrough",
	  long_description=open('README.md').read(),
	  long_description_content_type="text/markdown",
	  url="https://your.project.url",
	  classifiers=["Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License",
				   "Operating System :: OS Independent", ],
	  python_requires='>=3.9',
	  package_data={
          'hhfundlookthrough': ['data.json'],  # 在此指定数据文件
      }
      )
