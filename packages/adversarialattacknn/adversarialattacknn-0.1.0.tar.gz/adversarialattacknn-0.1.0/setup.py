from setuptools import setup, find_packages

setup(
    name='adversarialattacknn',
    version='0.1.0',
    author='Santhoshkumar K', 
    author_email='santhoshatwork17@gmail.com',  
    description='A library for adversarial attacks on neural networks',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/santhosh1705kumar/adversarialattacknn',  
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'torch>=1.7.0',
        'timm>=0.4.0',
        'numpy>=1.18.0',
        'torchvision>=0.8.0',
    ],
)
