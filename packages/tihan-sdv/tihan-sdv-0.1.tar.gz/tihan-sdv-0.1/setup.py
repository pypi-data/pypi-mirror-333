import setuptools

with open('requirements.txt','r',encoding='utf-8') as fh:
    install_requires = fh.readlines()

setuptools.setup(
    name = "tihan-sdv",
    version = "0.1",
    author= "Arindam Chakraborty",
    description="SDV in python",
    packages=[
        "tihan.sdv.visualizer"
    ],
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
    install_requires=install_requires,
    python_requires=">=3.8",
    setup_requires=["wheel"]

)