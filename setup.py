from setuptools import setup
import mp_kiwoom

setup(
    name='mp_kiwoom',
    version=mp_kiwoom.__version__,
    description='Moon Package for Ebest API',
    url='https://github.com/moonstock/mp_kiwoom',
    author='Moon Jung Sam',
    author_email='monblue@snu.ac.kr',
    license='MIT',
    packages=['mp_kiwoom'],
    # entry_points={'console_scripts': ['mp_kiwoom = mp_kiwoom.__main__:main']},
    keywords='kiwoom openapi',
    # python_requires='>=3.8',  # Python 3.8.6-32 bit
    # install_requires=[ # 패키지 사용을 위해 필요한 추가 설치 패키지
    #     'pythoncom', 
    #     'win32com'
    # ],
    # zip_safe=False
)

