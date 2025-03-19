from setuptools import setup, find_packages

setup(name='closedmindedness',
      version='1.1',
      packages=find_packages(),
      install_requires=['bitsandbytes',
                        'transformers',
                        'peft',
                        'torch',
                        'torchvision',
                        'numpy'],
      author='Michalis Mamakos',
      author_email='mamakos@u.northwestern.edu',
      description='Text classifier of closed-mindedness',
      url='https://huggingface.co/mamakos/CMClassifier/',
      classifiers=['Programming Language :: Python :: 3',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   ],
      python_requires='>=3.6'
)