from setuptools import setup

setup(
    name='scGALA',
    version='0.3.0',
    description='scGala: Graph Link Prediction Based Cell Alignment for Comprehensive Data Integration',
    url='https://github.com/mcgilldinglab/scGALA',
    author='Guo Jiang',
    author_email='guo.jiang@mail.mcgill.ca',
    license='MIT',
    packages=['scGALA'],
    install_requires=['scanpy[leiden]',
                      'torch_geometric',
                      'PyGCL',
                      'lightning',
                      'hnswlib',
                      'ipykernel',
                      'pot'                    
                      ],

    classifiers=[
        'Intended Audience :: Science/Research',
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.10',
    ],
)