from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Colab에 기본 설치된 패키지 목록 (2024-05-16 기준, 변경될 수 있음)
colab_installed = [
    'numpy', 'pandas', 'matplotlib', 'scikit-learn', 'scipy',
    'torch', 'torchvision', 'torchaudio', 'tensorboard',
    'jupyter', 'notebook', 'ipykernel', 'ipywidgets', 'seaborn'
]


setup(
    name='dldna',
    version='0.1.4',  # 버전 올림 (새로운 기능 추가)
    packages=find_packages(),
    install_requires=[  # 필수 패키지
        'transformers>=4.30',
        'datasets>=2.10',
        'tqdm>=4.60',
        'pillow>=9.0',
        'opencv-python>=4.5',
        'seaborn_image',
        'torchinfo',
        'pyhessian>=0.1.2',  
        'bayesian-optimization',
        'botorch',
    ],
    extras_require={
        'visualization': ['manim'],
        'dev': [  # 개발용 패키지
            'torchinfo',
            'pyhessian',
            'gudhi',
            'PyWavelets',
            'bayesian-optimization',
            'botorch',
            'sentencepiece',
        ],
        'colab': [  # Colab용 추가 패키지
            'transformers>=4.30',
            'datasets>=2.10',
            'tqdm>=4.60',
            'pillow>=9.0',
            'opencv-python>=4.5',
            'sentencepiece',

        ],
        'all': [  # 모든 패키지 (install_requires + extras_require)
            'manim',
            'torchinfo',
            'seaborn_image',
            'pyhessian',
            'gudhi',
            'PyWavelets',
            'bayesian-optimization',
            'botorch',
            'sentencepiece',
            'transformers>=4.30',
            'datasets>=2.10',
            'tqdm>=4.60',
            'pillow>=9.0',
            'opencv-python>=4.5',
            'jupyter>=1.0.0',
            'notebook>=6.5.0',
            'ipykernel>=6.29.0',
            'ipywidgets>=8.1.0',
            'seaborn',
             'torch>=1.13',
            'torchvision>=0.14',
            'torchaudio>=0.13',
            'tensorboard>=2.8',
            'numpy>=1.22',
            'pandas>=1.5',
            'matplotlib>=3.5',
            'scikit-learn>=1.0',
            'scipy>=1.8',

        ],
    },
    description='Deep Learning DNA: Surviving Architectures and Profound Principles',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Seon Yong Park',
    author_email='baida21@naver.com',
    url='https://github.com/Quantum-Intelligence-Frontier/dldna',
    license='CC BY-NC 4.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
    ],
    python_requires='>=3.7',
)